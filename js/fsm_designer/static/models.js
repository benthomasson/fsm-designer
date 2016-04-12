var inherits = require('inherits')

var fsm = require('./fsm.js')


function FSMState () {
}
exports.FSMState = FSMState

function FSMTransition () {
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
        fill(255)
        scale(1 / this.scaleXY)
        translate(-this.panX, -this.panY)
        text('fps: ' + frameRate(), windowWidth - 200, 10)
    }
}
exports.Application = Application
