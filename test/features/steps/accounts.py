import httplib
import json

from behave import given, when
from hamcrest import assert_that, equal_to

from steps.auth import authenticate


def get_account_id_by_realm(context, realm):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']
    conn = httplib.HTTPSConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("GET", "/v2/accounts/{}/children".format(reseller_id), headers=headers)

    response = json.loads(conn.getresponse().read())
    conn.close()

    for elm in response['data']:
        if elm['realm'] == realm:
            return elm['id']

    return None


@given(u'an account for realm "{realm}"')
def step_impl(context, realm):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']
    owner_id = auth['data']['owner_id']
    body = json.dumps({
        "data": {
            "name": realm,
            "realm": realm,
            "contract": {
                "representative": {
                    "account_id": reseller_id,
                    "user_id": owner_id
                }
            }
        }
    })
    conn = httplib.HTTPSConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("PUT", "/v2/accounts/{}".format(reseller_id), body, headers)
    response = conn.getresponse()
    conn.close()

    assert_that(response.status, equal_to(201), response.reason)


@when(u'delete the account with realm "{realm}"')
def step_impl(context, realm):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    account_id = get_account_id_by_realm(context, realm)

    conn = httplib.HTTPSConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("DELETE", "/v2/accounts/{}".format(account_id), headers=headers)
    response = conn.getresponse()
    conn.close()

    assert_that(response.status, equal_to(200), response.reason)
