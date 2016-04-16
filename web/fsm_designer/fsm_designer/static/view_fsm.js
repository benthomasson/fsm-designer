var inherits = require('inherits')

function Controller () {
    this.state = null
}
exports.Controller = Controller

Controller.prototype.changeState = function (state) {
    console.log('changeState: ' + state.constructor.name)
    if (this.state != null) {
        this.state.end(this)
    }
    this.state = state
    if (this.state != null) {
        this.state.start(this)
    }
}
function _State () {
    _State.prototype.start = function (controller) {
    }
    _State.prototype.end = function (controller) {
    }
}
var State = new _State()
exports.State = State
exports._State = _State

function _ViewReady () {
}
inherits(_ViewReady, _State)

var ViewReady = new _ViewReady()

_ViewReady.prototype.mouseDragged = function (controller) {
    controller.application.mousePointer = controller.application.MoveMousePointer
    controller.application.pointer_count_down = null
    controller.application.panX += mouseX - pmouseX
    controller.application.panY += mouseY - pmouseY
}
_ViewReady.prototype.mouseWheel = function (controller, event) {
    controller.application.mousePointer = controller.application.MagnifyingGlassMousePointer
    controller.application.pointer_count_down = Math.floor(frameRate() / 2)
    controller.application.scaleXY = controller.application.scaleXY + event.delta / 100
    if (controller.application.scaleXY < 0.2) {
        controller.application.scaleXY = 0.2
    }
    if (controller.application.scaleXY > 10) {
        controller.application.scaleXY = 10
    }
}
exports.ViewReady = ViewReady

