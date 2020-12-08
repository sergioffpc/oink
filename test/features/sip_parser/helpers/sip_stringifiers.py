import re


def stringify_params(params):
    params_str = ""
    for key, val in params.items():
        params_str += ";{}".format(key)
        if val:
            params_str += "={}".format(val)

    return params_str


def stringify_uri(uri):
    if isinstance(uri, str):
        return uri

    uri_str = uri.get("schema", "sip") + ":"
    if uri.get("user"):
        if uri.get("password"):
            uri_str += '{}:{}@'.format(uri["user"], uri["password"])
        else:
            uri_str += '{}@'.format(uri["user"])

    uri_str += uri.get("host")
    if uri.get("port"):
        uri_str += ':{}'.format(uri["port"])

    if uri.get("params"):
        uri_str += stringify_params(uri["params"])

    if uri.get("headers"):
        uri_headers = [key + "=" + str(value) for key, value in uri["headers"].items()]
        if uri_headers:
            uri_str += "?" + "&".join(uri_headers)

    return uri_str


def stringify_version(version):
    return str(version) or "2.0"


def stringify_aor(aor):
    if isinstance(aor, str):
        return aor

    aor_str = '{} <{}>{}'.format(aor.get("name") or "", stringify_uri(aor["uri"]), stringify_params(aor.get("params", {})))
    return aor_str.strip()  # Preferred format as section 7.3.1 of RFC 3261 indicates


def stringify_via(all_via):
    header_strs = []
    for data in all_via:
        if not data.get("host"):
            raise RuntimeError("No host found when stringifiying Via header")

        host_ref = data["host"]
        if data.get("port"):
            host_ref += ":{}".format(data['port'])

        header_strs.append(
            'Via: SIP/{}/{} {}{}'.format(stringify_version(data["version"]), data["protocol"].upper(), host_ref, stringify_params(data["params"]))
        )

    return "\r\n".join(header_strs)


def stringify_to(data):
    return "To: {}".format(stringify_aor(data))


def stringify_from(data):
    return "From: {}".format(stringify_aor(data))


def stringify_contact(data):
    if data == "*" or not data:
        return "Contact: *"

    contacts = ", ".join([stringify_aor(aor) for aor in data])
    return "Contact: {}".format(contacts)


def stringify_route(data):
    routes = ", ".join([stringify_aor(aor) for aor in data])
    return "Route: {}".format(routes)


def stringify_record_route(data):
    record_routes = ", ".join([stringify_aor(aor) for aor in data])
    return "Record-Route: {}".format(record_routes)


def stringify_path(data):
    paths = ", ".join([stringify_aor(aor) for aor in data])
    return "Path: {}".format(paths)


def stringify_cseq(data):
    return 'CSeq: {} {}'.format(data["seq"], data["method"])


def stringify_auth_header_one(name, data):
    params = []

    for param in data:
        if param != "scheme" and data[param]:
            params.append(param + "=" + str(data[param]))

    params_str = ",".join(params)
    if data.get("scheme"):
        return '{}: {} {}'.format(name, data["scheme"], params_str)

    return "{}: {}".format(name, params_str)


def stringify_auth_header_many(name, data_many):
    stringified_headers = []
    for data_one in data_many:
        stringified_headers.append(stringify_auth_header_one(name, data_one))

    return "".join(stringified_headers)


def stringify_refer_to(data):
    return "Refer-To: {}".format(stringify_aor(data))


def prettify_header_name(header_name):
    if header_name == "call-id":
        return "Call-ID"

    return re.sub(r"\b([a-z])", lambda m: m.group(0).upper(), header_name)


def stringify_header(header_name, header_data):
    # First, see if we can transform the header in a simple way, or we
    # don't know what to do with it (has no stringifier)
    if isinstance(header_data, (str, int)) or header_name not in HEADER_STRINGIFIER_FN.keys():
        if isinstance(header_data, (tuple, list)):
            header_data = header_data[0]

        return "{}: {}".format(prettify_header_name(header_name), header_data)

    # Else, call the stringifier function
    fn = HEADER_STRINGIFIER_FN[header_name]
    return fn(header_data)


# Association of header names to stringifier functions
HEADER_STRINGIFIER_FN = {
    "via": stringify_via,
    "to": stringify_to,
    "from": stringify_from,
    "contact": stringify_contact,
    "route": stringify_route,
    "record-route": stringify_record_route,
    "path": stringify_path,
    "cseq": stringify_cseq,
    "www-authenticate": lambda data: stringify_auth_header_many("WWW-Authenticate", data),
    "proxy-authenticate": lambda data: stringify_auth_header_many("Proxy-Authenticate", data),
    "authorization": lambda data: stringify_auth_header_many("Authorization", data),
    "proxy-authorization": lambda data: stringify_auth_header_many("Proxy-Authorization", data),
    "authentication-info": stringify_auth_header_one,
    "refer-to": stringify_refer_to,
}
