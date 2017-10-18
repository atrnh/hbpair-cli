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

        [data[row[0]].extend(row[1:])
         for i, row in enumerate(sheet)
         if i != 0  # skip the first row
         ]

        return cls(data)


    def update_with_csv(self, filename, stu_name_pos=0, pair_id_pos=-1):
        """Update pairs data with a csv."""

        pairs_by_id = _get_pairs_from_csv(filename, stu_name_pos, pair_id_pos)
        return self.update_with_dict(pairs_by_id)

    def update_with_gsheets(self, sheet_name, stu_name_pos=0, pair_id_pos=-1):
        """Update pairs data with Google Sheets."""
    
        pairs_by_id = _get_pairs_from_list(
                                           sheets.get_sheet(sheet_name),
                                           stu_name_pos,
                                           pair_id_pos
                                           )
        return self.update_with_dict(pairs_by_id)

    def update_with_all_gsheets(self, stu_name_pos=0, pair_id_pos=-1):
        """Update pairs data with all sheets in Google Sheets."""
        
        all_sheets = sheets.get_sheets_names()

        [self.update_with_dict(_get_pairs_from_list(
                                                    sheets.get_sheet(sheet_name),
                                                    stu_name_pos,
                                                    pair_id_pos
                                                    ))
         for sheet_name in all_sheets
         if sheet_name != 'All Pairs'
         ]

        return self

    def update_with_dict(self, pairs_by_id):
        """Update pairs data with a dictionary of pairs by pair ID."""
        
        for pair_id in pairs_by_id:
            curr_pair = pairs_by_id[pair_id]

            if len(curr_pair) == 2:
                self.data[curr_pair[0]].append(curr_pair[1])
                self.data[curr_pair[1]].append(curr_pair[0])
            else:
                self.data[curr_pair[0]].append('')

        return self

    def get_data_rows(self, with_header=True):
        rows = []
        first_time = True

        for student in self.data:
            if first_time and with_header:
                rows.append(_header(len(self.data[student])))
                first_time = False

            rows.append([student] + self.data[student])

        return rows

    def write_to_csv(self, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            [writer.writerow(row) for row in self.get_data_rows()]

    def push_to_gsheets(self, sheet_name):
        sheets.push_sheet(sheet_name, self.get_data_rows())


def _header(weeks_count):
    return ( 
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
    
    return _get_pairs_from_list(pairs_rows, stu_name_pos, pair_id_pos) 


def _get_pairs_from_list(pairs_rows, stu_name_pos, pair_id_pos):
    pairs_by_id = defaultdict(list)

    for pair_data in pairs_rows:
        stu_name = pair_data[stu_name_pos]
        pair_id = pair_data[pair_id_pos]

        pairs_by_id[pair_id].append(stu_name)

    return pairs_by_id
    
