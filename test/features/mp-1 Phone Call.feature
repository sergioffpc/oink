Feature: MP-### - DESCRIPTION

  Scenario: phone call
    Given an account for realm "pigsty.sip.integration.tests"

      And an user with name "lilly" and extension "3000" for realm "pigsty.sip.integration.tests"
      And a device with username "lilly-dev-0", password "******" for user "lilly" on realm "pigsty.sip.integration.tests"

      And an user with name "ziggy" and extension "3001" for realm "pigsty.sip.integration.tests"
      And a device with username "ziggy-dev-0", password "******" for user "ziggy" on realm "pigsty.sip.integration.tests"

    When we register a device with username "lilly-dev-0" and password "******" on realm "pigsty.sip.integration.tests"
     And we register a device with username "ziggy-dev-0" and password "******" on realm "pigsty.sip.integration.tests"

     And "sip:lilly-dev-0@pigsty.sip.integration.tests" makes a call to "sip:3001@pigsty.sip.integration.tests"
      | header_name      | header_value |
      | X-Lilly-Greeting | oink, oink   |
      | X-Ziggy-Greeting | snort, snort |

     And "sip:3001@pigsty.sip.integration.tests" accepts the call from "sip:lilly-dev-0@pigsty.sip.integration.tests"
     And wait for 5 seconds
     And "sip:3001@pigsty.sip.integration.tests" hangs up the call from "sip:lilly-dev-0@pigsty.sip.integration.tests"
#
#    Then the call record detail from realm "pigsty.sip.integration.tests" for call tagged as "call-0" must have the following attributes
#      | caller_id_number | callee_id_number | duration_seconds | hangup_cause    |
#      | 3000             | 3001             | 5                | NORMAL_CLEARING |
