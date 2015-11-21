
from math import sqrt, pi
import logging

from conf import settings
from widgets import arrow


logger = logging.getLogger("fsm_designer.models")


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
            stroke(settings.SELECTED_COLOR)
            ellipse(self.x, self.y, self.size+6, self.size+6)
        fill(0)
        if self.edit:
            text(self.label + "_", self.x - textWidth(self.label + "_")/2, self.y)
        else:
            text(self.label, self.x - textWidth(self.label)/2, self.y)

    def is_selected(self):
        return (mousePX - self.x)**2 + (mousePY - self.y)**2 < (self.size/2)**2


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
            selected_distance = 10 + settings.TEXT_SIZE * (self.label_offset + 1.5)
        elif abs(line_atan) > pi/2.0 and pline_atan > 0:
            selected_distance = 10
        else:
            selected_distance = 10 + settings.TEXT_SIZE * (self.label_offset + 1.5)
        if distance < selected_distance:
            if application.debug:
                stroke(settings.SELECTED_COLOR)
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
