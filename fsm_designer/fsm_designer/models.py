
from math import sqrt, pi
import logging
import itertools

from conf import settings
from widgets import arrow
from processing_widgets.widgets import Button, ButtonBar

from subprocess import Popen, PIPE, STDOUT


logger = logging.getLogger("fsm_designer.models")


class FSMState(object):

    def __init__(self, **kwargs):
        self.x = 0
        self.y = 0
        self.label = ""
        self.size = 100
        self.selected = False
        self.edit = False
        self.label_offset = 0
        self.__dict__.update(kwargs)

    def to_dict(self):
        d = {}
        d['label'] = self.label
        d['x'] = self.x
        d['y'] = self.y
        d['size'] = self.size
        return d

    def draw(self, controller):
        stroke(settings.COLOR)
        fill(settings.FILL)
        ellipse(self.x, self.y, self.size, self.size)
        if self.selected:
            strokeWeight(2)
            stroke(settings.SELECTED_COLOR)
            fill(settings.FILL)
            ellipse(self.x, self.y, self.size+6, self.size+6)
        fill(settings.COLOR)
        textSize(settings.TEXT_SIZE)
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
        if controller.debug:
            logger.debug("%s %s", line_atan, pline_atan)
            if abs(line_atan) < pi/2.0 and pline_atan < 0:
                stroke(settings.COLOR)
            elif abs(line_atan) > pi/2.0 and pline_atan < 0:
                stroke(255)
            elif abs(line_atan) > pi/2.0 and pline_atan > 0:
                stroke(settings.COLOR)
            else:
                stroke(255)
            line(x, y, result_x, result_y)
        if abs(line_atan) < pi/2.0 and pline_atan < 0:
            selected_distance = 10
        elif abs(line_atan) > pi/2.0 and pline_atan < 0:
            selected_distance = 10 + settings.TEXT_SIZE * (self.label_offset + 1.5)
        elif abs(line_atan) > pi/2.0 and pline_atan > 0:
            selected_distance = 10
        else:
            selected_distance = 10 + settings.TEXT_SIZE * (self.label_offset + 1.5)
        if distance < selected_distance:
            if controller.debug:
                stroke(settings.SELECTED_COLOR)
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
        self.mouse_pointer = None
        self.active_widgets = []
        self.model = None
        self.app = None
        self.directory = None
        self.active_widgets.append(Button(x=0, y=0, label="Save", call_back=self.save))
        self.active_widgets.append(Button(x=0, y=0, label="Load", call_back=self.load))
        self.active_widgets.append(Button(x=0, y=0, label="Generate", call_back=self.generate))
        self.active_widgets.append(Button(x=0, y=0, label="Validate", call_back=self.validate))
        self.button_bar = ButtonBar(self.active_widgets, 10, 10)

    def save(self, button):
        print button
        from design_fsm import Save
        self.changeState(Save)

    def load(self, button):
        print button
        from design_fsm import Load
        self.changeState(Load)

    def generate(self, button):
        p = Popen("fsm-designer generate -d {0} {1}.py".format(self.model, self.app),
                  shell=True, stdout=PIPE, stderr=STDOUT, cwd=self.directory)
        stdout, stderr = p.communicate()
        print stderr
        print stdout
        print p.returncode

    def validate(self, button):
        p = Popen("fsm-designer validate -d {0} {1}".format(self.model, self.app),
                  shell=True, stdout=PIPE, stderr=STDOUT, cwd=self.directory)
        stdout, stderr = p.communicate()
        print stderr
        print stdout
        print p.returncode

    def changeState(self, state):
        if self.state:
            self.state.end(self)
        self.state = state
        if self.state:
            self.state.start(self)

    def draw(self, controller):
        if self.debug:
            fill(0)
            textSize(settings.TEXT_SIZE)
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

        self.button_bar.draw()

        if self.mouse_pointer:
            self.mouse_pointer.draw()
