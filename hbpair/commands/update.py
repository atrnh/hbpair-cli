from .base import Base
from .pairs import AllPairs
from json import dumps

class Update(Base):

    def run(self):
        options = self.options
        all_pairs = AllPairs.from_csv(options['<source-csv>'])
        all_pairs.update_with_csv(options['<updater-csv>'])
        all_pairs.write_to_csv('all-pairs.csv')
