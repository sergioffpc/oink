import httplib
import json
import re
import uuid

from behave import given
from hamcrest import assert_that, equal_to

from steps.accounts import get_account_id_by_realm
from steps.auth import authenticate
from steps.users import get_user_id_by_name, get_user_by_id


def create_callflow(context, account_id, username, extension):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    callflow_id = re.sub('-', '', str(uuid.uuid4()))
    body = json.dumps({
        "data": {
            "flow": {
                "data": {
                    "timeout": 20,
                    "id": callflow_id
                },
                "module": "user"
            },
            "name": username,
            "numbers": [extension],
            "owner_id": callflow_id,
            "type": "mainUserCallflow"
        }
    })
    conn = httplib.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("PUT", "/v2/accounts/{}/callflows".format(account_id), body, headers)
    response = conn.getresponse()
    conn.close()

    return response


def create_device(context, account_id, user_id, username, password):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    body = json.dumps({
        "data": {
            "enabled": "true",
            "media": {
                "audio": {
                    "codecs": ["PCMU", "PCMA"]
                },
            },
            "sip": {
                "method": "password",
                "invite_format": "contact",
                "username": username,
                "password": password,
                "expire_seconds": "360"
            },
            "device_type": "softphone",
            "name": username,
            "owner_id": user_id
        }
    })
    conn = httplib.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("PUT", "/v2/accounts/{}/devices".format(account_id), body, headers)
    response = conn.getresponse()
    conn.close()

    return response


@given(u'a device with username "{username}", password "{password}" for user "{user}" on realm "{realm}"')
def step_impl(context, username, password, user, realm):
    account_id = get_account_id_by_realm(context, realm)
    user_id = get_user_id_by_name(context, account_id, user)

    user = get_user_by_id(context, account_id, user_id)

    response = create_callflow(context, account_id, username, user['data']['presence_id'])
    assert_that(response.status, equal_to(201), response.reason)

    response = create_device(context, account_id, user_id, username, password)
    assert_that(response.status, equal_to(201), response.reason)
