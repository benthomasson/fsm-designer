

import jinja2
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


def to_fsm_dict(module, name=None):
    states = []
    transitions = []
    fsm = dict(name=name or module.__name__, states=states, transitions=transitions)
    for key in dir(module):
        value = getattr(module, key)
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
    return fsm


def to_yaml(module, name=None):
    fsm = to_fsm_dict(module, name)
    return yaml.dump(fsm, default_flow_style=False)


def validate_design(design, module, name=None):
    actual = to_fsm_dict(module, name)
    design_states = set([s.get('label', '') for s in design.get('states', [])])
    actual_states = set([s.get('label', '') for s in actual.get('states', [])])
    missing_states = design_states - actual_states
    design_transitions = set([tuple(s.items()) for s in design.get('transitions', [])])
    actual_transitions = set([tuple(s.items()) for s in actual.get('transitions', [])])
    missing_transitions = design_transitions - actual_transitions

    return missing_states, missing_transitions


def generate_code(missing_states, missing_transitions):

    code = "from fsm import singleton, transition, State"

    for state in missing_states:
        state_missing_transitions = [dict(x) for x in missing_transitions if dict(x).get('from_state') == state]
        functions = dict()
        for t in state_missing_transitions:
            transitions = functions.get(t['label'], [])
            transitions.append(t)
            functions[t['label']] = transitions
        code += jinja2.Template("""\


@singleton
class {{state}}(State):
    {%for f_name, transitions in functions %}{%for t in transitions%}
    @transition('{{t.to_state}}'){%endfor%}
    def {{f_name}}(self, controller):
        {%for t in transitions-%}
        controller.changeState({{t.to_state}})
        {%endfor%}{%else%}pass
    {%endfor%}
""").render(state=state, functions=functions.iteritems())

    return code
