var fsm = require('./fsm.js')

QUnit.test( "init controller", function( assert ) {
    var c = new fsm.Controller()
    assert.ok(c != null, "Passed!")
})


QUnit.test( "Change state", function( assert ) {
    var c = new fsm.Controller()
    fsm.Load.fileSelected(c)
    assert.equal(c.state, fsm.Ready, "woot!")
})
