import re
import time
import uuid
from hashlib import md5

from behave import when, then, given
from hamcrest import assert_that, matches_regexp

from sip_parser.sip_message import SipMessage


def replace(context, term):
    return str(context.ua_dict[term.group(1)])


def evaluate(context, term):
    return eval(term, {
        'vars': context.ua_dict,
        'last': context.ua_last_message,
        'md5_digest': md5_digest,
    }, {}).strip('\"')


def md5_digest(message, password):
    search = re.search('sip:([^@]+)@([^@]+)', message.headers['from']['uri'])
    username = search.group(1)
    realm = search.group(2)

    nonce = str(message.headers['www-authenticate'][0]['nonce']).strip('\"')
    digest0 = md5("{}:{}:{}".format(username, realm, password).encode('utf-8')).hexdigest()
    digest1 = md5("REGISTER:sip:{}".format(realm).encode('utf-8')).hexdigest()

    return md5("{}:{}:{}".format(digest0, nonce, digest1).encode('utf-8')).hexdigest()


@given(u'the following UAC agent variables')
def step_impl(context):
    for row in context.table:
        context.ua_dict[row['variable']] = row['value']


@when(u'UAC agent starts a new transaction')
def step_impl(context):
    context.ua_dict['branch'] = uuid.uuid4()
    context.ua_dict['tag'] = uuid.uuid4()
    context.ua_dict['cseq'] = context.ua_dict['cseq'] + 1


@when(u'UAC agent sends the message')
def step_impl(context):
    message = ""
    for line in context.text.encode('utf-8').splitlines():
        evaluated = re.sub(r"`([^`]+)`", lambda term: evaluate(context, term.group(1)), line)
        message += re.sub(r"\[(\w+)]", lambda term: replace(context, term), evaluated) + '\r\n'
    message += '\r\n'

    context.ua_sock.sendto(bytes(message), (context.ua_dict['remote_ip'], context.ua_dict['remote_port']))
    context.ua_last_message = SipMessage.from_string(message)


@then(u'UAC agent must receive a message')
def step_impl(context):
    time.sleep(1)

    context.ua_queue_lock.acquire()
    message = context.ua_queue.pop(0)
    context.ua_queue_lock.release()

    actual = message.split('\r\n')
    expected = context.text.encode('utf-8').splitlines()
    for i in range(len(expected)):
        actual_line = actual[i]
        evaluated = re.sub(r"`([^`]+)`", lambda term: evaluate(context, term.group(1)), expected[i])
        expected_line = re.sub(r"\[(\w+)]", lambda term: replace(context, term), evaluated)
        assert_that(actual_line, matches_regexp(expected_line), message)

    context.ua_last_message = SipMessage.from_string(message)


@then(u'evaluate expression "{expr}" to variable "{var}"')
def step_impl(context, expr, var):
    context.ua_dict[var] = evaluate(context, expr)
