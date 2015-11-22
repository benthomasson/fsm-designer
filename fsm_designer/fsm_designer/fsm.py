

import yaml
import inspect
from jinja2 import Environment, PackageLoader
from conf import settings

import logging

logger = logging.getLogger('fsm_designer.fsm')

def singleton(klass):
    return klass()


def transition(new_state):
    def called_on(fn):
        transitions = getattr(fn, 'state_transitions', [])
        if isinstance(new_state, basestring):
            transitions.append(new_state)
        elif isinstance(new_state, State):
            transitions.append(new_state.__class__.__name__)
        else:
            transitions.append(new_state.__name__)
        setattr(fn, 'state_transitions', transitions)
        return fn
    return called_on


class State(object):

    pass


def to_fsm_dict(module, name=None):
    logger.debug("to_fsm_dict %s %s", module, name)
    states = []
    transitions = []
    fsm = dict(name=name or module.__name__, states=states, transitions=transitions)
    for key in dir(module):
        value = getattr(module, key)
        logger.debug("key %s", key)
        logger.debug("isinstance State %s",  isinstance(value, State))
        if isinstance(value, State):
            state_class = value.__class__
        elif type(value) == type and issubclass(value, State) and value is not State:
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


def to_yaml(module, name=None):
    fsm = to_fsm_dict(module, name)
    return yaml.dump(fsm, default_flow_style=False)


def validate_design(design, module, name=None):
    actual = to_fsm_dict(module, name)
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


def analyze_code(module):
    pass


def generate_code(missing_states, missing_transitions):

    code = "from fsm_designer.fsm import singleton, transition, State"
    env = Environment(loader=PackageLoader(settings.CODE_TEMPLATE[0], 'templates'))

    for state in missing_states:
        state_missing_transitions = [dict(x) for x in missing_transitions if dict(x).get('from_state') == state]
        functions = dict()
        for t in state_missing_transitions:
            transitions = functions.get(t['label'], [])
            transitions.append(t)
            functions[t['label']] = transitions
        template = env.get_template(settings.CODE_TEMPLATE[1])
        code += template.render(state=state, functions=functions.iteritems())

    return code
