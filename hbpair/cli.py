"""
hbpair

Usage:
    hbpair -h | --help
    hbpair --version
    hbpair push [-a | <sheet-name>]

Options:
    -a --all  Push all sheets

Examples:
    hbpair push Week\ 1 
"""


from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION

def main():
    NOT_COMMANDS = set(['Base', 'AllPairs'])

    import commands
    options = docopt(__doc__, version=VERSION)

    for (k, v) in options.items():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands
                       if command[0] not in NOT_COMMANDS][0]
            command = command(options)
            command.run()
