import httplib
import json
import socket
import threading
import urlparse
import uuid
from random import randint

import pjsua as pj
from hamcrest import assert_that, equal_to

from steps.auth import authenticate


def erase(context):
    auth = authenticate(context)
    auth_token = auth['auth_token']
    headers = {"Content-type": "application/json", "X-Auth-Token": auth_token}

    reseller_id = auth['data']['account_id']

    url = urlparse.urlparse(context.config.userdata['api'])
    if url.scheme == "https":
        conn = httplib.HTTPSConnection(url.hostname, url.port)
    else:
        conn = httplib.HTTPConnection(url.hostname, url.port)
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


def ua_consumer(context):
    while True:
        response, _ = context.ua_sock.recvfrom(8192)

        context.ua_queue_lock.acquire()
        context.ua_queue.append(response)
        context.ua_queue_lock.release()

        if context.ua_exit.is_set():
            break


def before_scenario(context, scenario):
    """
    These run before each scenario is run.
    """
    erase(context)

    # You need to instantiate one and exactly one of this class, and from the instance you
    # can then initialize and start the library.
    context.pj_lib = pj.Lib()

    # Init library with default config and some customized
    # logging config.
    ua_cfg = pj.UAConfig()
    ua_cfg.max_calls = 16
    context.pj_lib.init(ua_cfg=ua_cfg, log_cfg=pj.LogConfig(level=0, callback=log_cb))

    context.pj_caller_player = context.pj_lib.create_player("features/assets/sounds/caller_snd.wav", True)
    context.pj_callee_player = context.pj_lib.create_player("features/assets/sounds/callee_snd.wav", True)

    # Create UDP transport which listens to any available port.
    context.pj_transport = context.pj_lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))

    context.pj_lib.start()
    context.pj_lib.set_null_snd_dev()

    context.pj_devices = {}

    remote = urlparse.urlsplit('//' + context.config.userdata['proxy'])
    context.ua_dict = {
        'local_ip': socket.gethostbyname(socket.gethostname()),
        'local_port': randint(49152, 65535),
        'remote_ip': remote.hostname,
        'remote_port': remote.port,
        'cseq': randint(1, 65535),
        'call_id': uuid.uuid4(),
        'user_agent': context.scenario
    }

    context.ua_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    context.ua_sock.bind((context.ua_dict['local_ip'], context.ua_dict['local_port']))

    context.ua_queue = []
    context.ua_queue_lock = threading.Lock()

    context.ua_exit = threading.Event()
    context.ua_thread = threading.Thread(target=ua_consumer, args=(context,))
    context.ua_thread.setDaemon(True)
    context.ua_thread.start()


def after_scenario(context, scenario):
    """
    These run after each scenario is run.
    """
    erase(context)

    context.ua_exit.set()
    context.ua_sock.close()

    # Shutdown the library.
    context.pj_lib.hangup_all()

    context.pj_lib.player_destroy(context.pj_caller_player)
    context.pj_lib.player_destroy(context.pj_callee_player)

    context.pj_transport = None

    for acc in context.pj_devices.values():
        acc.delete()

    context.pj_lib.destroy()
    context.pj_lib = None
