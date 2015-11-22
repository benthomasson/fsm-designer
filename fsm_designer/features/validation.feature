Feature: Code Validation
    In order to improve code quality
    As a developer
    I want to validate the implemenation code for a finite state machine using the FSM design diagram.

    Scenario: Validate Python code from a FSM design
        Given a fsm design
        When validating code
        Then the code for an FSM should be checked against the FSM design

