"""
hbpair

Usage:
    hbpair -h | --help
    hbpair --version
    hbpair update (<source-csv> <updater-csv>)

Examples:
    hbpair update all-pairs.csv pairs-wk4.csv
"""


from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION

def main():
    import commands
    options = docopt(__doc__, version=VERSION)

    for (k, v) in options.items():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            print 'Commands:'
            print commands
            command = [command[1] for command in commands 
                       if command[0] != 'Base' and command[0] != 'AllPairs'][0]
            command = command(options)
            command.run()
