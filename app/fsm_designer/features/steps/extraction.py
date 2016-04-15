

from behave import given, when, then
from pkg_resources import resource_filename
import yaml

from code_generation import cd
import fsm_designer.cli

import os


@given(u'a fsm implementation module in Python')
def step_impl(context):
    context.modules = os.path.abspath(resource_filename('fsm_designer', '../features/steps/modules/'))


@when(u'extracting the design')
def step_impl(context):
    context.output = os.path.join(context.tempdir, 'output.yml')
    try:
        with cd(context.modules):
            fsm_designer.cli.main('extract simple {0}'.format(context.output).split())
    except SystemExit:
        raise AssertionError('SystemExit')


@then(u'the FSM design should be generated from the Python code.')
def step_impl(context):
    with open(context.output) as f:
        d = yaml.load(f.read())
    print(d)
    assert d
    assert d['states']
    assert d['transitions']
    assert d['states'] == [{'label': 'S0'}, {'label': 'S1'}]
    assert d['transitions'] == [{'from_state': 'S0', 'to_state': 'S1', 'label': 'hello'}]
