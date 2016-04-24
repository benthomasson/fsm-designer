/* global main fsm_to_load*/
console.log(main)

var application = new main.models.Application()
var socket = io.connect('/fsm-designer')
application.socket = socket

socket.on('saved', function (message) {
    application.on_saved(message)
})

function setup () {
    createCanvas(windowWidth, windowHeight)
    noCursor()

    application.fsm_to_load = fsm_to_load
}

function draw () {
    if (application.fsm_to_load) {
        application.load_fsm(fsm_to_load)
        application.fsm_to_load = null
    }
    clear()
    push()
    application.mousePX = (mouseX - application.panX) / application.scaleXY
    application.mousePY = (mouseY - application.panY) / application.scaleXY
    translate(application.panX, application.panY)
    scale(application.scaleXY)
    application.mouseSX = mouseX * 1 / application.scaleXY
    application.mouseSY = mouseY * 1 / application.scaleXY
    background(255)
    fill(255)
    application.draw_content(application)
    pop()
    application.draw_menus(application)
}

function windowResized () {
    resizeCanvas(windowWidth, windowHeight)
}

function mouseWheel (event) {
    application.mouseWheel(event)
    return false
}

function mousePressed () {
    application.mousePressed()
    return false
}

function mouseReleased () {
    application.mouseReleased()
}

function mouseDragged () {
    application.mouseDragged()
    return false
}

function keyTyped () {
    try {
        application.keyTyped()
    } catch (err) {
        console.log(err)
    }
    return false
}

function keyPressed () {
    try {
        application.keyPressed()
    } catch (err) {
        console.log(err)
    }
    // Prevent Chrome from using backspace for go to the last page.
    if (keyCode === BACKSPACE) {
        return false
    }
}

function keyReleased () {
    application.keyReleased()
}

!(function () {
    this.draw = draw
    this.setup = setup
    this.windowResized = windowResized
    this.mouseWheel = mouseWheel
    this.mousePressed = mousePressed
    this.mouseReleased = mouseReleased
    this.mouseDragged = mouseDragged
    this.socket = socket
    this.keyTyped = keyTyped
    this.keyPressed = keyPressed
    this.keyReleased = keyReleased
}())
