
console.log(main)

var application = new main.models.Application()
var state = new main.models.FSMState()
var state2 = new main.models.FSMState()
var transition = new main.models.FSMTransition()
var button = new main.widgets.Button()
var button1 = new main.widgets.Button()
var button2 = new main.widgets.Button()
button.call_back = function (button) {
    console.log('Button pressed!')
}
var active_widgets = []
active_widgets.push(button)
active_widgets.push(button1)
active_widgets.push(button2)
var bar = new main.widgets.ButtonBar()
bar.buttons.push(button)
bar.buttons.push(button1)
bar.buttons.push(button2)

function setup () {
    createCanvas(windowWidth, windowHeight)
}

function draw () {
    push()
    translate(application.panX, application.panY)
    scale(application.scaleXY)
    application.mouseSX = mouseX * 1 / application.scaleXY
    application.mouseSY = mouseY * 1 / application.scaleXY
    background(102)
    fill(255)

    state.x = 100
    state.y = 100
    state.label = 'Foo'

    state2.x = 300
    state2.y = 100
    state2.label = 'Bar'

    transition.from_state = state
    transition.to_state = state2
    transition.label = 'foobar'
    transition.draw(application)
    state.draw(application)
    state2.draw(application)

    button.label = 'Press'
    button1.label = '1'
    button2.label = '2'
    bar.x = 100
    bar.y = 300

    application.draw(application)
    pop()

    bar.draw(application)

    for (var i = 0; i < active_widgets.length; i++) {
        widget = active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mouseOver()
        } else {
            widget.mouseOut()
            widget.mouseReleased()
        }
    }

}

function windowResized () {
    resizeCanvas(windowWidth, windowHeight)
}

function mouseWheel (event) {
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
    for (var i = 0; i < active_widgets.length; i++) {
        widget = active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mousePressed()
            return
        }
    }
}

function mouseReleased () {
    for (var i = 0; i < active_widgets.length; i++) {
        widget = active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mouseReleased()
        }
    }
}

!(function () {
    this.draw = draw
    this.setup = setup
    this.windowResized = windowResized
    this.mouseWheel = mouseWheel
    this.mousePressed = mousePressed
    this.mouseReleased = mouseReleased
}())
