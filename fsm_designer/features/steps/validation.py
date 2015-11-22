
from behave import when, then
from code_generation import cd
import fsm_designer.cli


@when(u'validating code')
def step_impl1(context):
    context.execute_steps(u'when generating code')


@then(u'the code for an FSM should be checked against the FSM design')
def step_impl2(context):
    try:
        with cd(context.tempdir):
            context.result = fsm_designer.cli.main('validate {0} output'.format(context.design).split())
    except SystemExit:
        raise AssertionError('SystemExit')
    assert context.result is 0
