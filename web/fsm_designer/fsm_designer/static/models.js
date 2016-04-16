var fsm = require('./fsm.js')
var settings = require('./settings.js')
var widgets = require('./widgets.js')
var view_fsm = require('./view_fsm.js')
var menu_fsm = require('./menu_fsm.js')

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
    var main_controller = this.main_controller = new fsm.Controller()
    this.main_controller.application = this
    var view_controller = this.view_controller = new view_fsm.Controller()
    this.view_controller.state = view_fsm.ViewReady
    this.view_controller.application = this
    var menu_controller = this.menu_controller = new menu_fsm.Controller()
    this.menu_controller.state = menu_fsm.MenuReady
    this.menu_controller.application = this
    this.states = []
    this.transitions = []
    this.panX = 0
    this.panY = 0
    this.oldPanX = 0
    this.oldPanY = 0
    this.scaleXY = 1.0
    this.oldScaleXY = 0
    this.mouseSX = 0
    this.mouseSY = 0
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
    this.MoveMousePointer = new widgets.MoveMousePointer()
    this.MagnifyingGlassMousePointer = new widgets.MagnifyingGlassMousePointer()
    this.ArrowMousePointer = new widgets.ArrowMousePointer()
    this.pointer_count_down = null
    this.mousePointer = this.ArrowMousePointer

    var load_button = new widgets.Button()
    var save_button = new widgets.Button()
    var new_state_button = new widgets.Button()
    var new_transition_button = new widgets.Button()
    this.bar = new widgets.ButtonBar()
    this.bar.buttons.push(load_button)
    this.bar.buttons.push(save_button)
    this.bar.buttons.push(new_state_button)
    this.bar.buttons.push(new_transition_button)

    this.active_widgets.push(load_button)
    this.active_widgets.push(save_button)
    this.active_widgets.push(new_state_button)
    this.active_widgets.push(new_transition_button)

    load_button.label = 'Load'
    save_button.label = 'Save'
    new_state_button.label = 'New State'
    new_transition_button.label = 'New Transition'

    load_button.call_back = function () {
        menu_controller.state.load_button(menu_controller)
    }
    save_button.call_back = function () {
        menu_controller.state.save_button(menu_controller)
    }
    new_state_button.call_back = function () {
        menu_controller.state.new_state_button(menu_controller)
    }
    new_transition_button.call_back = function () {
        menu_controller.state.new_transition_button(menu_controller)
    }

    this.bar.x = 10
    this.bar.y = 10
}

Application.prototype.save = function (button) {
}

Application.prototype.load = function (button) {
}

Application.prototype.generate = function (button) {
}

Application.prototype.validate = function (button) {
}

Application.prototype.draw_content = function (controller) {
    var i = 0
    for (i = 0; i < this.transitions.length; i++) {
        this.transitions[i].draw(controller)
    }
    for (i = 0; i < this.states.length; i++) {
        this.states[i].draw(controller)
    }
}

Application.prototype.draw_menus = function (controller) {
    this.bar.draw(controller)
    if (this.debug) {
        var from_right = 5
        noStroke()
        fill(0)
        var fps_string = 'fps: ' + frameRate().toFixed(0)
        text(fps_string, width - (from_right * textSize()), textSize())
        text('state:' + this.state, width - (from_right * textSize()), textSize() * 2)
        text('pcd:' + this.pointer_count_down, width - (from_right * textSize()), textSize() * 3)
    }

    if (this.pointer_count_down === null) {
        // do nothing
    } else if (this.pointer_count_down <= 1) {
        this.mousePointer = this.ArrowMousePointer
        this.pointer_count_down = null
    } else {
        this.pointer_count_down -= 1
    }

    if (this.mousePointer) {
        this.mousePointer.draw()
    }

    var widget = null

    for (var i = 0; i < controller.active_widgets.length; i++) {
        widget = controller.active_widgets[i]
        if (mouseX > widget.left_extent() &&
                mouseX < widget.right_extent() &&
                mouseY > widget.top_extent() &&
                mouseY < widget.bottom_extent()) {
            widget.mouseOver()
        } else {
            widget.mouseOut()
            widget.mouseReleased()
        }
    }
}

Application.prototype.mouseWheel = function (event) {
    this.view_controller.state.mouseWheel(this.view_controller, event)
}
Application.prototype.mouseDragged = function () {
    this.view_controller.state.mouseDragged(this.view_controller)
}
Application.prototype.mousePressed = function () {
    this.menu_controller.state.mousePressed(this.menu_controller)
}
Application.prototype.mouseReleased = function () {
    this.menu_controller.state.mouseReleased(this.menu_controller)
}
exports.Application = Application
