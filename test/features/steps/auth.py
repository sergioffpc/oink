import hashlib
import http.client
import json

from steps.config import config_env


def authenticate():
    headers = {"Content-type": "application/json"}

    username = config_env['username']
    password = config_env['password']
    credentials = hashlib.md5(f"{username}:{password}".encode('utf-8')).hexdigest()
    body = json.dumps({
        "data": {
            "credentials": credentials,
            "account_name": config_env['account_name']
        }
    })

    conn = http.client.HTTPConnection(config_env['host'], config_env['port'])
    conn.request("PUT", "/v2/user_auth", body, headers)
    response = conn.getresponse()

    return json.loads(response.read())
