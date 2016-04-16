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

function _Load () {
}
inherits(_Load, _State)

// transition to MenuReady
_Load.prototype.start = function (controller) {
    controller.changeState(MenuReady)
}

var Load = new _Load()
exports.Load = Load

function _NewState () {
}
inherits(_NewState, _State)

// transition to MenuReady
_NewState.prototype.start = function (controller) {
    controller.changeState(MenuReady)
}

var NewState = new _NewState()
exports.NewState = NewState

function _NewTransition () {
}
inherits(_NewTransition, _State)

// transition to MenuReady
_NewTransition.prototype.start = function (controller) {
    controller.changeState(MenuReady)
}

var NewTransition = new _NewTransition()
exports.NewTransition = NewTransition

function _MenuReady () {
}
inherits(_MenuReady, _State)

// transition to NewState
_MenuReady.prototype.new_state_button = function (controller) {
    controller.changeState(NewState)
}

// transition to Load
_MenuReady.prototype.load_button = function (controller) {
    controller.changeState(Load)
}

// transition to NewTransition
_MenuReady.prototype.new_transition_button = function (controller) {
    controller.changeState(NewTransition)
}

// transition to Save
_MenuReady.prototype.save_button = function (controller) {
    controller.changeState(Save)
}

_MenuReady.prototype.mousePressed = function (controller) {
    var widget = null
    for (var i = 0; i < controller.application.active_widgets.length; i++) {
        widget = controller.application.active_widgets[i]
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

_MenuReady.prototype.mouseReleased = function (controller) {
    var widget = null
    for (var i = 0; i < controller.application.active_widgets.length; i++) {
        widget = controller.application.active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mouseReleased()
        }
    }
    controller.application.mousePointer = controller.application.ArrowMousePointer
    controller.application.pointer_count_down = null
}

var MenuReady = new _MenuReady()
exports.MenuReady = MenuReady

function _Save () {
}
inherits(_Save, _State)

// transition to MenuReady
_Save.prototype.start = function (controller) {
    controller.changeState(MenuReady)
}

var Save = new _Save()
exports.Save = Save

