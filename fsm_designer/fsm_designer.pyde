

from fsm import State, transition, to_yaml, singleton

import sys

states = []
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


@singleton
class Ready(BaseState):

    @transition(Other)
    def on_hello(self):
        pass

    @transition('MenuWheel')
    def mousePressed(self):
        global mousePressedX, mousePressedY, oldPanX, oldPanY, oldScaleXY
        mousePressedX = mouseX
        mousePressedY = mouseY
        oldPanX = panX
        oldPanY = panY
        oldScaleXY = scaleXY

        if mouseButton == RIGHT:
            application.changeState(MenuWheel)

    def mouseDragged(self):
        global panX, panY, scaleXY
        if mouseButton == LEFT and lastKeyCode == ALT:
            scaleXY = max(0.1, (mouseY - mousePressedY) / 100.0 + oldScaleXY)
            panX = oldPanX + (-1 * mousePressedX / oldScaleXY) + (mousePressedX / scaleXY)
            panY = oldPanY + (-1 * mousePressedY / oldScaleXY) + (mousePressedY / scaleXY)
        elif mouseButton == LEFT:
            panX = (mouseX - mousePressedX) / scaleXY + oldPanX
            panY = (mouseY - mousePressedY) / scaleXY + oldPanY

    def mouseReleased(self):
        global lastKeyCode
        lastKeyCode = 0

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
        self.label = None
        self.size = 100
        self.color = 255
        self.__dict__.update(kwargs)

    def draw(self):
        fill(self.color)
        ellipse(self.x, self.y, self.size, self.size)


class FSMTransition(object):

    def __init__(self, **kwargs):
        self.from_state = None
        self.to_state = None
        self.label = None

    def draw(self):
        pass


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
        key_t = "keyCode: {0}".format(lastKeyCode)
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
    rect(0,0,100,100)
    scale(scaleXY)
    translate(panX, panY)
    rect(0,0,100,100)
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
