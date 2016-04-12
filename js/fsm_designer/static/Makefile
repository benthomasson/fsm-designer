
.PHONY: all generate lint


all:
	browserify main.js  --standalone main > bundle.js

generate:
	fsm-designer generate-js ../../../fsm_designer/fsm_designer/design_fsm.yml fsm.js

lint:
	eslint fsm.js
