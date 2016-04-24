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
}
_State.prototype.start = function (controller) {
}
_State.prototype.end = function (controller) {
}
_State.prototype.mousePressed = function (controller) {
}
_State.prototype.mouseWheel = function (controller) {
}
_State.prototype.mouseDragged = function (controller) {
}
_State.prototype.mouseReleased = function (controller) {
}
_State.prototype.keyTyped = function (controller) {
}
_State.prototype.keyPressed = function (controller) {
}
_State.prototype.keyReleased = function (controller) {
}
var State = new _State()
exports.State = State
exports._State = _State

function _Load () {
}
inherits(_Load, _State)

// transition to Ready
_Load.prototype.fileSelected = function (controller) {
    controller.changeState(Ready)
}
_Load.prototype.fileSelected.transitions = []
_Load.prototype.fileSelected.transitions.push('Ready')

var Load = new _Load()
exports.Load = Load

function _Save () {
}
inherits(_Save, _State)

// transition to Ready
_Save.prototype.fileSelected = function (controller) {
    controller.changeState(Ready)
}

var Save = new _Save()
exports.Save = Save

function _SelectedTransition () {
}
inherits(_SelectedTransition, _State)

// transition to EditTransition
// transition to MenuWheel
// transition to Ready
_SelectedTransition.prototype.mousePressed = function (controller) {
    if (controller.application.selected_transition.is_selected(controller.application)) {
        controller.changeState(EditTransition)
    } else {
        controller.changeState(Ready)
        controller.state.mousePressed(controller)
    }
}

_SelectedTransition.prototype.keyPressed = function (controller) {
    console.log('keyPressed')
    if (keyCode === BACKSPACE) {
        controller.application.remove_transition(controller.application.selected_transition)
        controller.application.selected_transition = null
        controller.changeState(Ready)
    } else if (keyCode === DELETE) {
        controller.application.remove_transition(controller.application.selected_transition)
        controller.application.selected_transition = null
        controller.changeState(Ready)
    }
}

var SelectedTransition = new _SelectedTransition()
exports.SelectedTransition = SelectedTransition

function _Edit () {
}
inherits(_Edit, _State)

_Edit.prototype.start = function (controller) {
    controller.application.selected_state.edit = true
}

_Edit.prototype.end = function (controller) {
    controller.application.selected_state.edit = false
}

// transition to Selected
_Edit.prototype.keyTyped = function (controller) {
    if (this.handle_special_keys(controller)) {
        // do nothing
    } else {
        controller.application.selected_state.label += key
    }
}

_Edit.prototype.handle_special_keys = function (controller) {
    if (keyCode === RETURN) {
        controller.changeState(Selected)
        return true
    } else if (keyCode === ENTER) {
        controller.changeState(Selected)
        return true
    } else if (keyCode === BACKSPACE) {
        controller.application.selected_state.label = controller.application.selected_state.label.substring(0, controller.application.selected_state.label.length - 1)
        return true
    } else if (keyCode === DELETE) {
        controller.application.selected_state.label = controller.application.selected_state.label.substring(0, controller.application.selected_state.label.length - 1)
        return true
    } else {
        return false
    }
}

_Edit.prototype.keyPressed = _Edit.prototype.handle_special_keys

// transition to Selected
// transition to Ready
_Edit.prototype.mousePressed = function (controller) {
    if (controller.application.selected_state.is_selected(controller.application)) {
        controller.changeState(Selected)
    } else {
        controller.changeState(Ready)
        controller.state.mousePressed(controller)
    }
}

// transition to NewTransition
_Edit.prototype.mouseDragged = function (controller) {
    controller.changeState(Move)
}

var Edit = new _Edit()
exports.Edit = Edit

function _NewState () {
}
inherits(_NewState, _State)

// transition to Ready
_NewState.prototype.start = function (controller) {
    controller.changeState(Ready)
}

var NewState = new _NewState()
exports.NewState = NewState

function _NewTransition () {
}
inherits(_NewTransition, _State)

// transition to Selected
_NewTransition.prototype.mouseReleased = function (controller) {
    controller.changeState(Selected)
}

var NewTransition = new _NewTransition()
exports.NewTransition = NewTransition

function _Move () {
}
inherits(_Move, _State)

// transition to Selected
_Move.prototype.mouseReleased = function (controller) {
    controller.changeState(Selected)
}

_Move.prototype.start = function (controller) {
    controller.application.mousePointer = controller.application.MoveMousePointer
}

_Move.prototype.end = function (controller) {
    controller.application.mousePointer = controller.application.ArrowMousePointer
}

_Move.prototype.mouseDragged = function (controller) {
    controller.application.selected_state.x = controller.application.mousePX
    controller.application.selected_state.y = controller.application.mousePY
}

var Move = new _Move()
exports.Move = Move

