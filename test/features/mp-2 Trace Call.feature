Feature: MP-2 - TRACE REGISTER FLOW

  @wip
  Scenario: trace register flow
    #
    # Prepare the test environment.
    #
    Given an account for realm "pigsty.stg.uc.talkdesk.com"
      And an user with name "lilly" and extension "3000" for realm "pigsty.stg.uc.talkdesk.com"
      And a device with username "lilly-dev-0", password "******" for user "lilly" on realm "pigsty.stg.uc.talkdesk.com"
      And the following UAC agent variables
        | variable  | value                      |
        | user      | lilly-dev-0                |
        | realm     | pigsty.stg.uc.talkdesk.com |


    #
    # Starts a new SIP transaction and sends a REGISTER SIP message.  It's expected to receive a 401 Unauthorized
    # response message with a 'nonce' parameter to compute the digest 'response'.
    #
    When UAC agent starts a new transaction
     And UAC agent sends the message
      """
      REGISTER sip:[realm] SIP/2.0
      Via: SIP/2.0/UDP [local_ip]:[local_port];rport;branch=[branch]
      Route: <sip:[remote_ip]:[remote_port];lr>
      Max-Forwards: 70
      From: <sip:[user]@[realm]>;tag=[tag]
      To: <sip:[user]@[realm]>
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      User-Agent: [user_agent]
      Contact: <sip:[user]@[local_ip]:[local_port];ob>
      Expires: 300
      Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS
      Content-Length:  0
      """
    Then UAC agent must receive a message
      """
      SIP/2.0 401 Unauthorized
      From: <sip:[user]@[realm]>;tag=[tag]
      To: <sip:[user]@[realm]>;tag=.*
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      Contact: <sip:[user]@[local_ip]:[local_port];ob>
      WWW-Authenticate: Digest realm="[realm]",nonce=.*,algorithm=MD5
      Via: SIP/2.0/UDP [local_ip]:[local_port];received=.*;rport=.*;branch=[branch]
      Content-Length: 0
      """
      And evaluate expression "last.headers['www-authenticate'][0]['nonce']" to variable "nonce"
      And evaluate expression "last.headers['via'][0]['params']['received']" to variable "translated_ip"
      And evaluate expression "last.headers['via'][0]['params']['rport']" to variable "translated_port"


    #
    # With the 'nonce' parameter we can now resend the REGISTER SIP message with the proper 'authorization'
    # headers filled.
    #
    When UAC agent starts a new transaction
     And UAC agent sends the message
      """
      REGISTER sip:[realm] SIP/2.0
      Via: SIP/2.0/UDP [translated_ip]:[translated_port];rport;branch=[branch]
      Route: <sip:[remote_ip]:[remote_port];lr>
      Max-Forwards: 70
      From: <sip:[user]@[realm]>;tag=[tag]
      To: <sip:[user]@[realm]>
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      User-Agent: [user_agent]
      Contact: <sip:[user]@[translated_ip]:[translated_port];ob>
      Expires: 300
      Allow: PRACK, INVITE, ACK, BYE, CANCEL, UPDATE, INFO, SUBSCRIBE, NOTIFY, REFER, MESSAGE, OPTIONS
      Authorization: Digest username="[user]",realm="[realm]",nonce="[nonce]",uri="sip:[realm]",response="`response(last, '******')`",algorithm=MD5
      Content-Length:  0
      """
    Then UAC agent must receive a message
      """
      SIP/2.0 200 OK
      From: <sip:[user]@[realm]>;tag=[tag]
      To: <sip:[user]@[realm]>;tag=.*
      Call-ID: [call_id]
      CSeq: [cseq] REGISTER
      Contact: <sip:[user]@[translated_ip]:[translated_port];ob>;expires=300
      Supported: outbound
      Via: SIP/2.0/UDP [translated_ip]:[translated_port];rport=[translated_port];branch=[branch]
      Content-Length: 0
      """
