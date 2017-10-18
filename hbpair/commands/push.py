from .base import Base
from .AllPairs import AllPairs

class Push(Base):

    def run(self):
        options = self.options
        if options['--all']:
            print 'Updating All Pairs with all available sheets...'

            AllPairs.from_gsheets(
                'All Pairs'
            ).update_with_all_gsheets().push_to_gsheets('All Pairs')

        else:
            print 'Updating All Pairs with {}'.format(options['<sheet-name>'])

            AllPairs.from_gsheets(
                'All Pairs'
            ).update_with_gsheets(
                options['<sheet-name>']
            ).push_to_gsheets('All Pairs')

        print 'Done!'
