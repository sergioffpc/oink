Feature: MP-2 - TRACE REGISTER FLOW

  @wip
  Scenario: trace register flow
    #
    # Prepare the test environment.
    #
    Given an account for realm "pigsty.sip.integration.tests"
      And an user with name "lilly" and extension "3000" for realm "pigsty.sip.integration.tests"
      And a device with username "lilly-dev-0", password "******" for user "lilly" on realm "pigsty.sip.integration.tests"


    #
    # Starts a new SIP transaction and sends a REGISTER SIP message.  It's expected to receive a 401 Unauthorized
    # response message with a 'nonce' parameter to compute the digest 'response'.
    #
    When UAC agent starts a new transaction
     And UAC agent sends the message
      """
      REGISTER sip:pigsty.sip.integration.tests SIP/2.0
      Via: SIP/2.0/UDP [local_ip]:[local_port];rport;branch=[branch]
      Route: <sip:[remote_ip]:[remote_port];lr>
      Max-Forwards: 70
      From: <sip:lilly-dev-0@pigsty.sip.integration.tests>;tag=[tag]
      To: <sip:lilly-dev-0@pigsty.sip.integration.tests>
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      User-Agent: pjsip python
      Contact: <sip:lilly-dev-0@[local_ip]:[local_port];ob>
      Expires: 300
      Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS
      Content-Length:  0
      """
    Then UAC agent must receive a message
      """
      SIP/2.0 401 Unauthorized
      Via: SIP/2.0/UDP [local_ip]:[local_port];rport=[local_port];branch=[branch];received=[local_ip]
      From: <sip:lilly-dev-0@pigsty.sip.integration.tests>;tag=[tag]
      To: <sip:lilly-dev-0@pigsty.sip.integration.tests>;tag=.*
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      WWW-Authenticate: Digest realm="pigsty.sip.integration.tests", nonce=".*"
      Content-Length: 0
      """


    #
    # With the 'nonce' parameter we can now resend the REGISTER SIP message with the proper 'authorization'
    # headers filled.
    #
    When UAC agent starts a new transaction
     And UAC agent sends the message
      """
      REGISTER sip:pigsty.sip.integration.tests SIP/2.0
      Via: SIP/2.0/UDP [local_ip]:[local_port];rport;branch=[branch]
      Route: <sip:[remote_ip]:[remote_port];lr>
      Max-Forwards: 70
      From: <sip:lilly-dev-0@pigsty.sip.integration.tests>;tag=[tag]
      To: <sip:lilly-dev-0@pigsty.sip.integration.tests>
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      User-Agent: pjsip python
      Contact: <sip:lilly-dev-0@[local_ip]:[local_port];ob>
      Expires: 300
      Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS
      Authorization: Digest username="lilly-dev-0", realm="pigsty.sip.integration.tests", nonce=`last.headers['www-authenticate'][0]['nonce']`, uri="sip:pigsty.sip.integration.tests", response=`response(last, '******')`
      Content-Length:  0
      """
    # Here we are lazy and only validates the first line SIP message response.
    Then UAC agent must receive a message
      """
      SIP/2.0 100 checking your credentials
      """
     And UAC agent must receive a message
      """
      SIP/2.0 200 OK
      Via: SIP/2.0/UDP [local_ip]:[local_port];rport=[local_port];branch=[branch];received=[local_ip]
      From: <sip:lilly-dev-0@pigsty.sip.integration.tests>;tag=[tag]
      To: <sip:lilly-dev-0@pigsty.sip.integration.tests>;tag=.*
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      Contact: <sip:lilly-dev-0@[local_ip]:[local_port];ob>;expires=300
      Supported: outbound
      Content-Length: 0
      """
