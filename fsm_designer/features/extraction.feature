Feature: Design Extraction
    In order to improve developer communication
    As a developer
    I want to extract the FSM design from already written code for a finite state machine.

    Scenario: Generate a FSM design from Python code
        Given a fsm implementation module in Python
        When extracting the design
        Then the FSM design should be generated from the Python code.

