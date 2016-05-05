var inherits = require('inherits')
var models = require('./models.js')

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
}
_State.prototype.start = function (controller) {
}
_State.prototype.end = function (controller) {
}
_State.prototype.keyPressed = function (controller) {
}
_State.prototype.keyReleased = function (controller) {
}
var State = new _State()
exports.State = State
exports._State = _State

function _Start () {
}
inherits(_Start, _State)
var Start = new _Start()

_Start.prototype.start = function (controller) {
    controller.changeState(MenuReady)
}
_Start.prototype.start.transitions = ['MenuReady']
exports.Start = Start

function _Load () {
}
inherits(_Load, _State)

_Load.prototype.start = function (controller) {
    window.open('/static/upload.html', '_self')
    controller.changeState(MenuReady)
}
_Load.prototype.start.transitions = ['MenuReady']

var Load = new _Load()
exports.Load = Load

function _NewState () {
}
inherits(_NewState, _State)

_NewState.prototype.start = function (controller) {
    controller.application.mousePointer = controller.application.NewStatePointer
}

_NewState.prototype.mousePressed = function (controller) {
    controller.application.mousePointer = controller.application.ArrowMousePointer
    var new_state = new models.FSMState()
    new_state.x = controller.application.mousePX
    new_state.y = controller.application.mousePY
    new_state.label = controller.application.NewStatePointer.label
    controller.application.states.push(new_state)
    controller.changeState(MenuReady)
}
_NewState.prototype.mousePressed.transitions = ['MenuReady']

var NewState = new _NewState()
exports.NewState = NewState

function _NewTransition () {
}
inherits(_NewTransition, _State)

_NewTransition.prototype.start = function (controller) {
    controller.application.mousePointer = controller.application.NewTransitionPointer
}

_NewTransition.prototype.mousePressed = function (controller) {
    controller.application.select_state()
    if (controller.application.selected_state) {
        controller.changeState(ConnectTransition)
    } else {
        controller.application.mousePointer = controller.application.ArrowMousePointer
        controller.changeState(MenuReady)
    }
}
_NewTransition.prototype.mousePressed.transitions = ['MenuReady', 'ConnectTransition']

var NewTransition = new _NewTransition()
exports.NewTransition = NewTransition

function _ConnectTransition () {
}
inherits(_ConnectTransition, _State)

_ConnectTransition.prototype.start = function (controller) {
    var new_transition = new models.FSMTransition()
    new_transition.selected = true
    new_transition.from_state = controller.application.selected_state
    controller.application.selected_state.selected = false
    controller.application.selected_state = null
    controller.application.selected_transition = new_transition
    controller.application.transitions.push(new_transition)
}

_ConnectTransition.prototype.mousePressed = function (controller) {
    controller.application.select_state()
    if (controller.application.selected_state) {
        controller.application.selected_transition.to_state = controller.application.selected_state
        controller.application.selected_state.selected = false
        controller.application.selected_state = null
        controller.application.selected_transition.selected = false
        controller.application.selected_transition = null
        controller.application.mousePointer = controller.application.ArrowMousePointer
        controller.changeState(MenuReady)
    } else {
        controller.application.transitions.pop()
        controller.application.mousePointer = controller.application.ArrowMousePointer
        controller.changeState(MenuReady)
    }
}
_ConnectTransition.prototype.mousePressed.transitions = ['MenuReady']

var ConnectTransition = new _ConnectTransition()
exports.ConnectTransition = ConnectTransition

function _MenuReady () {
}
inherits(_MenuReady, _State)

_MenuReady.prototype.new_state_button = function (controller) {
    controller.changeState(NewState)
}
_MenuReady.prototype.new_state_button.transitions = ['NewState']

_MenuReady.prototype.load_button = function (controller) {
    controller.changeState(Load)
}
_MenuReady.prototype.load_button.transitions = ['Load']

_MenuReady.prototype.new_transition_button = function (controller) {
    controller.changeState(NewTransition)
}
_MenuReady.prototype.new_transition_button.transitions = ['NewTransition']

_MenuReady.prototype.save_button = function (controller) {
    controller.changeState(Save)
}
_MenuReady.prototype.save_button.transitions = ['Save']

_MenuReady.prototype.mousePressed = function (controller) {
    var widget = null
    for (var i = 0; i < controller.application.active_widgets.length; i++) {
        widget = controller.application.active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mousePressed()
            return
        }
    }
    controller.next_controller.state.mousePressed(controller.next_controller)
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
    controller.next_controller.state.mouseReleased(controller.next_controller)
}

_MenuReady.prototype.mouseWheel = function (controller, event) {
    controller.next_controller.state.mouseWheel(controller.next_controller, event)
}
_MenuReady.prototype.mouseDragged = function (controller) {
    controller.next_controller.state.mouseDragged(controller.next_controller)
}
_MenuReady.prototype.keyTyped = function (controller) {
    controller.next_controller.state.keyTyped(controller.next_controller)
}
_MenuReady.prototype.keyPressed = function (controller) {
    controller.next_controller.state.keyPressed(controller.next_controller)
}
_MenuReady.prototype.keyReleased = function (controller) {
    controller.next_controller.state.keyReleased(controller.next_controller)
}

var MenuReady = new _MenuReady()
exports.MenuReady = MenuReady

function _Save () {
}
inherits(_Save, _State)

_Save.prototype.start = function (controller) {
    console.log(controller.application.exportFSM())
    controller.application.socket.emit('save', controller.application.exportFSM())
}

_Save.prototype.on_saved = function (controller, message) {
    console.log(message)
    controller.application.last_saved_url = message.url
    controller.changeState(Saved)
}
_Save.prototype.on_saved.transitions = ['Saved']

var Save = new _Save()
exports.Save = Save

function _Saved () {
}
inherits(_Saved, _State)

_Saved.prototype.start = function (controller) {
    if (controller.application.last_saved_url != null) {
        window.open(controller.application.last_saved_url)
        controller.application.last_saved_url = null
    }
    controller.changeState(MenuReady)
}
_Saved.prototype.start.transitions = ['MenuReady']

var Saved = new _Saved()
exports.Saved = Saved
