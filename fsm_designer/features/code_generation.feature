Feature: Code Generation
    In order to improve developer productivity
    As a developer
    I want to generate the code for a finite state machine from the FSM design diagram.

    Scenario: Generate Python code from a FSM design
        Given a fsm design
        When generating code
        Then the code for an FSM should be generated in a python module