function _ScaleAndPan () {
}
inherits(_ScaleAndPan, _State)

// transition to Ready
_ScaleAndPan.prototype.mouseReleased = function (controller) {
    controller.changeState(Ready)
}

var ScaleAndPan = new _ScaleAndPan()
exports.ScaleAndPan = ScaleAndPan

function _Start () {
}
inherits(_Start, _State)

// transition to Ready
_Start.prototype.start = function (controller) {
    controller.changeState(Ready)
}

var Start = new _Start()
exports.Start = Start

function _MenuWheel () {
}
inherits(_MenuWheel, _State)

// transition to NewState
// transition to Save
// transition to Ready
// transition to Load
_MenuWheel.prototype.mouseReleased = function (controller) {
    controller.changeState(NewState)
    controller.changeState(Save)
    controller.changeState(Ready)
    controller.changeState(Load)
}

var MenuWheel = new _MenuWheel()
exports.MenuWheel = MenuWheel

function _BaseState () {
}
inherits(_BaseState, _State)

var BaseState = new _BaseState()
exports.BaseState = BaseState

function _Ready () {
}
inherits(_Ready, _State)

// transition to SelectedTransition
// transition to Selected
_Ready.prototype.mousePressed = function (controller) {
    controller.application.select_item()
    if (controller.application.selected_state != null) {
        controller.changeState(Selected)
    } else if (controller.application.selected_transition != null) {
        controller.changeState(SelectedTransition)
    }
}

_Ready.prototype.mouseWheel = function (controller, event) {
    controller.next_controller.state.mouseWheel(controller.next_controller, event)
}

_Ready.prototype.mouseDragged = function (controller) {
    controller.next_controller.state.mouseDragged(controller.next_controller)
}

_Ready.prototype.mouseReleased = function (controller) {
    controller.next_controller.state.mouseReleased(controller.next_controller)
}

var Ready = new _Ready()
exports.Ready = Ready

function _Selected () {
}
inherits(_Selected, _State)

// transition to MenuWheel
// transition to Ready
// transition to Move
// transition to Edit
_Selected.prototype.mousePressed = function (controller) {
    // controller.changeState(MenuWheel)
    // controller.changeState(Ready)
    // controller.changeState(Move)
    if (controller.application.selected_state === null) {
        controller.changeState(Ready)
        controller.mousePressed(controller)
    }
    if (controller.application.selected_state.is_selected(controller.application)) {
        controller.changeState(Edit)
    } else {
        controller.changeState(Ready)
        controller.state.mousePressed(controller)
    }
}

// transition to Move
// transition to NewTransition
_Selected.prototype.mouseDragged = function (controller) {
    if (controller.application.selected_state === null) {
        controller.changeState(Ready)
        controller.mousePressed(controller)
    }
    controller.changeState(Move)
    controller.state.mouseDragged(controller)
}

_Selected.prototype.keyPressed = function (controller) {
    console.log('keyPressed')
    if (keyCode === BACKSPACE) {
        controller.application.remove_state(controller.application.selected_state)
        controller.application.selected_state = null
        controller.changeState(Ready)
    } else if (keyCode === DELETE) {
        controller.application.remove_state(controller.application.selected_state)
        controller.application.selected_state = null
        controller.changeState(Ready)
    }
}

var Selected = new _Selected()
exports.Selected = Selected

function _EditTransition () {
}
inherits(_EditTransition, _State)

_EditTransition.prototype.start = function (controller) {
    controller.application.selected_transition.edit = true
}

_EditTransition.prototype.end = function (controller) {
    controller.application.selected_transition.edit = false
}

// transition to SelectedTransition
_EditTransition.prototype.keyTyped = function (controller) {
    if (this.handle_special_keys(controller)) {
        // do nothing
    } else {
        controller.application.selected_transition.label += key
    }
}

_EditTransition.prototype.handle_special_keys = function (controller) {
    if (keyCode === RETURN) {
        controller.changeState(SelectedTransition)
        return true
    } else if (keyCode === ENTER) {
        controller.changeState(SelectedTransition)
        return true
    } else if (keyCode === BACKSPACE) {
        controller.application.selected_transition.label = controller.application.selected_transition.label.substring(0, controller.application.selected_transition.label.length - 1)
        return true
    } else if (keyCode === DELETE) {
        controller.application.selected_transition.label = controller.application.selected_transition.label.substring(0, controller.application.selected_transition.label.length - 1)
        return true
    } else {
        return false
    }
}

_EditTransition.prototype.keyPressed = _EditTransition.prototype.handle_special_keys

// transition to Ready
// transition to SelectedTransition
_EditTransition.prototype.mousePressed = function (controller) {
    controller.changeState(Ready)
    // controller.changeState(SelectedTransition)
}

var EditTransition = new _EditTransition()
exports.EditTransition = EditTransition

