from .base import Base
from .AllPairs import AllPairs

class Push(Base):

    def run(self):
        options = self.options
        all_pairs = AllPairs.from_gsheets('All Pairs')
        all_pairs.update_with_gsheets(options['<sheet-name>'])
        all_pairs.push_to_gsheets('All Pairs')
