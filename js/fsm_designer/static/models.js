var inherits = require('inherits')
var fsm = require('./fsm.js')
var settings = require('./settings.js')
var widgets = require('./widgets.js')

function FSMState () {
    this.x = 0
    this.y = 0
    this.label = ''
    this.size = 100
    this.selected = false
    this.edit = false
    this.label_offset = 0
}
FSMState.prototype.draw = function (controller) {
    stroke(settings.COLOR)
    fill(settings.FILL)
    ellipse(this.x, this.y, this.size, this.size)
    if (this.selected) {
        strokeWeight(2)
        stroke(settings.SELECTED_COLOR)
        fill(settings.FILL)
        ellipse(this.x, this.y, this.size + 6, this.size + 6)
    }
    noStroke()
    fill(settings.COLOR)
    textSize(settings.TEXT_SIZE)
    if (this.edit) {
        text(this.label + '_', this.x - textWidth(this.label + '_') / 2, this.y)
    } else {
        text(this.label, this.x - textWidth(this.label) / 2, this.y)
    }
}
FSMState.prototype.is_selected = function (controller) {
    return Math.pow((controller.mousePX - this.x), 2) + Math.pow((controller.mousePY - this.y), 2) < Math.pow((this.size / 2), 2)
}
exports.FSMState = FSMState

function FSMTransition () {
    this.from_state = null
    this.to_state = null
    this.label = ''
    this.selected = false
    this.edit = false
}
FSMTransition.prototype.draw = function (controller) {
    this.label_offset = 0
    for (var i = 0; i < controller.transitions.length; i++) {
        var t = controller.transitions[i]
        if (t === this) {
            break
        }
        if (t.to_state === this.to_state && t.from_state === this.from_state) {
            this.label_offset += 1
        }
    }
    var label = this.label
    if (this.edit) {
        label = this.label + '_'
    }
    if (this.from_state != null && this.to_state == null) {
        widgets.arrow(this.from_state.x,
                      this.from_state.y,
                      controller.mousePX,
                      controller.mousePY,
                      0,
                      label,
                      this.selected,
                      this.label_offset)
    }
    if (this.from_state != null && this.to_state != null) {
        widgets.arrow(this.from_state.x,
                      this.from_state.y,
                      this.to_state.x,
                      this.to_state.y,
                      this.to_state.size / 2,
                      label,
                      this.selected,
                      this.label_offset)
    }
}
exports.FSMTransition = FSMTransition

function Application () {
    this.states = []
    this.transitions = []
    this.panX = 0
    this.panY = 0
    this.oldPanX = 0
    this.oldPanY = 0
    this.scaleXY = 1
    this.oldScaleXY = 0
    this.mousePX = 0
    this.mousePY = 0
    this.mousePressedX = 0
    this.mousePressedY = 0
    this.lastKeyCode = 0
    this.state = null
    this.wheel = null
    this.selected_state = null
    this.selected_transition = null
    this.debug = true
    this.mouse_pointer = null
    this.active_widgets = []
    this.model = null
    this.app = null
    this.directory = null
}

inherits(Application, fsm.Controller)

Application.prototype.save = function (button) {
}

Application.prototype.load = function (button) {
}

Application.prototype.generate = function (button) {
}

Application.prototype.validate = function (button) {
}

Application.prototype.draw = function (controller) {
    if (this.debug) {
        noStroke()
        fill(255)
        scale(1 / this.scaleXY)
        translate(-this.panX, -this.panY)
        text('fps: ' + frameRate(), 10, 10)
    }
}
exports.Application = Application
