Feature: Design Diff
    In order to improve code quality
    As a developer
    I want to find the differences between the implemenation code for a finite state machine and the FSM design diagram.

    Scenario: Find differences between two empty FSM designs
        Given two empty fsm designs
        When finding differences
        Then their should be no differences between the designs.

    Scenario: Find differences between two simple FSM designs
        Given two simple fsm designs
        When finding differences
        Then their should be no differences between the designs.

    Scenario: Find differences between two different FSM designs
        Given two different fsm designs
        When finding differences
        Then their should be differences between the designs.

    Scenario: Find differences between two different FSM designs
        Given two fsm designs with different transitions
        When finding differences
        Then their should be differences between the designs.
