
import os
import random
import traceback
import logging
import yaml

from fsm_designer.widgets import Wheel, MagnifyingGlassMousePointer, MoveMousePointer
from fsm_designer.models import FSMState, FSMTransition
from conf import settings


logger = logging.getLogger("fsm_designer.design_fsm")


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


class BaseState(State):

    def name(self):
        return self.__class__.__name__

    def start(self, controller):
        pass

    def end(self, controller):
        pass

    def mousePressed(self, controller):
        pass

    def mouseReleased(self, controller):
        pass

    def mouseDragged(self, controller):
        pass

    def keyPressed(self, controller):
        pass

    def keyReleased(self, controller):
        pass

    def keyTyped(self, controller):
        pass

    def fileSelected(self, controller, selected):
        pass


def select_item(controller):
    controller.selected_state = None
    for state in controller.states:
        if state.is_selected(controller) and controller.selected_state is None:
            state.selected = True
            controller.selected_state = state
        else:
            state.selected = False
    controller.selected_transition = None
    for t in controller.transitions:
        if t.is_selected(controller) and controller.selected_transition is None and controller.selected_state is None:
            t.selected = True
            controller.selected_transition = t
        else:
            t.selected = False


@singleton
class Start(BaseState):

    @transition('Ready')
    def start(self, controller):
        controller.changeState(Ready)


@singleton
class Ready(BaseState):

    @transition('MenuWheel')
    @transition('ScaleAndPan')
    @transition('Selected')
    @transition('SelectedTransition')
    def mousePressed(self, controller):
        if mouseButton == RIGHT:
            controller.changeState(MenuWheel)

        elif mouseButton == LEFT:
            select_item(controller)
            if controller.selected_state is not None:
                controller.changeState(Selected)
            elif controller.selected_transition is not None:
                controller.changeState(SelectedTransition)
            else:
                controller.changeState(ScaleAndPan)

    def keyPressed(self, controller):
        controller.lastKeyCode = keyCode

    def keyTyped(self, controller):
        if key == CODED:
            pass
        elif key == "d":
            controller.debug = not controller.debug


@singleton
class SelectedTransition(BaseState):

    @transition('EditTransition')
    @transition('MenuWheel')
    @transition('Ready')
    def mousePressed(self, controller):
        if mouseButton == RIGHT:
            if controller.selected_transition.is_selected(controller):
                controller.changeState(EditTransition)
            else:
                controller.selected_transition.selected = False
                controller.selected_transition = None
                controller.changeState(MenuWheel)
        elif mouseButton == LEFT:
            if controller.selected_transition.is_selected(controller):
                pass
            else:
                controller.changeState(Ready)
                controller.state.mousePressed(controller)

    @transition('Ready')
    def keyReleased(self, controller):
        if keyCode == 8:
            controller.selected_transition.selected = False
            controller.transitions.remove(controller.selected_transition)
            controller.changeState(Ready)


@singleton
class EditTransition(BaseState):

    def start(self, controller):
        controller.selected_transition.edit = True

    def end(self, controller):
        controller.selected_transition.edit = False

    @transition('SelectedTransition')
    @transition('Ready')
    def mousePressed(self, controller):
        if controller.selected_transition.is_selected(controller):
            controller.changeState(SelectedTransition)
            controller.state.mousePressed(controller)
        else:
            controller.changeState(Ready)
            controller.state.mousePressed(controller)

    def keyReleased(self, controller):
        if keyCode == 8:
            controller.selected_transition.label = controller.selected_transition.label[:-1]

    @transition('SelectedTransition')
    def keyTyped(self, controller):
        if key == CODED:
            if keyCode == 8:
                controller.selected_transition.label = controller.selected_transition.label[:-1]
        else:
            if key == RETURN:
                controller.changeState(SelectedTransition)
            elif key == ENTER:
                controller.changeState(SelectedTransition)
            elif key == BACKSPACE:
                controller.selected_transition.label = controller.selected_transition.label[:-1]
            elif key == DELETE:
                controller.selected_transition.label = controller.selected_transition.label[:-1]
            else:
                controller.selected_transition.label += key


