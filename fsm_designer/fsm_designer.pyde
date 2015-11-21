

from fsm import State, transition, to_yaml, singleton, validate_design, generate_code

import yaml

from conf import settings as conf_settings
from widgets import arrow, Wheel

import os
import sys
import traceback
import itertools
import random
import logging

from math import sqrt, pi

logger = logging.getLogger("fsm_designer")


page_width = 1024
page_height = 768

application = None


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

    def mouseDragged(self, controller):
        if mouseButton == LEFT and controller.lastKeyCode == ALT:
            controller.scaleXY = max(0.1, (mouseY - controller.mousePressedY) / 100.0 + controller.oldScaleXY)
            controller.panX = controller.oldPanX + (-1 * controller.mousePressedX / controller.oldScaleXY) + (controller.mousePressedX / controller.scaleXY)
            controller.panY = controller.oldPanY + (-1 * controller.mousePressedY / controller.oldScaleXY) + (controller.mousePressedY / controller.scaleXY)
        elif mouseButton == LEFT:
            controller.panX = (mouseX - controller.mousePressedX) / controller.scaleXY + controller.oldPanX
            controller.panY = (mouseY - controller.mousePressedY) / controller.scaleXY + controller.oldPanY

    @transition('Ready')
    def mouseReleased(self, controller):
        controller.lastKeyCode = 0
        controller.changeState(Ready)

    def keyPressed(self, controller):
        controller.lastKeyCode = keyCode

    def keyReleased(self, controller):
        controller.lastKeyCode = 0


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
                for state_d in d.get('states', []):
                    label = state_d.get('label') or "S{0}".format(next(controller.state_sequence))
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
            logging.info("Read from {0}".format(selection))
            controller.changeState(Ready)
        except Exception:
            logging.error(traceback.format_exc())


@singleton
class Save(BaseState):

    def start(self, controller):
        selectOutput("Output file", "fileSelected")

    @transition('Ready')
    def fileSelected(self, controller, selection):
        try:
            if selection:
                app = {}
                app['app'] = os.path.splitext(os.path.basename(selection.getAbsolutePath()))[0]
                app['view'] = dict(panX=controller.panX, panY=controller.panY, scaleXY=controller.scaleXY)
                app['states'] = [s.to_dict() for s in controller.states]
                app['transitions'] = [t.to_dict() for t in controller.transitions]
                with open(selection.getAbsolutePath(), 'w') as f:
                    f.write(yaml.safe_dump(app, default_flow_style=False))
            logging.info("Wrote to {0}".format(selection))
            controller.changeState(Ready)
        except Exception:
            logging.error(traceback.format_exc())


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


class FSMState(object):

    def __init__(self, **kwargs):
        self.x = 0
        self.y = 0
        self.label = ""
        self.size = 100
        self.color = 255
        self.selected = False
        self.edit = False
        self.label_offset = 0
        self.__dict__.update(kwargs)

    def to_dict(self):
        d = {}
        d['label'] = self.label
        d['x'] = self.x
        d['y'] = self.y
        d['color'] = self.color
        d['size'] = self.size
        return d

    def draw(self, controller):
        stroke(0)
        fill(self.color)
        ellipse(self.x, self.y, self.size, self.size)
        if self.selected:
            strokeWeight(2)
            noFill()
            stroke(conf_settings.SELECTED_COLOR)
            ellipse(self.x, self.y, self.size+6, self.size+6)
        fill(0)
        if self.edit:
            text(self.label + "_", self.x - textWidth(self.label + "_")/2, self.y)
        else:
            text(self.label, self.x - textWidth(self.label)/2, self.y)

    def is_selected(self, controller):
        return (controller.mousePX - self.x)**2 + (controller.mousePY - self.y)**2 < (self.size/2)**2


class FSMTransition(object):

    def __init__(self, **kwargs):
        self.from_state = None
        self.to_state = None
        self.label = ""
        self.selected = False
        self.edit = False
        self.__dict__.update(kwargs)

    def to_dict(self):
        d = {}
        d['label'] = self.label
        d['to_state'] = self.to_state.label
        d['from_state'] = self.from_state.label
        return d

    def is_selected(self, controller):
        x1 = self.from_state.x
        y1 = self.from_state.y
        x2 = self.to_state.x
        y2 = self.to_state.y
        x = controller.mousePX
        y = controller.mousePY

        dx = x2 - x1
        dy = y2 - y1

        d = sqrt(dx*dx + dy*dy)

        if d == 0:
            return False

        ca = dx/d
        sa = dy/d

        mX = (-x1+x)*ca + (-y1+y)*sa

        if mX <= 0:
            result_x = x1
            result_y = y1
        elif mX >= d:
            result_x = x2
            result_y = y2
        else:
            result_x = x1 + mX*ca
            result_y = y1 + mX*sa

        dx = x - result_x
        dy = y - result_y
        distance = sqrt(dx*dx + dy*dy)
        line_atan = atan2(y2-y1, x2-x1)
        pline_atan = atan2(result_y-y, result_x-x)
        if application.debug:
            logger.debug("%s %s", line_atan, pline_atan)
            if abs(line_atan) < pi/2.0 and pline_atan < 0:
                stroke(0)
            elif abs(line_atan) > pi/2.0 and pline_atan < 0:
                stroke(255)
            elif abs(line_atan) > pi/2.0 and pline_atan > 0:
                stroke(0)
            else:
                stroke(255)
            line(x, y, result_x, result_y)
        if abs(line_atan) < pi/2.0 and pline_atan < 0:
            selected_distance = 10
        elif abs(line_atan) > pi/2.0 and pline_atan < 0:
            selected_distance = 10 + conf_settings.TEXT_SIZE * (self.label_offset + 1.5)
        elif abs(line_atan) > pi/2.0 and pline_atan > 0:
            selected_distance = 10
        else:
            selected_distance = 10 + conf_settings.TEXT_SIZE * (self.label_offset + 1.5)
        if distance < selected_distance:
            if application.debug:
                stroke(conf_settings.SELECTED_COLOR)
                line(x, y, result_x, result_y)
            return True
        else:
            return False

    def draw(self, controller):
        self.label_offset = 0
        for t in controller.transitions:
            if t == self:
                break
            if t.to_state == self.to_state and t.from_state == self.from_state:
                self.label_offset += 1
        label = self.label
        if self.edit:
            label = self.label + "_"
        if self.from_state is not None and self.to_state is None:
            arrow(self.from_state.x,
                  self.from_state.y,
                  controller.mousePX,
                  controller.mousePY,
                  0,
                  label,
                  self.selected,
                  self.label_offset)
        if self.from_state is not None and self.to_state is not None:
            arrow(self.from_state.x,
                  self.from_state.y,
                  self.to_state.x,
                  self.to_state.y,
                  self.to_state.size/2,
                  label,
                  self.selected,
                  self.label_offset)


