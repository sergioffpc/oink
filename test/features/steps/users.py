import httplib
import json
import urlparse

from behave import given
from hamcrest import assert_that, equal_to

from steps.accounts import get_account_id_by_realm
from steps.auth import authenticate


def get_user_id_by_name(context, account_id, name):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    url = urlparse.urlparse(context.config.userdata['api'])
    if url.scheme == "https":
        conn = httplib.HTTPSConnection(url.hostname, url.port)
    else:
        conn = httplib.HTTPConnection(url.hostname, url.port)
    conn.request("GET", "/v2/accounts/{}/users".format(account_id), headers=headers)
    response = json.loads(conn.getresponse().read())
    conn.close()

    for elm in response['data']:
        if elm['username'] == name:
            return elm['id']

    return None


def get_user_by_id(context, account_id, user_id):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    url = urlparse.urlparse(context.config.userdata['api'])
    if url.scheme == "https":
        conn = httplib.HTTPSConnection(url.hostname, url.port)
    else:
        conn = httplib.HTTPConnection(url.hostname, url.port)
    conn.request("GET", "/v2/accounts/{}/users/{}".format(account_id, user_id), headers=headers)
    response = json.loads(conn.getresponse().read())
    conn.close()

    return response


def create_user(context, account_id, username, extension):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    body = json.dumps({
        "data": {
            "caller_id": {
                "internal": {
                    "name": username,
                    "number": extension
                }
            },
            "presence_id": extension,
            "first_name": username,
            "last_name": username,
            "priv_level": "user",
            "username": username,
            "password": username
        }
    })

    url = urlparse.urlparse(context.config.userdata['api'])
    if url.scheme == "https":
        conn = httplib.HTTPSConnection(url.hostname, url.port)
    else:
        conn = httplib.HTTPConnection(url.hostname, url.port)
    conn.request("PUT", "/v2/accounts/{}/users".format(account_id), body, headers)
    response = conn.getresponse()

    assert_that(response.status, equal_to(201), response.reason)

    conn.close()

    return response


@given(u'an user with name "{user}" and extension "{extension}" for realm "{realm}"')
def step_impl(context, user, extension, realm):
    account_id = get_account_id_by_realm(context, realm)

    response = create_user(context, account_id, user, extension)
    assert_that(response.status, equal_to(201), response.reason)
