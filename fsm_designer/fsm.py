

import yaml
import inspect


def transition(new_state):
    def called_on(fn):
        transitions = getattr(fn, 'state_transitions', [])
        if isinstance(new_state, basestring):
            transitions.append(new_state)
        else:
            transitions.append(new_state.__name__)
        setattr(fn, 'state_transitions', transitions)
        return fn
    return called_on


class State(object):

    pass



def to_yaml(module=None):
    states = []
    app = dict(name=module.__name__, states=states)
    for key in dir(module):
        value = getattr(module, key)
        if type(value) == type and issubclass(value, State) and value is not State:
            transitions = []
            state = dict(name=value.__name__, transitions=transitions)
            states.append(state)
            for name, fn in inspect.getmembers(value):
                if hasattr(fn, 'state_transitions'):
                    transitions.extend(getattr(fn, 'state_transitions'))
    return yaml.dump(app, default_flow_style=False)





