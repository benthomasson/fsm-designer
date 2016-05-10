
from behave import when, then
from code_generation import cd
import fsm_designer.cli
import os

HERE = os.path.dirname(__file__)


@given(u'two empty fsm designs')
def step_impl(context):
    context.designA = os.path.join(HERE, 'X')
    context.designB = os.path.join(HERE, 'Y')

@given(u'two simple fsm designs')
def step_impl(context):
    context.designA = os.path.join(HERE, 'x.yml')
    context.designB = os.path.join(HERE, 'y.yml')

@given(u'two different fsm designs')
def step_impl(context):
    context.designA = os.path.join(HERE, 'x.yml')
    context.designB = os.path.join(HERE, 'x2.yml')

@given(u'two fsm designs with different transitions')
def step_impl(context):
    context.designA = os.path.join(HERE, 'x.yml')
    context.designB = os.path.join(HERE, 'x3.yml')


@when(u'finding differences')
def step_impl(context):
    try:
        with cd(context.tempdir):
            context.result = fsm_designer.cli.main('diff {0} {1}'.format(context.designA, context.designB).split())
    except SystemExit, e:
        print(dir(e))
        print(e.code)
        print(e.message)
        print(e.args)
        raise AssertionError('SystemExit')


@then(u'their should be no differences between the designs.')
def step_impl(context):
    assert context.result is 0


@then(u'their should be differences between the designs.')
def step_impl(context):
    assert context.result is 1
