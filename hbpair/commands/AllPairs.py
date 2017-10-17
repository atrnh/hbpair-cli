"""Proposed workflow:
- Download new week as csv
- Use that to update all-pairs.csv
- Import csv to Google Sheets
"""


import csv
from collections import defaultdict
import sheets

class AllPairs:
    """Store student names and their pairs for each week."""

    def __init__(self, data=defaultdict(list)):
        self.data = data

    def __repr__(self):
        return str(self.data)

    @classmethod
    def from_csv(cls, filename):
        """Make AllPairs from csv of all student's pairs by name and week.

        First column of csv is student's name and next columns are their
        pairs' names by week.
        """

        data = defaultdict(list)

        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip the header

            for row in reader:
                data[row[0]].extend(row[1:])

        return cls(data)

    @classmethod
    def from_gsheets(cls, sheet_name):
        """Make AllPairs from rectangular list."""

        data = defaultdict(list)
        sheet = sheets.get_sheet(sheet_name)

        [data[row[0]].extend(row[1:]) for row in sheet]

        return cls(data)


    def update_with_csv(self, filename, stu_name_pos=0, pair_id_pos=-1):
        """Update pairs data using a dictionary of pairs by pair ID."""

        pairs_by_id = _get_pairs_from_csv(filename, stu_name_pos, pair_id_pos)

        for pair_id in pairs_by_id:
            curr_pair = pairs_by_id[pair_id]

            if len(curr_pair) == 2:
                self.data[curr_pair[0]].append(curr_pair[1])
                self.data[curr_pair[1]].append(curr_pair[0])
            else:
                self.data[curr_pair[0]].append('')

    def write_to_csv(self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)

            first_time = True

            for student in self.data:
                if first_time:
                    _write_header(writer, len(self.data[student]))
                    first_time = False

                writer.writerow([student] + self.data[student])


def _write_header(csv_writer, weeks_count):
    csv_writer.writerow(
        ['Name'] +
        ['Week {}'.format(week)
         for week in xrange(1, weeks_count + 1)
         ]
    )


def _get_rows_from_csv(filename):
    """Return rectangular list of csv rows."""
    with open(filename, 'rb') as csvfile:
        return list(csv.reader(csvfile))


def _get_pairs_from_csv(filename, stu_name_pos, pair_id_pos):
    """Return dictionary of pairs, by pair ID.

    Return dictionary with keys of pair ID and values of the pairs' names.

    Optionally designate column positions of the students' names and their
    pair IDs. Values default to names being in first column (0)
    and pair IDs in the last column (-1).
    """

    pairs_rows = _get_rows_from_csv(filename)
    pairs_by_id = defaultdict(list)

    for pair_data in pairs_rows:
        stu_name = pair_data[stu_name_pos]
        pair_id = pair_data[pair_id_pos]

        pairs_by_id[pair_id].append(stu_name)

    return pairs_by_id