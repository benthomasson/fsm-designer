
.PHONY: all generate lint


all: main test

main:
	browserify main.js  --standalone main > bundle.js

test:
	browserify test.js  --standalone test > test_bundle.js


generate:
	fsm-designer generate-js ../../../fsm_designer/fsm_designer/design_fsm.yml fsm.js

lint:
	eslint fsm.js
