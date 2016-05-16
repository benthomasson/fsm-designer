'''

Usage:
    fsm-designer [options] generate-py <fsm-design> <output-module>
    fsm-designer [options] generate-js <fsm-design> <output-module>
    fsm-designer [options] validate <fsm-design> <module>
    fsm-designer [options] extract <module> <output-fsm-design>
    fsm-designer [options] diff <a> <b>

Generate and validate an FSM implementation based on a FSM diagram.

Options:
    -h, --help          Show this page
    -v, --verbose       Enable verbose logging
    -d, --debug         Enable debug logging
    --template=<t>      Template to use
'''


from docopt import docopt

import os
import sys
import yaml

from fsm import validate_design, generate_code, to_yaml, diff
from jinja2 import Environment, PackageLoader, FileSystemLoader
from conf import settings

import logging
logger = logging.getLogger('fsm_designer.cli')


class Module(object):

    class State(object):
        pass

    def __init__(self, name):
        self.__name__ = name


def generate(template, fsm_design, output_module):
    module_name = os.path.splitext(os.path.basename(output_module))[0]
    with open(fsm_design) as f:
        missing_states, missing_transitions = validate_design(yaml.load(f.read()), Module(module_name))
    code = generate_code(template, missing_states, missing_transitions)
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


def diff_yaml(a_file, b_file):
    with open(a_file) as af:
        a = yaml.load(af.read())
    with open(b_file) as bf:
        b = yaml.load(bf.read())
    missing_states, missing_transitions = diff(a or {}, b or {})
    return_value = 0
    if missing_states:
        print "Extra states in", a_file
        print "\n".join(list(missing_states))
        return_value = 1
    if missing_transitions:
        print "Extra transitions in", a_file
        print missing_transitions
        return_value = 1
    missing_states, missing_transitions = diff(b or {}, a or {})
    if missing_states:
        print "Extra states in", b_file
        print "\n".join(list(missing_states))
        return_value = 1
    if missing_transitions:
        print "Extra transitions in", b_file
        print missing_transitions
        return_value = 1
    return return_value


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
    if parsed_args['generate-py']:
        if parsed_args['--template']:
            env = Environment(loader=FileSystemLoader("."))
            template = env.get_template(parsed_args['--template'])
        else:
            env = Environment(loader=PackageLoader(*settings.TEMPLATES_PATH))
            template = env.get_template("fsm.pyt")
        generate(template, parsed_args['<fsm-design>'], parsed_args['<output-module>'])
    if parsed_args['generate-js']:
        if parsed_args['--template']:
            env = Environment(loader=FileSystemLoader("."))
            template = env.get_template(parsed_args['--template'])
        else:
            env = Environment(loader=PackageLoader(*settings.TEMPLATES_PATH))
            template = env.get_template("fsm.jst")
        generate(template, parsed_args['<fsm-design>'], parsed_args['<output-module>'])
    elif parsed_args['validate']:
        if validate(parsed_args['<fsm-design>'], parsed_args['<module>']):
            return 0
        else:
            return 1
    elif parsed_args['diff']:
        return diff_yaml(parsed_args['<a>'], parsed_args['<b>'])
    elif parsed_args['extract']:
        extract(parsed_args['<module>'], parsed_args['<output-fsm-design>'])
