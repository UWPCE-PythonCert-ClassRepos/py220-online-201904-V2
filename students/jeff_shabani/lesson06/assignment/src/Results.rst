Achieved a 46% increase on performance from poor_perf to good_perf.

Typical run-time for poor_perf was 5.53 seconds. Typical good_perf runtime
is 2.99 seconds.

Improvements were achieved by the following:

-Used Pandas library to harness its abilities to read and peform complex calculations an large datasets.
-Read in only fields necessary to produce results (date, sentence).
-Filed is initally filtered for records that only have the years 2013 - 2018.
-Shrank dataset size after each check year counts.

Script to create million record dataset is named make_mega_file.py, which creates a csv names 'mega.csv'