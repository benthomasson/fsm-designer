
.PHONY: all generate lint


all: main test

main:
	browserify main.js  --standalone main > bundle.js

test:
	browserify test.js  --standalone test > test_bundle.js

generate-fsm:
	fsm-designer generate-js ../../../fsm_designer/fsm_designer/design_fsm.yml fsm.js

generate-button-fsm:
	fsm-designer generate-js ../../../fsm_designer/processing_widgets/button_fsm.yml button_fsm.js

lint:
	eslint fsm.js models.js widgets.js settings.js button_fsm.js
