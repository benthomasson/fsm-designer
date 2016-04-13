var inherits = require('inherits')
var settings = require('./settings.js')
var button_fsm = require('./button_fsm.js')

function arrow (x1, y1, x2, y2, arrow_offset, label = '', selected = false, label_offset = 0) {
    if (selected) {
        strokeWeight(6)
        stroke(settings.SELECTED_COLOR)
        fill(0)
        line(x1, y1, x2, y2)
        push()
        translate(x2, y2)
        rotate(atan2(y2 - y1, x2 - x1))
        translate(-arrow_offset, 0)
        stroke(settings.SELECTED_COLOR)
        fill(settings.SELECTED_COLOR)
        triangle(4, 0, -12, 7, -12, -7)
        pop()
    }
    strokeWeight(2)
    stroke(settings.COLOR)
    fill(settings.COLOR)
    line(x1, y1, x2, y2)
    push()
    translate(x2, y2)
    rotate(atan2(y2 - y1, x2 - x1))
    push()
    translate(-arrow_offset, 0)
    stroke(settings.COLOR)
    fill(settings.COLOR)
    triangle(0, 0, -10, 5, -10, -5)
    pop()
    translate(-sqrt(Math.pow((y2 - y1), 2) + Math.pow((x2 - x1), 2)) / 2.0, 0)
    textSize(settings.TEXT_SIZE)
    noStroke()
    text(label, -textWidth(label) / 2, -(settings.TEXT_SIZE * 0.5) - settings.TEXT_SIZE * label_offset)
    pop()
}
exports.arrow = arrow

function Widget () {

}

Widget.prototype.mouseOver = function () {
}

Widget.prototype.mouseOut = function () {
}

Widget.prototype.mousePressed = function () {
}

Widget.prototype.mouseReleased = function () {
}

Widget.prototype.topExtent = function () {
    return 0
}
Widget.prototype.bottomExtent = function () {
    return 0
}
Widget.prototype.leftExtent = function () {
    return 0
}
Widget.prototype.rightExtent = function () {
    return 0
}

function Button (x, y, label, text_size = 20, size = 20, color = '#5A5A5A', fill = '#B9B9B9', pressed_color = '#7F7F7F', call_back = null) {
    this.x = x
    this.y = y
    this.text_size = text_size
    this.label = label
    this.color = color
    this.fill = fill
    this.size = size
    this.pressed_color = pressed_color
    this.state = button_fsm.NotPressed
    this.pressed = false
    this.active = false
    this.call_back = call_back
}

inherits(Button, button_fsm.Controller)

Button.prototype.mouseOver = function () {
    this.active = true
}

Button.prototype.mouseOut = function () {
    this.active = false
    this.state.mouseOut(this)
}

Button.prototype.mousePressed = function () {
    this.state.mousePressed(this)
}

Button.prototype.mouseReleased = function () {
    this.state.mouseReleased(this)
}

Button.prototype.topExtent = function () {
    return this.y
}
Button.prototype.leftExtent = function () {
    return this.x
}
Button.prototype.rightExtent = function () {
    textSize(this.text_size)
    return this.x + textWidth(this.label) + this.size
}
Button.prototype.bottomExtent = function () {
    return this.y + this.size + this.text_size
}
Button.prototype.width = function () {
    return this.right_extent() - this.left_extent()
}
Button.prototype.height = function () {
    return this.bottom_extent() - this.top_extent()
}

Button.prototype.draw = function () {
    this.draw_button()
    this.draw_icon()
    this.draw_label()
}

Button.prototype.draw_button = function () {
    push()
    translate(this.x, this.y)
    if (this.active) {
        stroke(this.color)
    } else {
        stroke(this.fill)
    }
    if (this.pressed) {
        fill(this.pressed_color)
    } else {
        fill(this.fill)
    }
    textSize(this.text_size)
    rect(0, 0, this.width, this.height, this.size / 5)
    pop()
}
Button.prototype.draw_icon = function () {
}

Button.prototype.draw_label = function () {
    push()
    translate(this.x, this.y)
    translate((textWidth(this.label) + this.size) / 2,
              (this.size + this.text_size) / 2 - this.text_size / 4)
    textAlign(CENTER, CENTER)
    fill(this.color)
    text(this.label, 0, 0)
    pop()
    textAlign(LEFT, BASELINE)
}

exports.Button = Button
function button (x, y, label, text_size = 20, size = 20, color = '#5A5A5A', fill = '#B9B9B9') {
    return Button(x, y, label, text_size, size, color, fill).draw()
}
exports.button = button
