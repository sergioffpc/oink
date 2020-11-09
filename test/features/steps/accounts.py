from behave import *

import http.client
import json

from steps.auth import authenticate
from steps.config import config, config_env


def get_account_id_by_name(auth, name):
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']
    conn = http.client.HTTPConnection(config_env['host'], config_env['port'])
    conn.request("GET", f"/v2/accounts/{reseller_id}/children", headers=headers)

    response = json.loads(conn.getresponse().read())
    conn.close()

    for elm in response['data']:
        if elm['name'] == name and elm['realm'] == config['environment']['realm']:
            return elm['id']

    return None


@given(u'an account with name "{acc_name}"')
def step_impl(context, acc_name):
    auth = authenticate()
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']
    owner_id = auth['data']['owner_id']
    body = json.dumps({
        "data": {
            "language": "en-US",
            "name": acc_name,
            "timezone": "America/Los_Angeles",
            "realm": config['environment']['realm'],
            "contract": {
                "representative": {
                    "account_id": reseller_id,
                    "user_id": owner_id,
                    "name": "Account Admin"
                }
            }
        }
    })
    conn = http.client.HTTPConnection(config_env['host'], config_env['port'])
    conn.request("PUT", f"/v2/accounts/{reseller_id}", body, headers)

    response = conn.getresponse()
    print(response.read())

    conn.close()

    assert response.status == 201


@when(u'delete account with name "{acc_name}"')
def step_impl(context, acc_name):
    auth = authenticate()
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    account_id = get_account_id_by_name(auth, acc_name)

    conn = http.client.HTTPConnection(config_env['host'], config_env['port'])
    conn.request("DELETE", f"/v2/accounts/{account_id}", headers=headers)
    response = conn.getresponse()
    print(response.read())

    conn.close()

    assert response.status == 200
