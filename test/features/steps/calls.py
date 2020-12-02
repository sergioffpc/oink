import httplib
import json
import threading

import pjsua as pj
from behave import when, then
from hamcrest import assert_that, equal_to, not_none, greater_than

from steps.accounts import get_account_id_by_realm
from steps.auth import authenticate

A_LEG = 0
B_LEG = 1

current_call_tag = None
call_tracker = {}


# An account specifies the identity of the person (or endpoint) on one side of SIP conversation.  At least one account
# instance needs to be created before anything else, and from the account instance you can start making/receiving calls
# as well as adding buddies.
class AccountCallback(pj.AccountCallback):
    def __init__(self, context, account=None):
        self.sem = None
        self.context = context
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()

        print "*** register: uri={}, code={} [{}]".format(self.account.info().uri,
                                                          self.account.info().reg_status,
                                                          self.account.info().reg_reason)

    def on_incoming_call(self, call):
        call_info = call.info()
        print "*** incoming call: uri={}, remote_uri={} [{}]".format(call_info.uri,
                                                                     call_info.remote_uri,
                                                                     call_info.state_text)

        global current_call_tag, call_tracker
        call_tracker[current_call_tag][B_LEG] = call
        current_call_tag = None

        call_cb = CallCallback(self.context, call)
        call.set_callback(call_cb)
        call.answer(180)


# This class represents an ongoing call (or speaking technically, an INVITE session) and can be used to manipulate it,
# such as to answer the call, hangup the call, put the call on hold, transfer the call, etc.
class CallCallback(pj.CallCallback):
    def __init__(self, context, call=None):
        self.sem = None
        self.context = context
        pj.CallCallback.__init__(self, call)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_state(self):
        call_info = self.call.info()
        if self.sem:
            if call_info.state != pj.CallState.NULL:
                self.sem.release()

        print "*** call: uri={}, remote_uri=<{}> [{}] code={} [{}]".format(call_info.uri,
                                                                           call_info.remote_uri,
                                                                           call_info.state_text,
                                                                           call_info.last_code,
                                                                           call_info.last_reason)

    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            call_slot = self.call.info().conf_slot
            player_slot = self.context.pj_lib.player_get_slot(self.context.pj_caller_player)
            self.context.pj_lib.conf_connect(player_slot, call_slot)


@when(u'we register a device with username "{username}" and password "{password}" on realm "{realm}"')
def step_impl(context, username, password, realm):
    acc_cfg = pj.AccountConfig(username=username.encode('utf-8'),
                               password=password.encode('utf-8'),
                               domain=realm.encode('utf-8'),
                               proxy="sip:{};lr".format(context.config.userdata['proxy']))
    acc = context.pj_lib.create_account(acc_cfg)

    acc_cb = AccountCallback(context, acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    context.pj_devices["sip:{}@{}".format(username, realm)] = acc


@when(u'"{src_uri}" makes a call to "{dst_uri}" tagged as "{tag}"')
def step_impl(context, src_uri, dst_uri, tag):
    global current_call_tag, call_tracker
    current_call_tag = tag.encode('utf-8')

    acc = context.pj_devices[src_uri.encode('utf-8')]

    hdr_list = []
    if context.table is not None:
        for row in context.table:
            hdr_list.append((row['header_name'].encode('utf-8'), row['header_value'].encode('utf-8')))

    call_cb = CallCallback(context)
    call = acc.make_call(dst_uri.encode('utf-8'), cb=call_cb, hdr_list=hdr_list)
    call_tracker[current_call_tag] = [call, None]
    call_cb.wait()


@when(u'"{leg}" leg channel from call tagged as "{tag}" on realm "{realm}" must have the following attributes')
def step_impl(context, leg, tag, realm):
    global call_tracker
    call = call_tracker[tag][A_LEG if leg == "a" else B_LEG]
    call_id = call.info().sip_call_id

    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    account_id = get_account_id_by_realm(context, realm)
    conn = httplib.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("GET", "/v2/accounts/{}/channels/{}".format(account_id, call_id), headers=headers)
    response = conn.getresponse()
    assert_that(response.status, equal_to(200), response.reason)

    channel_details = json.loads(response.read())
    assert_that(len(channel_details['data']), greater_than(0))

    conn.close()

    for row in context.table:
        for heading in context.table.headings:
            assert_that(str(channel_details['data'][heading]), equal_to(row[heading]), heading)


@when(u'accepts the call tagged as "{tag}"')
def step_impl(context, tag):
    global call_tracker
    call = call_tracker[tag][B_LEG]

    assert_that(call, not_none())
    call.answer(200)


@when(u'"{leg}" leg hangs up the call tagged as "{tag}"')
def step_impl(context, leg, tag):
    global call_tracker
    call = call_tracker[tag][A_LEG if leg == "a" else B_LEG]

    assert_that(call, not_none())
    call.hangup()


@then(u'call record detail from call tagged as "{tag}" on realm "{realm}" must have the following attributes')
def step_impl(context, tag, realm):
    global call_tracker
    call = call_tracker[tag][A_LEG]
    call_id = call.info().sip_call_id

    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    account_id = get_account_id_by_realm(context, realm)
    conn = httplib.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("GET", "/v2/accounts/{}/cdrs".format(account_id), headers=headers)
    response = conn.getresponse()
    assert_that(response.status, equal_to(200), response.reason)

    cdrs = json.loads(response.read())

    conn.close()

    for cdr in cdrs['data']:
        if cdr['call_id'] == call_id:
            conn.request("GET", "/v2/accounts/{}/cdrs/{}".format(account_id, cdr['id']), headers=headers)
            response = conn.getresponse()
            assert_that(response.status, equal_to(200), response.reason)

            cdr_details = json.loads(response.read())
            assert_that(len(cdr_details['data']), greater_than(0))

            conn.close()

            for row in context.table:
                for heading in context.table.headings:
                    assert_that(str(cdr_details['data'][heading]), equal_to(row[heading]), heading)
