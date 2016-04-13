
console.log(main)

var scaleXY = 1.0
var panX = 0
var panY = 0
var application = new main.models.Application()
var state = new main.models.FSMState()
var state2 = new main.models.FSMState()
var transition = new main.models.FSMTransition()

function setup () {
    createCanvas(windowWidth, windowHeight)
}

function draw() {
    translate(panX, panY)
    scale(scaleXY)
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
    application.draw(application)

}

function windowResized () {
    resizeCanvas(windowWidth, windowHeight)
}

function mouseWheel (event) {
    scaleXY = scaleXY + event.delta / 100
    if (scaleXY < 0.2) {
        scaleXY = 0.2
    }
    if (scaleXY > 10) {
        scaleXY = 10
    }
    return false
}

!(function () {
    this.draw = draw
    this.setup = setup
    this.windowResized = windowResized
    this.mouseWheel = mouseWheel
}())