@singleton
class Selected(BaseState):

    @transition('MenuWheel')
    @transition('Edit')
    @transition('Ready')
    @transition('Move')
    def mousePressed(self, controller):
        if mouseButton == RIGHT:
            if controller.selected_state.is_selected(controller):
                controller.changeState(Edit)
            else:
                controller.selected_state.selected = False
                controller.selected_state = None
                controller.changeState(MenuWheel)
        elif mouseButton == LEFT:
            if controller.selected_state.is_selected(controller):
                controller.changeState(Move)
            else:
                controller.changeState(Ready)
                controller.state.mousePressed(controller)

    @transition('Move')
    @transition('NewTransition')
    def mouseDragged(self, controller):
        if mouseButton == LEFT:
            controller.changeState(Move)
            controller.state.mouseDragged(controller)
        if mouseButton == RIGHT:
            controller.changeState(NewTransition)
            controller.state.mouseDragged(controller)

    @transition('Ready')
    def keyReleased(self, controller):
        if keyCode == 8:
            controller.selected_state.selected = False
            controller.states.remove(controller.selected_state)
            for t in controller.transitions[:]:
                if t.to_state == controller.selected_state or t.from_state == controller.selected_state:
                    controller.transitions.remove(t)
            controller.selected_state = None
            controller.changeState(Ready)


@singleton
class NewTransition(BaseState):

    def start(self, controller):
        new_transition = FSMTransition(from_state=controller.selected_state, selected=True)
        controller.transitions.append(new_transition)
        controller.selected_transition = new_transition

    def end(self, controller):
        if controller.selected_transition is not None and controller.selected_transition.to_state is None:
            controller.transitions.remove(controller.selected_transition)
        controller.selected_transition.selected = False
        controller.selected_transition = None

    @transition('Selected')
    def mouseReleased(self, controller):
        for state in controller.states:
            if state == controller.selected_state:
                continue
            if state.is_selected(controller):
                controller.selected_transition.to_state = state
                break
        controller.changeState(Selected)


@singleton
class Move(BaseState):

    def mouseDragged(self, controller):
        controller.selected_state.x = controller.mousePX
        controller.selected_state.y = controller.mousePY

    @transition('Selected')
    def mouseReleased(self, controller):
        controller.changeState(Selected)


@singleton
class Edit(BaseState):

    def start(self, controller):
        controller.selected_state.edit = True

    def end(self, controller):
        controller.selected_state.edit = False

    @transition('NewTransition')
    def mouseDragged(self, controller):
        if mouseButton == RIGHT:
            controller.changeState(NewTransition)
            controller.state.mouseDragged(controller)

    @transition('Selected')
    @transition('Ready')
    def mousePressed(self, controller):
        if controller.selected_state.is_selected(controller):
            controller.changeState(Selected)
            controller.state.mousePressed(controller)
        else:
            controller.changeState(Ready)
            controller.state.mousePressed(controller)

    def keyReleased(self, controller):
        if keyCode == 8:
            controller.selected_state.label = controller.selected_state.label[:-1]

    @transition('Selected')
    def keyTyped(self, controller):
        if key == CODED:
            if keyCode == 8:
                controller.selected_state.label = controller.selected_state.label[:-1]
        else:
            if key == RETURN:
                controller.changeState(Selected)
            elif key == ENTER:
                controller.changeState(Selected)
            elif key == BACKSPACE:
                controller.selected_state.label = controller.selected_state.label[:-1]
            elif key == DELETE:
                controller.selected_state.label = controller.selected_state.label[:-1]
            else:
                controller.selected_state.label += key


@singleton
class ScaleAndPan(BaseState):

    def start(self, controller):
        controller.mousePressedX = mouseX
        controller.mousePressedY = mouseY
        controller.oldPanX = controller.panX
        controller.oldPanY = controller.panY
        controller.oldScaleXY = controller.scaleXY
        if controller.lastKeyCode == ALT:
            controller.mouse_pointer = MagnifyingGlassMousePointer()
        else:
            controller.mouse_pointer = MoveMousePointer()

    def end(self, controller):
        controller.mouse_pointer = None

    def mouseDragged(self, controller):
        if mouseButton == LEFT and controller.lastKeyCode == ALT:
            controller.scaleXY = max(0.1, (controller.mousePressedY - mouseY) / 100.0 + controller.oldScaleXY)
            controller.panX = controller.oldPanX + (-1 * controller.mousePressedX / controller.oldScaleXY) + (controller.mousePressedX / controller.scaleXY)
            controller.panY = controller.oldPanY + (-1 * controller.mousePressedY / controller.oldScaleXY) + (controller.mousePressedY / controller.scaleXY)
        elif mouseButton == LEFT:
            controller.panX = (mouseX - controller.mousePressedX) / controller.scaleXY + controller.oldPanX
            controller.panY = (mouseY - controller.mousePressedY) / controller.scaleXY + controller.oldPanY

    @transition('Ready')
    def mouseReleased(self, controller):
        controller.lastKeyCode = 0
        controller.mouse_pointer = None
        controller.changeState(Ready)

    def keyPressed(self, controller):
        controller.lastKeyCode = keyCode
        if controller.lastKeyCode == ALT:
            controller.mouse_pointer = MagnifyingGlassMousePointer()

    def keyReleased(self, controller):
        controller.lastKeyCode = 0
        controller.mouse_pointer = MoveMousePointer()


