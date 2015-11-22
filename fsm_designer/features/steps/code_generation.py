
from behave import given, when, then
from pkg_resources import resource_filename

import os
import tempfile
import shutil

from contextlib import contextmanager

import fsm_designer.cli


@contextmanager
def cd(directory):
    current_directory = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(current_directory)


@given(u'a fsm design')
def step_impl1(context):
    context.design = os.path.abspath(resource_filename('fsm_designer', '../features/steps/designs/simple.yml'))


@when(u'generating code')
def step_impl2(context):
    context.tempdir = tempfile.mkdtemp()
    try:
        with cd(context.tempdir):
            fsm_designer.cli.main('generate {0} output.py'.format(context.design).split())
            assert os.path.exists('output.py'), 'No code generated'
            with open('output.py') as f:
                context.generated_code = f.read()
    except SystemExit:
        raise AssertionError('SystemExit')


class Module(object):

    pass


@then(u'the code for an FSM should be generated in a python module')
def step_impl3(context):
    module = Module()
    exec context.generated_code in module.__dict__
    assert module.S0
    assert module.S1
    assert module.S0.hello
    assert module.S0.hello.state_transitions
    assert module.S0.hello.state_transitions == ['S1']
