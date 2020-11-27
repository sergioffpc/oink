import httplib
import json
import re
import threading
import time

import pjsua as pj

from behave import when, then
from hamcrest import assert_that, not_none

from steps.accounts import get_account_id_by_realm
from steps.auth import authenticate


current_call = None


class AccountCallback(pj.AccountCallback):
    sem = None

    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        if self.sem:
            if self.account.info().reg_status >= 200:
                self.sem.release()

    def on_incoming_call(self, call):
        call_info = call.info()
        print "*** incoming call from {} to {}: [{}]".format(call_info.remote_uri, call_info.uri, call_info.state_text)

        call_cb = CallCallback(call)
        call.set_callback(call_cb)

        call.answer(180)


class CallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    def on_state(self):
        global current_call
        print "Call with", self.call.info().remote_uri,
        print "is", self.call.info().state_text,
        print "last code =", self.call.info().last_code,
        print "(" + self.call.info().last_reason + ")"

        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print 'Current call is', current_call

    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pj.Lib.instance().conf_connect(call_slot, 0)
            pj.Lib.instance().conf_connect(0, call_slot)
            print "Media is now active"
        else:
            print "Media is inactive"


@when(u'we register a device with username "{username}" and password "{password}" on realm "{realm}"')
def step_impl(context, username, password, realm):
    acc_cfg = pj.AccountConfig(username=username.encode('utf-8'),
                               password=password.encode('utf-8'),
                               domain=realm.encode('utf-8'),
                               proxy="sip:{};lr".format(context.config.userdata['proxy']))
    acc = context.pj_lib.create_account(acc_cfg)

    acc_cb = AccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    context.pj_devices["sip:{}@{}".format(username, realm)] = acc


@when(u'"{src_uri}" makes a call to "{dst_uri}"')
def step_impl(context, src_uri, dst_uri):
    acc = context.pj_devices[src_uri]
    call = acc.make_call(dst_uri.encode('utf-8'), cb=CallCallback())

    context.pj_calls[(src_uri, dst_uri)] = call


@when(u'"{dst_uri}" hangs up the call from "{src_uri}"')
def step_impl(context, dst_uri, src_uri):
    call = context.pj_calls[(src_uri, dst_uri)]
    assert_that(call, not_none())

    call.hangup()


@when(u'"{dst_uri}" accepts the call from "{src_uri}"')
def step_impl(context, dst_uri, src_uri):
    call = context.pj_calls[(src_uri, dst_uri)]
    assert_that(call, not_none())

    call.answer(200)


@then(u'the call record detail from realm "{realm}" for call tagged as "{tag}" must have the following attributes')
def step_impl(context, realm, tag):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    account_id = get_account_id_by_realm(context, realm)
    conn = httplib.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("GET", "/v2/accounts/{}/cdrs".format(account_id), headers=headers)
    response = json.loads(conn.getresponse().read())
    conn.close()

    cdr_id = response['data'][0]['id']
    conn.request("GET", "/v2/accounts/{}/cdrs/{}".format(account_id, cdr_id), headers=headers)
    response = json.loads(conn.getresponse().read())
    conn.close()

    for row in context.table:
        for heading in context.table.headings:
            assert response['data'][heading] == row[heading]
