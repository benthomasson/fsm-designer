var inherits= require('inherits')

function Controller () {
    this.state = null

}
exports.Controller = Controller

Controller.prototype.changeState = function(state) {
    if (this.state != null) {
        this.state.end(this)
    }
    this.state = state
    if (this.state != null) {
        this.state.start(this)
    }
}

function BaseState () {
}
exports.BaseState = BaseState

inherits(Load, BaseState)

function Load () {
}
exports.Load = Load

Load.prototype.start = function (controller) {
}
Load.prototype.end = function (controller) {
}
// transition to Ready
Load.prototype.fileSelected = function (controller) {

    controller.changeState(Ready)
}


function Save () {
}
exports.Save = Save

Save.prototype.start = function (controller) {
}
Save.prototype.end = function (controller) {
}
// transition to Ready
Save.prototype.fileSelected = function (controller) {

    controller.changeState(Ready)
}


function SelectedTransition () {
}
exports.SelectedTransition = SelectedTransition

SelectedTransition.prototype.start = function (controller) {
}
SelectedTransition.prototype.end = function (controller) {
}
// transition to EditTransition
SelectedTransition.prototype.start = function (controller) {
}
SelectedTransition.prototype.end = function (controller) {
}
// transition to MenuWheel
SelectedTransition.prototype.start = function (controller) {
}
SelectedTransition.prototype.end = function (controller) {
}
// transition to Ready
SelectedTransition.prototype.mousePressed = function (controller) {

    controller.changeState(EditTransition)

    controller.changeState(MenuWheel)

    controller.changeState(Ready)
}


function Edit () {
}
exports.Edit = Edit

Edit.prototype.start = function (controller) {
}
Edit.prototype.end = function (controller) {
}
// transition to Selected
Edit.prototype.keyTyped = function (controller) {

    controller.changeState(Selected)
}

Edit.prototype.start = function (controller) {
}
Edit.prototype.end = function (controller) {
}
// transition to Selected
Edit.prototype.start = function (controller) {
}
Edit.prototype.end = function (controller) {
}
// transition to Ready
Edit.prototype.mousePressed = function (controller) {

    controller.changeState(Selected)

    controller.changeState(Ready)
}

Edit.prototype.start = function (controller) {
}
Edit.prototype.end = function (controller) {
}
// transition to NewTransition
Edit.prototype.mouseDragged = function (controller) {

    controller.changeState(NewTransition)
}


function NewState () {
}
exports.NewState = NewState

NewState.prototype.start = function (controller) {
}
NewState.prototype.end = function (controller) {
}
// transition to Ready
NewState.prototype.start = function (controller) {

    controller.changeState(Ready)
}


function NewTransition () {
}
exports.NewTransition = NewTransition

NewTransition.prototype.start = function (controller) {
}
NewTransition.prototype.end = function (controller) {
}
// transition to Selected
NewTransition.prototype.mouseReleased = function (controller) {

    controller.changeState(Selected)
}


function Move () {
}
exports.Move = Move

Move.prototype.start = function (controller) {
}
Move.prototype.end = function (controller) {
}
// transition to Selected
Move.prototype.mouseReleased = function (controller) {

    controller.changeState(Selected)
}


function ScaleAndPan () {
}
exports.ScaleAndPan = ScaleAndPan

ScaleAndPan.prototype.start = function (controller) {
}
ScaleAndPan.prototype.end = function (controller) {
}
// transition to Ready
ScaleAndPan.prototype.mouseReleased = function (controller) {

    controller.changeState(Ready)
}


function Start () {
}
exports.Start = Start

Start.prototype.start = function (controller) {
}
Start.prototype.end = function (controller) {
}
// transition to Ready
Start.prototype.start = function (controller) {

    controller.changeState(Ready)
}


function MenuWheel () {
}
exports.MenuWheel = MenuWheel

MenuWheel.prototype.start = function (controller) {
}
MenuWheel.prototype.end = function (controller) {
}
// transition to NewState
MenuWheel.prototype.start = function (controller) {
}
MenuWheel.prototype.end = function (controller) {
}
// transition to Save
MenuWheel.prototype.start = function (controller) {
}
MenuWheel.prototype.end = function (controller) {
}
// transition to Ready
MenuWheel.prototype.start = function (controller) {
}
MenuWheel.prototype.end = function (controller) {
}
// transition to Load
MenuWheel.prototype.mouseReleased = function (controller) {

    controller.changeState(NewState)

    controller.changeState(Save)

    controller.changeState(Ready)

    controller.changeState(Load)
}



function Ready () {
}
exports.Ready = Ready

Ready.prototype.start = function (controller) {
}
Ready.prototype.end = function (controller) {
}
// transition to ScaleAndPan
Ready.prototype.start = function (controller) {
}
Ready.prototype.end = function (controller) {
}
// transition to SelectedTransition
Ready.prototype.start = function (controller) {
}
Ready.prototype.end = function (controller) {
}
// transition to Selected
Ready.prototype.start = function (controller) {
}
Ready.prototype.end = function (controller) {
}
// transition to MenuWheel
Ready.prototype.mousePressed = function (controller) {

    controller.changeState(ScaleAndPan)

    controller.changeState(SelectedTransition)

    controller.changeState(Selected)

    controller.changeState(MenuWheel)
}


function Selected () {
}
exports.Selected = Selected

Selected.prototype.start = function (controller) {
}
Selected.prototype.end = function (controller) {
}
// transition to MenuWheel
Selected.prototype.start = function (controller) {
}
Selected.prototype.end = function (controller) {
}
// transition to Ready
Selected.prototype.start = function (controller) {
}
Selected.prototype.end = function (controller) {
}
// transition to Move
Selected.prototype.start = function (controller) {
}
Selected.prototype.end = function (controller) {
}
// transition to Edit
Selected.prototype.mousePressed = function (controller) {

    controller.changeState(MenuWheel)

    controller.changeState(Ready)

    controller.changeState(Move)

    controller.changeState(Edit)
}

Selected.prototype.start = function (controller) {
}
Selected.prototype.end = function (controller) {
}
// transition to Move
Selected.prototype.start = function (controller) {
}
Selected.prototype.end = function (controller) {
}
// transition to NewTransition
Selected.prototype.mouseDragged = function (controller) {

    controller.changeState(Move)

    controller.changeState(NewTransition)
}


function EditTransition () {
}
exports.EditTransition = EditTransition

EditTransition.prototype.start = function (controller) {
}
EditTransition.prototype.end = function (controller) {
}
// transition to SelectedTransition
EditTransition.prototype.keyTyped = function (controller) {

    controller.changeState(SelectedTransition)
}

EditTransition.prototype.start = function (controller) {
}
EditTransition.prototype.end = function (controller) {
}
// transition to Ready
EditTransition.prototype.start = function (controller) {
}
EditTransition.prototype.end = function (controller) {
}
// transition to SelectedTransition
EditTransition.prototype.mousePressed = function (controller) {

    controller.changeState(Ready)

    controller.changeState(SelectedTransition)
}


