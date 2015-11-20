

from fsm import State, transition, to_yaml, singleton

import sys

from math import sqrt, pi

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


class BaseState(State):

    def name(self):
        return self.__class__.__name__

    def start(self):
        pass

    def end(self):
        pass

    def mousePressed(self):
        pass

    def mouseReleased(self):
        pass

    def mouseDragged(self):
        pass

    def keyPressed(self):
        pass

    def keyReleased(self):
        pass

    def keyTyped(self):
        pass

    def fileSelected(self, selected):
        pass


@singleton
class Other(BaseState):

    pass


def select_state():
    application.selected_state = None
    for state in states:
        if state.is_selected() and application.selected_state is None:
            state.selected = True
            application.selected_state = state
        else:
            state.selected = False


@singleton
class Ready(BaseState):

    @transition('MenuWheel')
    @transition('ScaleAndPan')
    @transition('Selected')
    def mousePressed(self):
        if mouseButton == RIGHT:
            application.changeState(MenuWheel)

        elif mouseButton == LEFT:
            select_state()
            if application.selected_state is None:
                application.changeState(ScaleAndPan)
            else:
                application.changeState(Selected)

    def keyPressed(self):
        global lastKeyCode
        lastKeyCode = keyCode


@singleton
class Selected(BaseState):

    @transition('MenuWheel')
    @transition('Edit')
    @transition('Ready')
    @transition('Move')
    def mousePressed(self):
        if mouseButton == RIGHT:
            if application.selected_state.is_selected():
                application.changeState(Edit)
            else:
                application.selected_state.selected = False
                application.selected_state = None
                application.changeState(MenuWheel)
        elif mouseButton == LEFT:
            if application.selected_state.is_selected():
                application.changeState(Move)
            else:
                application.changeState(Ready)
                application.state.mousePressed()

    @transition('Move')
    @transition('NewTransition')
    def mouseDragged(self):
        if mouseButton == LEFT:
            application.changeState(Move)
            application.state.mouseDragged()
        if mouseButton == RIGHT:
            application.changeState(NewTransition)
            application.state.mouseDragged()

    def keyReleased(self):
        if keyCode == 8:
            application.selected_state.selected = False
            states.remove(application.selected_state)
            application.changeState(Ready)


@singleton
class NewTransition(BaseState):

    def start(self):
        new_transition = FSMTransition(from_state=application.selected_state)
        transitions.append(new_transition)
        application.selected_transition = new_transition

    def end(self):
        if application.selected_transition is not None and application.selected_transition.to_state is None:
            transitions.remove(application.selected_transition)
        application.selected_transition = None

    @transition('Selected')
    def mouseReleased(self):
        for state in states:
            if state == application.selected_state:
                continue
            if state.is_selected():
                application.selected_transition.to_state = state
                break
        application.changeState(Selected)


@singleton
class Move(BaseState):

    def start(self):
        global mousePressedX, mousePressedY

    def mouseDragged(self):
        application.selected_state.x = mousePX
        application.selected_state.y = mousePY

    @transition('Selected')
    def mouseReleased(self):
        application.changeState(Selected)


@singleton
class Edit(BaseState):

    def start(self):
        application.selected_state.edit = True

    def end(self):
        application.selected_state.edit = False

    @transition('NewTransition')
    def mouseDragged(self):
        if mouseButton == RIGHT:
            application.changeState(NewTransition)
            application.state.mouseDragged()

    @transition('Selected')
    @transition('Ready')
    def mousePressed(self):
        if application.selected_state.is_selected():
            application.changeState(Selected)
            application.state.mousePressed()
        else:
            application.changeState(Ready)
            application.state.mousePressed()

    def keyReleased(self):
        if keyCode == 8:
            application.selected_state.label = application.selected_state.label[:-1]

    @transition('Selected')
    def keyTyped(self):
        print key, keyCode
        if key == CODED:
            if keyCode == 8:
                application.selected_state.label = application.selected_state.label[:-1]
        else:
            if key == RETURN:
                application.changeState(Selected)
            elif key == ENTER:
                application.changeState(Selected)
            elif key == BACKSPACE:
                application.selected_state.label = application.selected_state.label[:-1]
            elif key == DELETE:
                application.selected_state.label = application.selected_state.label[:-1]
            else:
                application.selected_state.label += key


@singleton
class ScaleAndPan(BaseState):

    def start(self):
        global mousePressedX, mousePressedY, oldPanX, oldPanY, oldScaleXY
        mousePressedX = mouseX
        mousePressedY = mouseY
        oldPanX = panX
        oldPanY = panY
        oldScaleXY = scaleXY

    def mouseDragged(self):
        global panX, panY, scaleXY
        if mouseButton == LEFT and lastKeyCode == ALT:
            scaleXY = max(0.1, (mouseY - mousePressedY) / 100.0 + oldScaleXY)
            panX = oldPanX + (-1 * mousePressedX / oldScaleXY) + (mousePressedX / scaleXY)
            panY = oldPanY + (-1 * mousePressedY / oldScaleXY) + (mousePressedY / scaleXY)
        elif mouseButton == LEFT:
            panX = (mouseX - mousePressedX) / scaleXY + oldPanX
            panY = (mouseY - mousePressedY) / scaleXY + oldPanY

    @transition('Ready')
    def mouseReleased(self):
        global lastKeyCode
        lastKeyCode = 0
        application.changeState(Ready)

    def keyPressed(self):
        global lastKeyCode
        lastKeyCode = keyCode

    def keyReleased(self):
        global lastKeyCode
        lastKeyCode = 0


