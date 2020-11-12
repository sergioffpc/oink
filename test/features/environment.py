import http.client
import json

from steps.auth import authenticate


def erase(context):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']
    conn = http.client.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("GET", f"/v2/accounts/{reseller_id}/children", headers=headers)
    response = json.loads(conn.getresponse().read())

    for elm in response['data']:
        if elm['realm'] == context.config.userdata['realm']:
            account_id = elm['id']
            conn.request("DELETE", f"/v2/accounts/{account_id}", headers=headers)
            assert conn.getresponse().status == 200

    conn.close()


def before_scenario(context, scenario):
    """
    These run before each scenario is run.
    """
    erase(context)


def after_scenario(context, scenario):
    """
    These run after each scenario is run.
    """
    erase(context)
