

from fsm import State, transition, to_yaml

import sys

class Other(State):

    pass


class Ready(State):

    @transition(Other)
    def on_hello(self):
        pass


print to_yaml(sys.modules[__name__])

pg = None
panX = 50
panY = 50
scaleX = 1.0
scaleY = 1.0
mousePX = mousePY = 0
mousePressedX = 0
mousePressedY = 0

def setup():
    global pg
    size(1024, 768, FX2D)
    noCursor()



def draw():
    global mousePX, mousePY, panX, panY
    mousePX = mouseX/scaleX - panX
    mousePY = mouseY/scaleY - panY
    background(102)
    stroke(255)
    strokeWeight(1)
    translate(panX, panY)
    line(width*0.5, height*0.5, mousePX, mousePY)

    
    
def mousePressed():
    if mouseButton == RIGHT or keyCode == CONTROL:
        cursor(HAND)
        global mousePressedX, mousePressedY
        mousePressedX = mousePX
        mousePressedY = mousePY
        print mousePressedX, mousePressedY
    
    
def mouseDragged():
    if mouseButton == RIGHT or keyCode == CONTROL:
        cursor(HAND)
        global mousePressedX, mousePressedY, panX, panY
        panX = panX + (mousePX - mousePressedX)
        panY = panY + (mousePY - mousePressedY)
        print panX, panY
        
        
def mouseReleased():
    cursor(ARROW)    