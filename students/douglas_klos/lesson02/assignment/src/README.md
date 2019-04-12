My approach to the assignment:

I used pdb and logging to find the location of the problems
in the JSON data and added functions / refactored the 
charges_calc.py to handle the bad data.

The first problem was that the JSON file had an extra comma
in a line that would prevent it from loading.  This was discovered
by using pdb and reading the exceptions.  Aside from a regular
expression I didn't see an easy way to dynamically repair a bad 
json data file, so I opted to have the program output exception
information that should lead the use to the issue with the file
and allow them to easily correct it, in this case, removing 
the extra comma.  This is logged as a critical error as it prevents
the program from continuing execution.

The other issues were all able to be handled during execution.
There were many records that had the start and end dates reversed.
These were simple enough to correct and issue logger warnings.
There were a couple of entries with 0 units rented or missing end
dates, these were parsed out and written to a separate json file
with 'bad' in the name.  All the good records are written to the
specified output.

My intent behind this is to isolate the bad records into a small file
and allow for manual correction of these records.  When working
on a clients database I'd want to make it as simple as possible for them
to have all their working records, and a way to correct the bad records.
I could have easily coded the program to just make up data for the
bad / missing entries, but we don't know that it would be the
correct data that the client intended, hence my approach.






Grading
=======

The assignment is grade by looking for:

- Error message for typo in input JSON file.
- Error message for quantity = 0 in any of the rentals.
- Warning for rentals missing end_date.
- And others...
2. Run linting using the regular batch file.
