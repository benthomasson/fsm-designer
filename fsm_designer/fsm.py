

import yaml
import inspect


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



def to_yaml(module=None):
    states = []
    app = dict(name=module.__name__, states=states)
    for key in dir(module):
        value = getattr(module, key)
        if isinstance(value, State):
            state_class = value.__class__
        elif type(value) == type and issubclass(value, State) and value is not State:
            state_class = value
        else:
            continue
        transitions = []
        state = dict(name=state_class.__name__, transitions=transitions)
        states.append(state)
        for name, fn in inspect.getmembers(state_class):
            if hasattr(fn, 'state_transitions'):
                for destination in getattr(fn, 'state_transitions'):
                    transitions.append(dict(function=name, destination=destination))
    return yaml.dump(app, default_flow_style=False)





