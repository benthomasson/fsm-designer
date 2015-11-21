'''

Usage:
    fsm-designer [options]

Generate and validate an FSM implementation based on a FSM diagram.

Options:
    -h, --help          Show this page
    -v, --verbose       Enable verbose logging
    -d, --debug         Enable debug logging
'''


from docopt import docopt

import sys

import logging
logger = logging.getLogger('fsm_designer.cli')


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
    logger.debug("sys.argv %s", sys.argv)
    logger.debug("parsed_args %s", parsed_args)