@singleton
class NewState(BaseState):

    def name(self):
        return "New State!"

    @transition(Ready)
    def start(self):
        s = FSMState(name="New", x=mousePX, y=mousePY)
        states.append(s)
        application.changeState(Ready)


@singleton
class MenuWheel(BaseState):

    def start(self):
        application.wheel = Wheel(mouseX, mouseY)

    def end(self):
        application.wheel = None

    @transition(Ready)
    def mouseReleased(self):
        menu_selection = application.wheel.get_menu_selection()
        if menu_selection == "New":
            application.changeState(NewState)
        elif menu_selection == "Save":
            application.changeState(Ready)
        elif menu_selection == "Load":
            application.changeState(Ready)
        else:
            application.changeState(Ready)


class FSMState(object):

    def __init__(self, **kwargs):
        self.x = 0
        self.y = 0
        self.label = ""
        self.size = 100
        self.color = 255
        self.selected = False
        self.edit = False
        self.__dict__.update(kwargs)

    def draw(self):
        stroke(0)
        fill(self.color)
        ellipse(self.x, self.y, self.size, self.size)
        if self.selected:
            strokeWeight(2)
            noFill()
            stroke("#66FFFF")
            ellipse(self.x, self.y, self.size+6, self.size+6)
        fill(0)
        if self.edit:
            text(self.label + "_", self.x - textWidth(self.label + "_")/2, self.y)
        else:
            text(self.label, self.x - textWidth(self.label)/2, self.y)

    def is_selected(self):
        return (mousePX - self.x)**2 + (mousePY - self.y)**2 < (self.size/2)**2


def arrow(x1, y1, x2, y2, arrow_offset, label=""):
    line(x1, y1, x2, y2)
    line(x2, y2, x2, y2)
    pushMatrix()
    translate(x2, y2)
    rotate(atan2(y2-y1, x2-x1))
    pushMatrix()
    translate(-arrow_offset, 0)
    triangle(0, 0, -10, 5, -10, -5)
    popMatrix()
    translate(-sqrt((y2-y1)**2 + (x2-x1)**2)/2.0, 0)
    if abs(atan2(y2-y1, x2-x1)) > 2:
        rotate(pi)
    text(label, -textWidth(label) / 2, -TEXT_SIZE * 0.5)
    popMatrix()


class FSMTransition(object):

    def __init__(self, **kwargs):
        self.from_state = None
        self.to_state = None
        self.label = "foobar"
        self.__dict__.update(kwargs)

    def draw(self):
        strokeWeight(2)
        stroke(0)
        fill(0)
        if self.from_state is not None and self.to_state is None:
            arrow(self.from_state.x, self.from_state.y, mousePX, mousePY, 0, self.label)
        if self.from_state is not None and self.to_state is not None:
            arrow(self.from_state.x, self.from_state.y, self.to_state.x, self.to_state.y, self.to_state.size/2, self.label)


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
        self.state = Ready
        self.wheel = None
        self.selected_state = None
        self.selected_transition = None

    def changeState(self, state):
        if self.state:
            self.state.end()
        self.state = state
        if self.state:
            self.state.start()

    def draw(self):
        fill(255)
        textSize(TEXT_SIZE)
        xy_t = "xy_t: {0}, {1}".format(mouseX, mouseY)
        text(xy_t,
             page_width - 100 - textWidth(xy_t),
             page_height - 150)
        xyp_t = "xyp_t: {0}, {1}".format(mousePX, mousePY)
        text(xyp_t,
             page_width - 100 - textWidth(xyp_t),
             page_height - 130)
        text(self.state.name(),
             page_width - 100 - textWidth(self.state.name()),
             page_height - 110)
        fps = "fps: {0}".format(int(frameRate))
        text(fps,
             page_width - 100 - textWidth(fps),
             page_height - 50)
        pan = "pan: {0}, {1}".format(int(panX), int(panY))
        text(pan,
             page_width - 100 - textWidth(pan),
             page_height - 30)
        scaleXYT = "scale: {0}".format(scaleXY)
        text(scaleXYT,
             page_width - 100 - textWidth(scaleXYT),
             page_height - 10)
        key_t = "key: {0} keyCode: {1}".format(str(key).strip(), keyCode)
        text(key_t,
             page_width - 100 - textWidth(key_t),
             page_height - 70)
        mouseButton_t = "mouseButton: {0}".format(mouseButton)
        text(mouseButton_t,
             page_width - 100 - textWidth(mouseButton_t),
             page_height - 90)

        if self.wheel:
            self.wheel.draw()


print to_yaml(sys.modules[__name__])


def setup():
    global application
    size(page_width, page_height, FX2D)
    application = Application()
    frameRate(30)


def draw():
    global mousePX, mousePY
    mousePX = mouseX / scaleXY - panX
    mousePY = mouseY / scaleXY - panY
    background(102)
    application.draw()
    scale(scaleXY)
    translate(panX, panY)
    for t in transitions:
        t.draw()
    for state in states:
        state.draw()


def mousePressed():
    application.state.mousePressed()


def mouseDragged():
    application.state.mouseDragged()


def mouseReleased():
    application.state.mouseReleased()


def keyPressed():
    application.state.keyPressed()


def keyReleased():
    application.state.keyReleased()


def keyTyped():
    application.state.keyTyped()


def fileSelected(selection):
    application.state.fileSelected(selection)
