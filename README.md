# hbpair
You're probably here because you need an All Pairs sheet in order to use the
Pairing Tools plugin for Google Sheets.

This is a CLI that generates an `all-pairs.csv` that can be imported to Google
Sheets. It will look something like this:

Name | Week 1 | Week 2
---- | ------ | ------
Phoenix Wright | Maya Fey | Miles Edgeworth
Maya Fey | Phoenix Wright | Apollo Justice

Where *Name* is a student's name and *Week 1* is their pair for week 1.

## Usage
```
hbpair update (<source-csv> <updater-csv>)
```

Example:
```
hbpair update all-pairs.csv pairs-wk4.csv
```

### Working with Google Sheets
1. The easiest way to get going right now is to clone this repo and create
   a Python virtual environment

   ```
   virtualenv env
   ```
2. Navigate to your `hbpair-cli` directory and run `pip install` on the
   directory.

   ```
   pip install .
   ```
3. Export your **All Pairs** sheet as a `.csv`, which should list all students'
   names:

   Name |
   ---- |
   Apollo Justice |
   ... |
4. Export your pairing sheet for that week as a `.csv`. It should contain
   students' names in the first column and have their pair ID in the **last
   column**. This sheet typically doesn't contain a header:

   ... | ... | ...   
   --- | --- | ---
   Phoenix Wright | tardy | 1
   Maya Fey |   | 1
5. Your updated pairs sheet will be created or updated at `all-pairs.csv` and
   can be imported into Google Sheets. When prompted, choose to overwrite
   the current sheet (or create a new one).

## To-do
- [x] Fetch current spreadsheet from Google
- [x] Push changes to Google Sheets
