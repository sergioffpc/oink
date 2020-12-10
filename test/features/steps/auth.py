import hashlib
import httplib
import json
import urlparse


def authenticate(context):
    headers = {"Content-type": "application/json"}

    username = context.config.userdata['username']
    password = context.config.userdata['password']
    credentials = hashlib.md5("{}:{}".format(username, password).encode('utf-8')).hexdigest()
    body = json.dumps({
        "data": {
            "credentials": credentials,
            "account_name": context.config.userdata['account_name']
        }
    })

    url = urlparse.urlparse(context.config.userdata['api'])
    if url.scheme == "https":
        conn = httplib.HTTPSConnection(url.hostname, url.port)
    else:
        conn = httplib.HTTPConnection(url.hostname, url.port)
    conn.request("PUT", "/v2/user_auth", body, headers)
    response = conn.getresponse()

    return json.loads(response.read())
