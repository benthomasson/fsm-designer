

from fsm import State, transition, to_yaml, singleton, validate_design, generate_code

import yaml

import os
import sys
import traceback
import itertools
import random
import logging

from math import sqrt, pi

logger = logging.getLogger("fsm_designer")

state_sequence = itertools.count(start=0, step=1)

states = []
transitions = []
page_width = 1024
page_height = 768
panX = 0
panY = 0
scaleXY = 1.0
oldScaleXY = 0
lastKeyCode = 0
mousePX = mousePY = 0
oldPanX = oldPanY = 0
mousePressedX = mousePressedY = 0
TEXT_SIZE = 12
application = None

SELECTED_COLOR = "#66FFFF"


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
    for state in states:
        if state.is_selected() and controller.selected_state is None:
            state.selected = True
            controller.selected_state = state
        else:
            state.selected = False
    controller.selected_transition = None
    for t in transitions:
        if t.is_selected() and controller.selected_transition is None and controller.selected_state is None:
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
        global lastKeyCode
        lastKeyCode = keyCode

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
            if controller.selected_transition.is_selected():
                controller.changeState(EditTransition)
            else:
                controller.selected_transition.selected = False
                controller.selected_transition = None
                controller.changeState(MenuWheel)
        elif mouseButton == LEFT:
            if controller.selected_transition.is_selected():
                pass
            else:
                controller.changeState(Ready)
                controller.state.mousePressed(controller)

    def keyReleased(self, controller):
        if keyCode == 8:
            controller.selected_transition.selected = False
            transitions.remove(controller.selected_transition)
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
        if controller.selected_transition.is_selected():
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
            if controller.selected_state.is_selected():
                controller.changeState(Edit)
            else:
                controller.selected_state.selected = False
                controller.selected_state = None
                controller.changeState(MenuWheel)
        elif mouseButton == LEFT:
            if controller.selected_state.is_selected():
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
            states.remove(controller.selected_state)
            controller.changeState(Ready)


@singleton
class NewTransition(BaseState):

    def start(self, controller):
        new_transition = FSMTransition(from_state=controller.selected_state, selected=True)
        transitions.append(new_transition)
        controller.selected_transition = new_transition

    def end(self, controller):
        if controller.selected_transition is not None and controller.selected_transition.to_state is None:
            transitions.remove(controller.selected_transition)
        controller.selected_transition.selected = False
        controller.selected_transition = None

    @transition('Selected')
    def mouseReleased(self, controller):
        for state in states:
            if state == controller.selected_state:
                continue
            if state.is_selected():
                controller.selected_transition.to_state = state
                break
        controller.changeState(Selected)


@singleton
class Move(BaseState):

    def start(self, controller):
        global mousePressedX, mousePressedY

    def mouseDragged(self, controller):
        controller.selected_state.x = mousePX
        controller.selected_state.y = mousePY

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
        if controller.selected_state.is_selected():
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
        global mousePressedX, mousePressedY, oldPanX, oldPanY, oldScaleXY
        mousePressedX = mouseX
        mousePressedY = mouseY
        oldPanX = panX
        oldPanY = panY
        oldScaleXY = scaleXY

    def mouseDragged(self, controller):
        global panX, panY, scaleXY
        if mouseButton == LEFT and lastKeyCode == ALT:
            scaleXY = max(0.1, (mouseY - mousePressedY) / 100.0 + oldScaleXY)
            panX = oldPanX + (-1 * mousePressedX / oldScaleXY) + (mousePressedX / scaleXY)
            panY = oldPanY + (-1 * mousePressedY / oldScaleXY) + (mousePressedY / scaleXY)
        elif mouseButton == LEFT:
            panX = (mouseX - mousePressedX) / scaleXY + oldPanX
            panY = (mouseY - mousePressedY) / scaleXY + oldPanY

    @transition('Ready')
    def mouseReleased(self, controller):
        global lastKeyCode
        lastKeyCode = 0
        controller.changeState(Ready)

    def keyPressed(self, controller):
        global lastKeyCode
        lastKeyCode = keyCode

    def keyReleased(self, controller):
        global lastKeyCode
        lastKeyCode = 0


