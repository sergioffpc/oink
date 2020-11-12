import http.client
import json
import re
import uuid

from behave import given

from steps.accounts import get_account_id_by_name
from steps.auth import authenticate


def create_user(context, account_id, user_name, user_ext):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    body = json.dumps({
        "data": {
            "caller_id": {
                "internal": {
                    "name": user_name,
                    "number": user_ext
                }
            },
            "presence_id": user_ext,
            "first_name": user_name,
            "last_name": user_name,
            "priv_level": "user",
            "username": user_name,
            "password": user_name
        }
    })
    conn = http.client.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("PUT", f"/v2/accounts/{account_id}/users", body, headers)
    response = conn.getresponse()
    print(response.read())

    conn.close()

    return response


def create_callflow(context, account_id, user_name, user_ext):
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
            "name": user_name,
            "numbers": [user_ext],
            "owner_id": callflow_id,
            "type": "mainUserCallflow"
        }
    })
    conn = http.client.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("PUT", f"/v2/accounts/{account_id}/callflows", body, headers)
    response = conn.getresponse()
    print(response.read())

    conn.close()

    return response


def create_device(context, account_id, user_name):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    body = json.dumps({
        "data": {
            "sip": {
                "password": user_name,
                "realm": context.config.userdata['realm'],
                "username": user_name
            },
            "device_type": "softphone",
            "enabled": "true",
            "media": {
                "audio": {
                    "codecs": ["PCMU", "PCMA"]
                }
            },
            "name": user_name
        }
    })
    conn = http.client.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("PUT", f"/v2/accounts/{account_id}/devices", body, headers)
    response = conn.getresponse()
    print(response.read())

    conn.close()

    return response


@given(u'an user with name "{user_name}" and extension "{user_ext}" for account "{acc_name}"')
def step_impl(context, user_name, user_ext, acc_name):
    account_id = get_account_id_by_name(context, acc_name)

    response = create_user(context, account_id, user_name, user_ext)
    assert response.status == 201

    response = create_callflow(context, account_id, user_name, user_ext)
    assert response.status == 201

    response = create_device(context, account_id, user_name)
    assert response.status == 201