class Application(object):

    def __init__(self):
        self.state_sequence = itertools.count(start=0, step=1)
        self.states = []
        self.transitions = []
        self.panX = 0
        self.panY = 0
        self.oldPanX = 0
        self.oldPanY = 0
        self.scaleXY = 1
        self.oldScaleXY = 0
        self.mousePX = 0
        self.mousePY = 0
        self.mousePressedX = 0
        self.mousePressedY = 0
        self.lastKeyCode = 0
        self.state = None
        self.wheel = None
        self.selected_state = None
        self.selected_transition = None
        self.debug = False

    def changeState(self, state):
        if self.state:
            self.state.end(self)
        self.state = state
        if self.state:
            self.state.start(self)

    def draw(self, controller):
        if self.debug:
            fill(255)
            textSize(conf_settings.TEXT_SIZE)
            xy_t = "xy_t: {0}, {1}".format(mouseX, mouseY)
            text(xy_t,
                 width - 100 - textWidth(xy_t),
                 height - 150)
            xyp_t = "xyp_t: {0}, {1}".format(controller.mousePX, controller.mousePY)
            text(xyp_t,
                 width - 100 - textWidth(xyp_t),
                 height - 130)
            text(self.state.name(),
                 width - 100 - textWidth(self.state.name()),
                 height - 110)
            fps = "fps: {0}".format(int(frameRate))
            text(fps,
                 width - 100 - textWidth(fps),
                 height - 50)
            pan = "pan: {0}, {1}".format(int(controller.panX), int(controller.panY))
            text(pan,
                 width - 100 - textWidth(pan),
                 height - 30)
            scaleXYT = "scale: {0}".format(controller.scaleXY)
            text(scaleXYT,
                 width - 100 - textWidth(scaleXYT),
                 height - 10)
            try:
                key_t = ""
                key_t = "key: {0} keyCode: {1}".format(str(key).strip(), keyCode)
            except Exception:
                pass
            text(key_t,
                 width - 100 - textWidth(key_t),
                 height - 70)
            mouseButton_t = "mouseButton: {0}".format(mouseButton)
            text(mouseButton_t,
                 width - 100 - textWidth(mouseButton_t),
                 height - 90)

        if self.wheel:
            self.wheel.draw()


def validate_self():

    logging.debug("pwd: {0}".format(os.getcwd()))

    with open("current.yml", 'w') as f:
        self_yml = to_yaml(sys.modules[__name__], "fsm_designer")
        f.write(self_yml)

    with open("design.yml") as f:
        design = yaml.load(f.read())
        missing_states, missing_transitions = validate_design(design, sys.modules[__name__], "fsm_designer")
        if missing_states or missing_transitions:
            print "Self validation failed! Example code:"
            print generate_code(missing_states, missing_transitions)


def settings():
    pass


def setup():
    global application
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug logging enabled")
    size(page_width, page_height, FX2D)
    application = Application()
    application.changeState(Start)
    frame.setTitle("FSM Designer")
    frame.setResizable(True)
    frameRate(30)
    validate_self()
    logging.debug("setup completed")


def scale_and_pan():
    scale(application.scaleXY)
    translate(application.panX, application.panY)


def draw():
    application.mousePX = mouseX / application.scaleXY - application.panX
    application.mousePY = mouseY / application.scaleXY - application.panY
    background(102)
    pushMatrix()
    scale_and_pan()
    for t in application.transitions:
        t.draw(application)
    for state in application.states:
        state.draw(application)
    popMatrix()
    application.draw(application)
    scale_and_pan()


def mousePressed():
    application.state.mousePressed(application)


def mouseDragged():
    application.state.mouseDragged(application)


def mouseReleased():
    application.state.mouseReleased(application)


def keyPressed():
    application.state.keyPressed(application)


def keyReleased():
    application.state.keyReleased(application)


def keyTyped():
    application.state.keyTyped(application)


def fileSelected(selection):
    application.state.fileSelected(application, selection)
