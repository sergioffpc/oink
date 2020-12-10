Feature: MP-1 - PHONE CALL

  @integration
  Scenario: phone call
    Given an account for realm "pigsty.stg.uc.talkdesk.com"
      And an user with name "lilly" and extension "3000" for realm "pigsty.stg.uc.talkdesk.com"
      And a device with username "lilly-dev-0", password "******" for user "lilly" on realm "pigsty.stg.uc.talkdesk.com"
      And an user with name "ziggy" and extension "3001" for realm "pigsty.stg.uc.talkdesk.com"
      And a device with username "ziggy-dev-0", password "******" for user "ziggy" on realm "pigsty.stg.uc.talkdesk.com"


    When we register a device with username "lilly-dev-0" and password "******" on realm "pigsty.stg.uc.talkdesk.com"
     And we register a device with username "ziggy-dev-0" and password "******" on realm "pigsty.stg.uc.talkdesk.com"
     And "sip:lilly-dev-0@pigsty.stg.uc.talkdesk.com" makes a call to "sip:3001@pigsty.stg.uc.talkdesk.com" tagged as "call-0"
      | header_name      | header_value |
      | X-Lilly-Greeting | oink, oink   |
      | X-Ziggy-Greeting | snort, snort |
     And accepts the call tagged as "call-0"
     And wait for 5 seconds
     And "a" leg channel from call tagged as "call-0" on realm "pigsty.stg.uc.talkdesk.com" must have the following attributes
      | answered | destination | call_direction |
      | True     | 3001        | inbound        |
     And "b" leg hangs up the call tagged as "call-0"


    Then call record detail from call tagged as "call-0" on realm "pigsty.stg.uc.talkdesk.com" must have the following attributes
      | caller_id_number | callee_id_number | hangup_cause    |
      | 3000             | 3001             | NORMAL_CLEARING |
