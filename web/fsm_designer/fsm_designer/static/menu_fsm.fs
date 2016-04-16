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
_Load.prototype. = function (controller) {

    controller.changeState(MenuReady)
}

var Load = new _Load()
exports.Load = Load

function _NewState () {
}
inherits(_NewState, _State)

// transition to MenuReady
_NewState.prototype. = function (controller) {

    controller.changeState(MenuReady)
}

var NewState = new _NewState()
exports.NewState = NewState

function _NewTransition () {
}
inherits(_NewTransition, _State)

// transition to MenuReady
_NewTransition.prototype. = function (controller) {

    controller.changeState(MenuReady)
}

var NewTransition = new _NewTransition()
exports.NewTransition = NewTransition

function _MenuReady () {
}
inherits(_MenuReady, _State)

// transition to NewState
// transition to Load
// transition to NewTransition
// transition to Save
_MenuReady.prototype. = function (controller) {

    controller.changeState(NewState)

    controller.changeState(Load)

    controller.changeState(NewTransition)

    controller.changeState(Save)
}

var MenuReady = new _MenuReady()
exports.MenuReady = MenuReady

function _Save () {
}
inherits(_Save, _State)

// transition to MenuReady
_Save.prototype. = function (controller) {

    controller.changeState(MenuReady)
}

var Save = new _Save()
exports.Save = Save