@singleton
class Load(BaseState):

    def start(self, controller):
        selectInput("Input file", "fileSelected")

    @transition('Ready')
    def fileSelected(self, controller, selection):
        try:
            if selection:
                new_states = []
                new_transitions = []
                with open(selection.getAbsolutePath()) as f:
                    d = yaml.load(f.read())
                controller.model = selection.getAbsolutePath()
                controller.app = d.get('app', os.path.splitext(os.path.basename(selection.getAbsolutePath()))[0])
                controller.directory = os.path.dirname(selection.getAbsolutePath())
                for state_d in d.get('states', []):
                    label = state_d.get('label') or "S{0}".format(next(controller.state_sequence))
                    textSize(settings.TEXT_SIZE)
                    state = FSMState(label=label,
                                     x=state_d.get('x', random.randrange(int(controller.panX), int(width*controller.scaleXY + controller.panX))),
                                     y=state_d.get('y', random.randrange(int(controller.panY), int(height*controller.scaleXY + controller.panY))),
                                     color=state_d.get('color', 255),
                                     size=state_d.get('size', max(100, textWidth(label) + 20)))
                    new_states.append(state)
                for transition_d in d.get('transitions', []):
                    from_state = [s for s in new_states if s.label == transition_d['from_state']]
                    to_state = [s for s in new_states if s.label == transition_d['to_state']]
                    assert len(from_state) == 1, str(from_state)
                    assert len(to_state) == 1, str(to_state)
                    t = FSMTransition(label=transition_d.get('label', ''),
                                      to_state=to_state[0],
                                      from_state=from_state[0])
                    new_transitions.append(t)
                view_d = d.get('view', {})
                controller.panX = view_d.get('panX', 0)
                controller.panY = view_d.get('panY', 0)
                controller.scaleXY = view_d.get('scaleXY', 1)
                controller.states = new_states
                controller.transitions = new_transitions
            logger.info("Read from {0}".format(selection))
            controller.changeState(Ready)
        except Exception:
            logger.error(traceback.format_exc())


@singleton
class Save(BaseState):

    def start(self, controller):
        selectOutput("Output file", "fileSelected")

    @transition('Ready')
    def fileSelected(self, controller, selection):
        try:
            if selection:
                app = {}
                app['app'] = controller.app or os.path.splitext(os.path.basename(selection.getAbsolutePath()))[0]
                app['view'] = dict(panX=controller.panX, panY=controller.panY, scaleXY=controller.scaleXY)
                app['states'] = [s.to_dict() for s in controller.states]
                app['transitions'] = [t.to_dict() for t in controller.transitions]
                with open(selection.getAbsolutePath(), 'w') as f:
                    f.write(yaml.safe_dump(app, default_flow_style=False))
            logger.info("Wrote to {0}".format(selection))
            controller.changeState(Ready)
        except Exception:
            logger.error(traceback.format_exc())


@singleton
class NewState(BaseState):

    @transition(Ready)
    def start(self, controller):
        s = FSMState(label="S{0}".format(next(controller.state_sequence)), x=controller.mousePX, y=controller.mousePY)
        controller.states.append(s)
        controller.changeState(Ready)


@singleton
class MenuWheel(BaseState):

    def start(self, controller):
        controller.wheel = Wheel(mouseX, mouseY)

    def end(self, controller):
        controller.wheel = None

    @transition(Ready)
    @transition('Save')
    @transition('Load')
    @transition('NewState')
    def mouseReleased(self, controller):
        menu_selection = controller.wheel.get_menu_selection()
        if menu_selection == "New":
            controller.changeState(NewState)
        elif menu_selection == "Save":
            controller.changeState(Save)
        elif menu_selection == "Load":
            controller.changeState(Load)
        else:
            controller.changeState(Ready)
