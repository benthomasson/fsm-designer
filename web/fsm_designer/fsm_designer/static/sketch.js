/* global main */
console.log(main)

var application = new main.models.Application()
var socket = io.connect('/fsm-designer')

var state = new main.models.FSMState()
var state2 = new main.models.FSMState()
var transition = new main.models.FSMTransition()

function setup () {
    createCanvas(windowWidth, windowHeight)
    noCursor()

    state.x = 100
    state.y = 100
    state.label = 'Foo'

    state2.x = 300
    state2.y = 100
    state2.label = 'Bar'

    transition.from_state = state
    transition.to_state = state2
    transition.label = 'foobar'

    application.states.push(state)
    application.states.push(state2)

    application.transitions.push(transition)
}

function draw () {
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
    application.keyTyped()
    return false
}

function keyPressed () {
    application.keyPressed()
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
