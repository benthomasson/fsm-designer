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
    controller.next_controller.state.keyPressed(controller)
}
_State.prototype.keyReleased = function (controller) {
}
var State = new _State()
exports.State = State
exports._State = _State

function _SelectedTransition () {
}
inherits(_SelectedTransition, _State)

_SelectedTransition.prototype.mousePressed = function (controller) {
    if (controller.application.selected_transition.is_selected(controller.application)) {
        controller.changeState(EditTransition)
    } else {
        controller.changeState(Ready)
        controller.state.mousePressed(controller)
    }
}
_SelectedTransition.prototype.mousePressed.transitions = ['EditTransition', 'Ready']

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
_SelectedTransition.prototype.keyPressed.transitions = ['Ready']

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

_Edit.prototype.keyTyped = function (controller) {
    if (this.handle_special_keys(controller)) {
        // do nothing
    } else {
        controller.application.selected_state.label += key
    }
}
_Edit.prototype.keyTyped.transitions = ['Selected']

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
_Edit.prototype.keyPressed.transitions = ['Selected']

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
_Edit.prototype.mousePressed.transitions = ['Selected', 'Ready']

_Edit.prototype.mouseDragged = function (controller) {
    controller.changeState(Move)
}
_Edit.prototype.mouseDragged.transitions = ['Move']

var Edit = new _Edit()
exports.Edit = Edit

function _Move () {
}
inherits(_Move, _State)

// transition to Selected
_Move.prototype.mouseReleased = function (controller) {
    controller.changeState(Selected)
}
_Move.prototype.mouseReleased.transitions = ['Selected']

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

function _Start () {
}
inherits(_Start, _State)

// transition to Ready
_Start.prototype.start = function (controller) {
    controller.changeState(Ready)
}
_Start.prototype.start.transitions = ['Ready']

var Start = new _Start()
exports.Start = Start

function _Ready () {
}
inherits(_Ready, _State)

// transition to SelectedTransition
// transition to Selected
_Ready.prototype.mousePressed = function (controller) {
    controller.application.select_item()
    if (controller.application.selected_property != null) {
        controller.changeState(EditProperty)
    } else if (controller.application.selected_state != null) {
        controller.changeState(Selected)
    } else if (controller.application.selected_transition != null) {
        controller.changeState(SelectedTransition)
    } else {
        controller.next_controller.state.mousePressed(controller.next_controller)
    }
}
_Ready.prototype.mousePressed.transitions = ['EditProperty', 'SelectedTransition', 'Selected']

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

_Selected.prototype.mousePressed = function (controller) {
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
_Selected.prototype.mousePressed.transitions = ['Ready', 'Edit']

_Selected.prototype.mouseDragged = function (controller) {
    if (controller.application.selected_state === null) {
        controller.changeState(Ready)
        controller.mousePressed(controller)
    }
    controller.changeState(Move)
    controller.state.mouseDragged(controller)
}
_Selected.prototype.mouseDragged.transitions = ['Ready', 'Move']

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
_Selected.prototype.keyPressed.transitions = ['Ready']

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
_EditTransition.prototype.keyPressed.transitions = ['SelectedTransition']

_EditTransition.prototype.mousePressed = function (controller) {
    controller.changeState(Ready)
}
_EditTransition.prototype.mousePressed.transitions = ['Ready']

var EditTransition = new _EditTransition()
exports.EditTransition = EditTransition

function _EditProperty () {
}
inherits(_EditProperty, _State)

_EditProperty.prototype.start = function (controller) {
    controller.application.selected_property.edit = true
}

_EditProperty.prototype.end = function (controller) {
    controller.application.selected_property.object[controller.application.selected_property.property] = controller.application.selected_property.label
    controller.application.selected_property.edit = false
    controller.application.selected_property.selected = false
    controller.application.selected_property = null
}

// transition to Ready
_EditProperty.prototype.keyTyped = function (controller) {
    if (this.handle_special_keys(controller)) {
        // do nothing
    } else {
        controller.application.selected_property.label += key
    }
}

_EditProperty.prototype.handle_special_keys = function (controller) {
    if (keyCode === RETURN) {
        controller.changeState(Ready)
        return true
    } else if (keyCode === ENTER) {
        controller.changeState(Ready)
        return true
    } else if (keyCode === BACKSPACE) {
        controller.application.selected_property.label = controller.application.selected_property.label.substring(0, controller.application.selected_property.label.length - 1)
        return true
    } else if (keyCode === DELETE) {
        controller.application.selected_property.label = controller.application.selected_property.label.substring(0, controller.application.selected_property.label.length - 1)
        return true
    } else {
        return false
    }
}

_EditProperty.prototype.keyPressed = _EditProperty.prototype.handle_special_keys
_EditProperty.prototype.keyPressed.transitions = ['Ready']

// transition to Ready
_EditProperty.prototype.mousePressed = function (controller) {
    controller.changeState(Ready)
    controller.state.mousePressed(controller)
}
_EditProperty.prototype.mousePressed.transitions = ['Ready']

var EditProperty = new _EditProperty()
exports.EditProperty = EditProperty
