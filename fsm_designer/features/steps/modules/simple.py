

def singleton(klass):
    return klass()


def transition(new_state):
    def called_on(fn):
        transitions = getattr(fn, 'state_transitions', [])
        if isinstance(new_state, basestring):
            transitions.append(new_state)
        elif isinstance(new_state, type):
            transitions.append(new_state.__name__)
        elif isinstance(type(new_state), type):
            transitions.append(new_state.__class__.__name__)
        else:
            raise Exception('Unsupported type {0}'.format(new_state))
        setattr(fn, 'state_transitions', transitions)
        return fn
    return called_on


class State(object):

    def start(self, controller):
        pass

    def end(self, controller):
        pass


class Controller(object):

    def __init__(self):
        self.state = None

    def changeState(self, state):
        if self.state:
            self.state.end(self)
        self.state = state
        if self.state:
            self.state.start(self)


@singleton
class S1(State):
    pass


@singleton
class S0(State):

    @transition('S1')
    def hello(self, controller):
        controller.changeState(S1)
