Feature: MP-### - DESCRIPTION

  Scenario: phone call
    Given an account with name "pigsty"
    Given an user with name "lilly" and extension "3000" for account "pigsty"
    Given an user with name "ziggy" and extension "3001" for account "pigsty"

    When "lilly" calls "ziggy" during "5s"

    Then call record must have the following attributes
      | caller_id_number | callee_id_number | duration_seconds | hangup_cause    |
      | 3000             | 3001             | 5                | NORMAL_CLEARING |
