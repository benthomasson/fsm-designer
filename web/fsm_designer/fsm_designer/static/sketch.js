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
    application.mousePointer = application.MagnifyingGlassMousePointer
    application.pointer_count_down = Math.floor(frameRate() / 2)
    application.scaleXY = application.scaleXY + event.delta / 100
    if (application.scaleXY < 0.2) {
        application.scaleXY = 0.2
    }
    if (application.scaleXY > 10) {
        application.scaleXY = 10
    }
    return false
}

function mousePressed () {
    if (mouseButton === LEFT) {
        console.log('left')
    }
    if (mouseButton === RIGHT) {
        console.log('right')
    }
    if (mouseButton === CENTER) {
        console.log('center')
    }
    var widget = null
    for (var i = 0; i < application.active_widgets.length; i++) {
        widget = application.active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mousePressed()
            return false
        }
    }

    return false
}

function mouseReleased () {
    var widget = null
    for (var i = 0; i < application.active_widgets.length; i++) {
        widget = application.active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mouseReleased()
        }
    }
    application.mousePointer = application.ArrowMousePointer
    application.pointer_count_down = null
}

function mouseDragged () {
    application.mousePointer = application.MoveMousePointer
    application.pointer_count_down = null
    application.panX += mouseX - pmouseX
    application.panY += mouseY - pmouseY
    return false
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
}())
