

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
    size(200, 200, FX2D);
    smooth(4)
    #pg = createGraphics(100, 100);


def draw():
    global mousePX, mousePY, panX, panY
    mousePX = mouseX/scaleX - panX
    mousePY = mouseY/scaleY - panY
    #pg.beginDraw()
    background(102)
    stroke(255)
    strokeWeight(1)
    translate(panX, panY)
    line(width*0.5, height*0.5, mousePX, mousePY)
    #pg.endDraw()
    #scale(scaleX, scaleY)
    #image(pg, panX, panY);
    
    
def mousePressed():
    global mousePressedX, mousePressedY
    mousePressedX = mousePX
    mousePressedY = mousePY
    print mousePressedX, mousePressedY
    
    
def mouseDragged():
    global mousePressedX, mousePressedY, panX, panY
    panX = panX + (mousePX - mousePressedX)
    panY = panY + (mousePY - mousePressedY)
    print panX, panY