@singleton
class Load(BaseState):

    def start(self, controller):
        selectInput("Input file", "fileSelected")

    @transition('Ready')
    def fileSelected(self, controller, selection):
        global states, transitions, panX, panY, scaleXY
        try:
            if selection:
                new_states = []
                new_transitions = []
                with open(selection.getAbsolutePath()) as f:
                    d = yaml.load(f.read())
                for state_d in d.get('states', []):
                    label = state_d.get('label') or "S{0}".format(next(state_sequence))
                    state = FSMState(label=label,
                                     x=state_d.get('x', random.randrange(panX, width*scaleXY + panX)),
                                     y=state_d.get('y', random.randrange(panY, height*scaleXY + panY)),
                                     color=state_d.get('color', 255),
                                     size=state_d.get('size', max(100, textWidth(label) + 20)))
                    new_states.append(state)
                for transition_d in d.get('transitions', []):
                    from_state = [s for s in new_states if s.label == transition_d['from_state']]
                    to_state = [s for s in new_states if s.label == transition_d['to_state']]
                    assert len(from_state) == 1, str(from_state)
                    assert len(to_state) == 1, str(to_state)
                    t = FSMTransition(label=transition_d.get('label'),
                                      to_state=to_state[0],
                                      from_state=from_state[0])
                    new_transitions.append(t)
                view_d = d.get('view', {})
                panX = view_d.get('panX', 0)
                panY = view_d.get('panY', 0)
                scaleXY = view_d.get('scaleXY', 1)
                states = new_states
                transitions = new_transitions
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
                app['view'] = dict(panX=panX, panY=panY, scaleXY=scaleXY)
                app['states'] = [s.to_dict() for s in states]
                app['transitions'] = [t.to_dict() for t in transitions]
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
        s = FSMState(label="S{0}".format(next(state_sequence)), x=mousePX, y=mousePY)
        states.append(s)
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

    def draw(self):
        stroke(0)
        fill(self.color)
        ellipse(self.x, self.y, self.size, self.size)
        if self.selected:
            strokeWeight(2)
            noFill()
            stroke(SELECTED_COLOR)
            ellipse(self.x, self.y, self.size+6, self.size+6)
        fill(0)
        if self.edit:
            text(self.label + "_", self.x - textWidth(self.label + "_")/2, self.y)
        else:
            text(self.label, self.x - textWidth(self.label)/2, self.y)

    def is_selected(self):
        return (mousePX - self.x)**2 + (mousePY - self.y)**2 < (self.size/2)**2


def arrow(x1, y1, x2, y2, arrow_offset, label="", selected=False, label_offset=0):
    if selected:
        strokeWeight(6)
        stroke(SELECTED_COLOR)
        fill(0)
        line(x1, y1, x2, y2)
        pushMatrix()
        translate(x2, y2)
        rotate(atan2(y2-y1, x2-x1))
        translate(-arrow_offset, 0)
        stroke(SELECTED_COLOR)
        fill(SELECTED_COLOR)
        triangle(4, 0, -12, 7, -12, -7)
        popMatrix()
    strokeWeight(2)
    stroke(0)
    fill(0)
    line(x1, y1, x2, y2)
    pushMatrix()
    translate(x2, y2)
    rotate(atan2(y2-y1, x2-x1))
    pushMatrix()
    translate(-arrow_offset, 0)
    stroke(0)
    fill(0)
    triangle(0, 0, -10, 5, -10, -5)
    popMatrix()
    translate(-sqrt((y2-y1)**2 + (x2-x1)**2)/2.0, 0)
    text(label, -textWidth(label) / 2, -(TEXT_SIZE * 0.5) - TEXT_SIZE * label_offset)
    popMatrix()


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

    def is_selected(self):
        x1 = self.from_state.x
        y1 = self.from_state.y
        x2 = self.to_state.x
        y2 = self.to_state.y
        x = mousePX
        y = mousePY

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
            selected_distance = 10 + TEXT_SIZE * (self.label_offset + 1.5)
        elif abs(line_atan) > pi/2.0 and pline_atan > 0:
            selected_distance = 10
        else:
            selected_distance = 10 + TEXT_SIZE * (self.label_offset + 1.5)
        if distance < selected_distance:
            if application.debug:
                stroke(SELECTED_COLOR)
                line(x, y, result_x, result_y)
            return True
        else:
            return False

    def draw(self):
        self.label_offset = 0
        for t in transitions:
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
                  mousePX,
                  mousePY,
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


class Wheel(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_menu_selection(self):
        if mouseX < self.x and mouseY < self.y:
            return "New"
        elif mouseX > self.x and mouseY > self.y:
            return "Save"
        elif mouseX > self.x and mouseY < self.y:
            return "Load"
        return None

    def draw(self):
        if self.x and self.y:
            noFill()
            stroke(0)
            strokeWeight(2)
            ellipse(self.x, self.y, 100, 100)
            textSize(TEXT_SIZE)
            text("New", self.x - 55, self.y - 55)
            text("Save", self.x + 55, self.y + 55 + TEXT_SIZE)
            text("Load", self.x + 55, self.y - 55)
            line(self.x, self.y, self.x + 50, self.y)
            line(self.x, self.y, self.x - 50, self.y)
            line(self.x, self.y, self.x, self.y - 50)
            line(self.x, self.y, self.x, self.y + 50)
            line(self.x, self.y, mouseX, mouseY)


class Application(object):

    def __init__(self):
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

    def draw(self):
        if self.debug:
            fill(255)
            textSize(TEXT_SIZE)
            xy_t = "xy_t: {0}, {1}".format(mouseX, mouseY)
            text(xy_t,
                 width - 100 - textWidth(xy_t),
                 height - 150)
            xyp_t = "xyp_t: {0}, {1}".format(mousePX, mousePY)
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
            pan = "pan: {0}, {1}".format(int(panX), int(panY))
            text(pan,
                 width - 100 - textWidth(pan),
                 height - 30)
            scaleXYT = "scale: {0}".format(scaleXY)
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
    scale(scaleXY)
    translate(panX, panY)


def draw():
    global mousePX, mousePY
    mousePX = mouseX / scaleXY - panX
    mousePY = mouseY / scaleXY - panY
    background(102)
    pushMatrix()
    scale_and_pan()
    for t in transitions:
        t.draw()
    for state in states:
        state.draw()
    popMatrix()
    application.draw()
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
