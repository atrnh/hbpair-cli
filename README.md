# hbpair
You're probably here because you need an All Pairs sheet in order to use the
Pairing Tools plugin for Google Sheets.

This CLI updates an "All Pairs" sheet in Google Sheets. It looks something like
this:

Name | Week 1 | Week 2
---- | ------ | ------
Phoenix Wright | Maya Fey | Miles Edgeworth
Maya Fey | Phoenix Wright | Apollo Justice

Where *Name* is a student's name and *Week 1* is their pair for week 1.

## Usage
```
hbpair push [-a | <sheet-name>]
```

Options:
```
-a --all  Update All Pairs using all pairing sheets.
```

Example:
```
hbpair push Week\ 1
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
3. Make sure your **All Pairs** sheet has a column with all your students'
   names:

   Name |
   ---- |
   Apollo Justice |
   ... |
4. When you assign pairs for the week, make sure you have students' names in
   the first column and their pair IDs in the **last column**. This sheet
   typically doesn't contain a header:

   ... | ... | ...   
   --- | --- | ---
   Phoenix Wright | tardy | 1
   Maya Fey |   | 1
5. Run `hbpair push` with the name of your new pairing sheet.

## To-do
- [ ] Fetch current All Pairs spreadsheet from Google
- [x] Push changes to Google Sheets
