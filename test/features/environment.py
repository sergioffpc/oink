import httplib
import json

import pjsua as pj
from hamcrest import assert_that, equal_to

from steps.auth import authenticate


def erase(context):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']
    conn = httplib.HTTPConnection(context.config.userdata['host'], context.config.userdata['port'])
    conn.request("GET", "/v2/accounts/{}/children".format(reseller_id), headers=headers)
    response = conn.getresponse()

    assert_that(response.status, equal_to(200), response.reason)

    body = json.loads(response.read())
    for elm in body['data']:
        conn.request("DELETE", "/v2/accounts/{}".format(elm['id']), headers=headers)
        response = conn.getresponse()

        assert_that(response.status, equal_to(200), response.reason)

    conn.close()


def log_cb(level, message, length):
    print message,


def before_scenario(context, scenario):
    """
    These run before each scenario is run.
    """
    erase(context)

    context.pj_lib = pj.Lib()

    # Init library with default config and some customized
    # logging config.
    ua_cfg = pj.UAConfig()
    ua_cfg.max_calls = 16
    context.pj_lib.init(ua_cfg=ua_cfg, log_cfg=pj.LogConfig(level=0, callback=log_cb))

    # Create UDP transport which listens to any available port.
    context.pj_transport = context.pj_lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))

    context.pj_lib.start()
    context.pj_lib.set_null_snd_dev()

    context.pj_devices = {}


def after_scenario(context, scenario):
    """
    These run after each scenario is run.
    """
    erase(context)

    # Shutdown the library.
    context.pj_transport = None

    for acc in context.pj_devices.values():
        acc.delete()

    context.pj_lib.destroy()
    context.pj_lib = None
