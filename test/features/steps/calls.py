from behave import when, then

import pjsua2 as pj


class Account(pj.Account):
    def onRegState(self, prm):
        print(f"registration state: {prm.reason}")


@when(u'"{caller}" calls "{callee}"')
def step_impl(context, caller, callee):
    ep_cfg = pj.EpConfig()
    ep = pj.Endpoint()
    ep.libCreate()
    ep.libInit(ep_cfg)

    sip_tp_config = pj.TransportConfig()
    sip_tp_config.port = 5060
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sip_tp_config)
    ep.libStart()

    cfg = pj.AccountConfig()
    cfg.idUri = f"sip:{caller}@{context.config.userdata['realm']}"
    cfg.regConfig.registrarUri = f"sip:kamailio.oink:5060"

    cred = pj.AuthCredInfo("digest", "*", caller, 0, caller)
    cfg.sipConfig.authCreds.append(cred)

    acc = Account()
    acc.create(cfg)

    ep.libDestroy()


@then(u'call record must have the following attributes')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then call record must have the following attributes')
