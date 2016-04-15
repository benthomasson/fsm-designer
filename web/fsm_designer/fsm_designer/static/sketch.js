
console.log(main)

var scaleXY = 1.0
var panX = 0
var panY = 0
var application = new main.models.Application()

function setup () {
    createCanvas(windowWidth, windowHeight)
}

function draw() {
    translate(panX, panY)
    scale(scaleXY)
    background(102)
    fill(255)

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
