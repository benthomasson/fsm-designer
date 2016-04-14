

import yaml
import inspect
from jinja2 import Environment, PackageLoader
from conf import settings

import logging

logger = logging.getLogger('fsm_designer.fsm')


def to_fsm_dict(module, name=None, state_base_class_name='State'):
    logger.debug("to_fsm_dict %s %s", module, name)
    states = []
    transitions = []
    fsm = dict(app=name or module.__name__, states=states, transitions=transitions)
    state_base_class = getattr(module, state_base_class_name)
    for key in dir(module):
        value = getattr(module, key)
        logger.debug("key %s", key)
        logger.debug("isinstance %s %s", state_base_class, isinstance(value, state_base_class))
        if isinstance(value, state_base_class):
            state_class = value.__class__
        elif type(value) == type and issubclass(value, state_base_class) and value is not state_base_class:
            state_class = value
        else:
            continue
        state = dict(label=state_class.__name__)
        states.append(state)
        for name, fn in inspect.getmembers(state_class):
            if hasattr(fn, 'state_transitions'):
                for destination in getattr(fn, 'state_transitions'):
                    transitions.append(dict(label=name, from_state=state_class.__name__, to_state=destination))
    logger.debug("fsm %s", fsm)
    return fsm


def to_yaml(module, name=None, state_base_class_name='State'):
    fsm = to_fsm_dict(module, name, state_base_class_name)
    return yaml.dump(fsm, default_flow_style=False)


def validate_design(design, module, name=None, state_base_class_name='State'):
    actual = to_fsm_dict(module, name, state_base_class_name)
    design_states = set([s.get('label', '') for s in design.get('states', [])])
    logger.debug("design_states %s", design_states)
    actual_states = set([s.get('label', '') for s in actual.get('states', [])])
    logger.debug("actual_states %s", actual_states)
    missing_states = design_states - actual_states
    logger.debug("missing_states %s", missing_states)
    design_transitions = set([tuple(s.items()) for s in design.get('transitions', [])])
    logger.debug("design_transitions %s", design_transitions)
    actual_transitions = set([tuple(s.items()) for s in actual.get('transitions', [])])
    logger.debug("actual_transitions %s", actual_transitions)
    missing_transitions = design_transitions - actual_transitions
    logger.debug("missing_transitions %s", missing_transitions)
    return missing_states, missing_transitions


def generate_code(code_template, missing_states, missing_transitions):

    env = Environment(loader=PackageLoader(*settings.TEMPLATES_PATH))
    template = env.get_template(code_template)

    states = []
    missing_transitions_copy = missing_transitions.copy()

    for state in missing_states:
        state_missing_transitions = [dict(x) for x in missing_transitions if dict(x).get('from_state') == state]
        for x in missing_transitions:
            if dict(x).get('from_state') == state:
                missing_transitions_copy.remove(x)
        functions = dict()
        for t in state_missing_transitions:
            transitions = functions.get(t['label'], [])
            transitions.append(t)
            functions[t['label']] = transitions
        states.append((state, functions.items()))

    state_missing_transitions = [dict(x) for x in missing_transitions_copy]
    for t in state_missing_transitions:
        functions = dict()
        transitions = functions.get(t['label'], [])
        transitions.append(t)
        functions[t['label']] = transitions
        states.append((t.get('from_state'), functions.items()))

    return template.render(states=states)
