var inherits= require('inherits')

function Controller () {
    this.state = null

}
exports.Controller = Controller

Controller.prototype.changeState = function(state) {
    console.log('changeState: ' + state.constructor.name);
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

// transition to Ready
_Load.prototype.fileSelected = function (controller) {

    controller.changeState(Ready)
}
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

    controller.changeState(EditTransition)

    controller.changeState(MenuWheel)

    controller.changeState(Ready)
}
var SelectedTransition = new _SelectedTransition()
exports.SelectedTransition = SelectedTransition


function _Edit () {
}
inherits(_Edit, _State)

// transition to Selected
_Edit.prototype.keyTyped = function (controller) {

    controller.changeState(Selected)
}
var Edit = new _Edit()
exports.Edit = Edit

// transition to Selected
// transition to Ready
_Edit.prototype.mousePressed = function (controller) {

    controller.changeState(Selected)

    controller.changeState(Ready)
}
var Edit = new _Edit()
exports.Edit = Edit

// transition to NewTransition
_Edit.prototype.mouseDragged = function (controller) {

    controller.changeState(NewTransition)
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


function _Ready () {
}
inherits(_Ready, _State)

// transition to ScaleAndPan
// transition to SelectedTransition
// transition to Selected
// transition to MenuWheel
_Ready.prototype.mousePressed = function (controller) {

    controller.changeState(ScaleAndPan)

    controller.changeState(SelectedTransition)

    controller.changeState(Selected)

    controller.changeState(MenuWheel)
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

    controller.changeState(MenuWheel)

    controller.changeState(Ready)

    controller.changeState(Move)

    controller.changeState(Edit)
}
var Selected = new _Selected()
exports.Selected = Selected

// transition to Move
// transition to NewTransition
_Selected.prototype.mouseDragged = function (controller) {

    controller.changeState(Move)

    controller.changeState(NewTransition)
}
var Selected = new _Selected()
exports.Selected = Selected


function _EditTransition () {
}
inherits(_EditTransition, _State)

// transition to SelectedTransition
_EditTransition.prototype.keyTyped = function (controller) {

    controller.changeState(SelectedTransition)
}
var EditTransition = new _EditTransition()
exports.EditTransition = EditTransition

// transition to Ready
// transition to SelectedTransition
_EditTransition.prototype.mousePressed = function (controller) {

    controller.changeState(Ready)

    controller.changeState(SelectedTransition)
}
var EditTransition = new _EditTransition()
exports.EditTransition = EditTransition


