'''

Usage:
    fsm-designer [options] generate <fsm-design> <output-module>
    fsm-designer [options] validate <fsm-design> <module>
    fsm-designer [options] extract <module> <output-fsm-design>

Generate and validate an FSM implementation based on a FSM diagram.

Options:
    -h, --help          Show this page
    -v, --verbose       Enable verbose logging
    -d, --debug         Enable debug logging
'''


from docopt import docopt

import os
import sys
import yaml

from fsm import validate_design, generate_code, to_yaml

import logging
logger = logging.getLogger('fsm_designer.cli')


class Module(object):

    def __init__(self, name):
        self.__name__ = name


def generate(fsm_design, output_module):
    module_name = os.path.splitext(os.path.basename(output_module))[0]
    with open(fsm_design) as f:
        missing_states, missing_transitions = validate_design(yaml.load(f.read()), Module(module_name))
    code = generate_code(missing_states, missing_transitions)
    with open(output_module, 'w') as f:
        f.write(code)


def _load_module(module_name):
    sys.path.append(os.getcwd())
    module = __import__(module_name)
    for part in module_name.split(".")[1:]:
        module = getattr(module, part)
    return module


def validate(fsm_design, module_name):
    module = _load_module(module_name)
    with open(fsm_design) as f:
        missing_states, missing_transitions = validate_design(yaml.load(f.read()), module)
    code = generate_code(missing_states, missing_transitions)
    if missing_states or missing_transitions:
        logger.error("FSM design validation failed for %s", module_name)
        logger.error("Add these states and transitions")
        print code
        return False
    else:
        logger.info("FSM design validation passed!")
        return True


def extract(module_name, output_fsm_design):
    module = _load_module(module_name)
    with open(output_fsm_design, 'w') as f:
        f.write(to_yaml(module))


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug('Debug logging enabled')
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
        logger.info('Verbose logging enabled')
    else:
        logging.basicConfig(level=logging.WARN)
    logger.debug("sys.argv %s", sys.argv)
    logger.debug("parsed_args %s", parsed_args)

    if parsed_args['generate']:
        generate(parsed_args['<fsm-design>'], parsed_args['<output-module>'])
    elif parsed_args['validate']:
        if validate(parsed_args['<fsm-design>'], parsed_args['<module>']):
            return 0
        else:
            return 1
    elif parsed_args['extract']:
        extract(parsed_args['<module>'], parsed_args['<output-fsm-design>'])
