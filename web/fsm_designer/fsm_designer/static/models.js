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
FSMTransition.prototype.is_selected = function (controller) {
    var x1 = this.from_state.x
    var y1 = this.from_state.y
    var x2 = this.to_state.x
    var y2 = this.to_state.y
    var x = controller.mousePX
    var y = controller.mousePY

    var dx = x2 - x1
    var dy = y2 - y1

    var d = sqrt(dx * dx + dy * dy)

    if (d === 0) {
        return false
    }

    var ca = dx / d
    var sa = dy / d

    var mX = (-x1 + x) * ca + (-y1 + y) * sa

    var result_x = null
    var result_y = null

    if (mX <= 0) {
        result_x = x1
        result_y = y1
    } else if (mX >= d) {
        result_x = x2
        result_y = y2
    } else {
        result_x = x1 + mX * ca
        result_y = y1 + mX * sa
    }

    dx = x - result_x
    dy = y - result_y
    var distance = sqrt(dx * dx + dy * dy)
    var line_atan = atan2(y2 - y1, x2 - x1)
    var pline_atan = atan2(result_y - y, result_x - x)
    if (controller.debug) {
        console.log('line_atan: ' + line_atan + 'pline_atan: ' + pline_atan)
        if (abs(line_atan) < PI / 2.0 && pline_atan < 0) {
            stroke(settings.COLOR)
        } else if (abs(line_atan) > PI / 2.0 && pline_atan < 0) {
            stroke(0)
        } else if (abs(line_atan) > PI / 2.0 && pline_atan > 0) {
            stroke(settings.COLOR)
        } else {
            stroke(0)
        }
        push()
        controller.scaleAndPan()
        line(x, y, result_x, result_y)
        pop()
    }
    var selected_distance = 0
    if (abs(line_atan) < PI / 2.0 && pline_atan < 0) {
        selected_distance = 10
    } else if (abs(line_atan) > PI / 2.0 && pline_atan < 0) {
        selected_distance = 10 + settings.TEXT_SIZE * (this.label_offset + 1.5)
    } else if (abs(line_atan) > PI / 2.0 && pline_atan > 0) {
        selected_distance = 10
    } else {
        selected_distance = 10 + settings.TEXT_SIZE * (this.label_offset + 1.5)
    }
    if (distance < selected_distance) {
        if (controller.debug) {
            stroke(settings.SELECTED_COLOR)
            push()
            controller.scaleAndPan()
            line(x, y, result_x, result_y)
            pop()
        }
        return true
    } else {
        return false
    }
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
    this.main_controller.changeState(fsm.Start)
    var view_controller = this.view_controller = new view_fsm.Controller()
    this.view_controller.application = this
    this.view_controller.changeState(view_fsm.Start)
    var menu_controller = this.menu_controller = new menu_fsm.Controller()
    this.menu_controller.application = this
    this.menu_controller.changeState(menu_fsm.Start)
    this.menu_controller.next_controller = this.main_controller
    this.main_controller.next_controller = this.view_controller
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

Application.prototype.scaleAndPan = function () {
    translate(this.panX, this.panY)
    scale(this.scaleXY)
}

Application.prototype.select_item = function () {
    this.selected_state = null
    this.selected_transition = null
    var i = 0
    var state = null
    var transition = null
    for (i = 0; i < this.states.length; i++) {
        state = this.states[i]
        if (state.is_selected(this) && this.selected_state === null) {
            state.selected = true
            this.selected_state = state
        } else {
            state.selected = false
        }
    }
    for (i = 0; i < this.transitions.length; i++) {
        transition = this.transitions[i]
        if (transition.is_selected(this) && this.selected_state === null) {
            transition.selected = true
            this.selected_transition = transition
        } else {
            transition.selected = false
        }
    }
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
        var from_right = 20
        noStroke()
        fill(0)
        var fps_string = 'fps: ' + frameRate().toFixed(0)
        text(fps_string, width - (from_right * textSize()), textSize())
        text('main state:' + this.main_controller.state.constructor.name, width - (from_right * textSize()), textSize() * 2)
        text('menu state:' + this.menu_controller.state.constructor.name, width - (from_right * textSize()), textSize() * 3)
        text('view state:' + this.view_controller.state.constructor.name, width - (from_right * textSize()), textSize() * 4)
        text('pcd:' + this.pointer_count_down, width - (from_right * textSize()), textSize() * 5)
        text('X, Y:' + mouseX + ', ' + mouseY, width - (from_right * textSize()), textSize() * 6)
        text('PX, PY:' + this.mousePX + ', ' + this.mousePY, width - (from_right * textSize()), textSize() * 7)
        text('key:' + key, width - (from_right * textSize()), textSize() * 8)
        text('keyCode:' + keyCode, width - (from_right * textSize()), textSize() * 9)
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
    this.menu_controller.state.mouseWheel(this.menu_controller, event)
}
Application.prototype.mouseDragged = function () {
    this.menu_controller.state.mouseDragged(this.menu_controller)
}
Application.prototype.mousePressed = function () {
    this.menu_controller.state.mousePressed(this.menu_controller)
}
Application.prototype.mouseReleased = function () {
    this.menu_controller.state.mouseReleased(this.menu_controller)
}
Application.prototype.keyTyped = function () {
    this.menu_controller.state.keyTyped(this.menu_controller)
}
Application.prototype.keyPressed = function () {
    this.menu_controller.state.keyPressed(this.menu_controller)
}
Application.prototype.keyReleased = function () {
    this.menu_controller.state.keyReleased(this.menu_controller)
}
exports.Application = Application
