

from fsm import to_yaml, validate_design, generate_code

import yaml

from models import Application

import os
import sys
import logging

from design_fsm import Start
import design_fsm


logger = logging.getLogger("fsm_designer")


page_width = 1024
page_height = 768
application = None


def validate_self():

    logging.debug("pwd: {0}".format(os.getcwd()))

    with open("current.yml", 'w') as f:
        self_yml = to_yaml(design_fsm, "fsm_designer")
        f.write(self_yml)

    with open("design.yml") as f:
        design = yaml.load(f.read())
        missing_states, missing_transitions = validate_design(design, design_fsm, "fsm_designer")
        logger.debug(missing_states)
        logger.debug(missing_transitions)
        if missing_states or missing_transitions:
            print "Self validation failed! Example code:"
            print generate_code(missing_states, missing_transitions)
        else:
            logger.info("Self validation completed")


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
