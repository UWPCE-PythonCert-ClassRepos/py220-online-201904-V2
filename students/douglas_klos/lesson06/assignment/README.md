# Lesson 06 - Profiling and performance

These tests are being run on the following hardware:

Core i7-6700k @ 4.3GHz, 32GB DDR4, Linux Mint 19 (4.15), fairly old SSD drive.

Jumping right in, we run from the command line:
```
$ cp ./src/poor_pref.py ./src/poor_pref_v0.py
$ mv ./src/poor_pref.py ./src/poor_pref_v1.py
$ python -m cProfile --sort time ./src/poor_pref_v0.py
```
Giving us the result of:
```
{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         1056798 function calls (1056781 primitive calls) in 2.422 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    2.320    2.320    2.382    2.382 poor_pref_v0.py:11(analyze)
        1    0.038    0.038    2.420    2.420 poor_pref_v0.py:62(main)
  1000012    0.035    0.000    0.035    0.000 {method 'append' of 'list' objects}
    27750    0.017    0.000    0.017    0.000 {built-in method _codecs.utf_8_decode}
    27750    0.010    0.000    0.027    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
       10    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)

.........................abbreviated for length.................................

```
First, execution time of around 2.3 seconds for a million records is better
than I expected, I might need to up it to 10 million to get better results.

What's this? We're calling list.append over a million times?  Hmm, the code is
executing
```
if lrow[5] > "00/00/2012":
    new_ones.append((lrow[5], lrow[0]))
```
So clearly that if statement isn't operating as intended, since the dates were
randomly generated to be between 1900 and 2019, it's nearly impossible that
they'd all be over 2012.

We'll change that to:
```
date1 = datetime.datetime.strptime(lrow[5], "%m/%d/%Y")
date2 = datetime.datetime.strptime("01/01/2012", "%m/%d/%Y")
if date1 > date2:
```
...and see what we get.

```
$ python -m cProfile --sort time ./src/poor_pref_v1.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         46125855 function calls (46125773 primitive calls) in 19.159 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
2000000    8.070    0.000   14.430    0.000 _strptime.py:318(_strptime)
     1    2.819    2.819   19.153   19.153 poor_pref_v1.py:11(analyze)
2000000    1.230    0.000   15.660    0.000 _strptime.py:574(_strptime_datetime)
2000002    0.879    0.000    1.238    0.000 locale.py:384(normalize)
2000000    0.756    0.000    0.756    0.000 {method 'match' of 're.Pattern' objects}
2000002    0.662    0.000    2.899    0.000 locale.py:571(getlocale)
2000000    0.622    0.000   16.283    0.000 {built-in method strptime}
2000002    0.534    0.000    0.534    0.000 {built-in method _locale.setlocale}
2000000    0.521    0.000    0.521    0.000 {method 'groupdict' of 're.Match' objects}
2000002    0.519    0.000    3.419    0.000 _strptime.py:26(_getlang)
6000034    0.505    0.000    0.505    0.000 {method 'get' of 'dict' objects}
2000002    0.466    0.000    1.704    0.000 locale.py:467(_parse_localename)
4000001    0.328    0.000    0.328    0.000 {method 'toordinal' of 'datetime.date' objects}
4000253/4000237    0.295    0.000    0.295    0.000 {built-in method builtins.len}
4000372    0.275    0.000    0.275    0.000 {built-in method builtins.isinstance}
2000000    0.158    0.000    0.158    0.000 {method 'keys' of 'dict' objects}
2000000    0.156    0.000    0.156    0.000 {method 'weekday' of 'datetime.date' objects}
2000049    0.154    0.000    0.154    0.000 {method 'lower' of 'str' objects}
2000000    0.150    0.000    0.150    0.000 {method 'end' of 're.Match' objects}
 27750    0.024    0.000    0.024    0.000 {built-in method _codecs.utf_8_decode}
 27750    0.019    0.000    0.044    0.000 codecs.py:319(decode)
 66863    0.008    0.000    0.008    0.000 {method 'append' of 'list' objects}
     1    0.003    0.003   19.157   19.157 poor_pref_v1.py:65(main)
     4    0.001    0.000    0.001    0.000 {built-in method marshal.loads}
    25    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
     2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
  13/3    0.000    0.000    0.000    0.000 sre_parse.py:475(_parse)
    16    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
     1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
  16/3    0.000    0.000    0.000    0.000 sre_compile.py:71(_compile)
    38    0.000    0.000    0.000    0.000 {method 'strftime' of 'datetime.date' objects}
    26    0.000    0.000    0.000    0.000 {built-in method posix.stat}
     9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)

.........................abbreviated for length.................................
```
Oh no, that's horrible.  Clearly adding datetime.datetime.strptime to make the
comparison legit did not improve execution time.  We're not calling append a
million times anymore, but we're wasting a lot of time now doing date
comparisons.  On to the next idea...
```
$ cp ./src/poor_pref_v0.py ./src/poor_pref_v2.py
```
We're going to take out the append altogether, right now it's just wasted
operations.
```
$ python -m cProfile --sort time ./src/poor_pref_v2.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         56798 function calls (56781 primitive calls) in 2.226 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    2.198    2.198    2.224    2.224 poor_pref_v2.py:11(analyze)
 27750    0.016    0.000    0.016    0.000 {built-in method _codecs.utf_8_decode}
 27750    0.009    0.000    0.026    0.000 codecs.py:319(decode)
     2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
    13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
     2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
     1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
     9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)

.........................abbreviated for length.................................
```
Well that got the time down a bit.  Now let's replace all those if's with
elif's and see what happens

```
$ cp ./src/poor_pref_v2.py ./src/poor_pref_v3.py
$ python -m cProfile --sort time ./src/poor_pref_v3.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         56798 function calls (56781 primitive calls) in 2.173 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    2.146    2.146    2.171    2.171 poor_pref_v3.py:11(analyze)
 27750    0.016    0.000    0.016    0.000 {built-in method _codecs.utf_8_decode}
 27750    0.009    0.000    0.025    0.000 codecs.py:319(decode)
     2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
    13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
     2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
     1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
     9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)

.........................abbreviated for length.................................
```

There's a double loop in the analyze function too, pretty sure we don't need
to go through the file twice, we can do it all in one pass.

```
$ python -m cProfile --sort time ./src/poor_pref_v4.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         29042 function calls (29025 primitive calls) in 1.253 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       1    1.239    1.239    1.251    1.251 poor_pref_v4.py:11(analyze)
   13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
   13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
       2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
      13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
       2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
       1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
       9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```
Now we're getting somewhere, that shaved a second off the time!

Let's try using a generator
```
$ python -m cProfile --sort time ./src/poor_pref_v5.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         1029043 function calls (1029026 primitive calls) in 2.148 seconds

Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000001    1.549    0.000    1.562    0.000 poor_pref_v5.py:11(generate_line)
        1    0.583    0.583    2.146    2.146 poor_pref_v5.py:18(analyze)
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.005    0.000    0.013    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```
That made things worse.

How about replacing the dictionary with int variables...
```
$ python -m cProfile --sort time ./src/poor_perf_v6.py
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29042 function calls (29025 primitive calls) in 1.248 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.234    1.234    1.246    1.246 poor_perf_v6.py:11(analyze)
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```

1.253 seconds vs 1.248 seconds.  That is faster, but it could also be just
variance in background system processes.  We'll run it several more times.

```
29042 function calls (29025 primitive calls) in 1.248 seconds
29042 function calls (29025 primitive calls) in 1.269 seconds
29042 function calls (29025 primitive calls) in 1.284 seconds
29042 function calls (29025 primitive calls) in 1.257 seconds
29042 function calls (29025 primitive calls) in 1.289 seconds
29042 function calls (29025 primitive calls) in 1.278 seconds

Average = 1.2708 seconds
```
With dictionaries again...
```
29042 function calls (29025 primitive calls) in 1.253 seconds
29042 function calls (29025 primitive calls) in 1.284 seconds
29042 function calls (29025 primitive calls) in 1.296 seconds
29042 function calls (29025 primitive calls) in 1.305 seconds
29042 function calls (29025 primitive calls) in 1.270 seconds
29042 function calls (29025 primitive calls) in 1.326 seconds

Average = 1.289 seconds
```

Difference = 0.0182 seconds faster with int variables over dictionary,

Further testing, using the provided pytest file, I adjusted the inputs to be
the dict version and the int version.  This would give me a quick comparisons
on which is faster.  I ran the test twenty times, below are the results:
```
int based = 16
dict based  = 4
```
So we're going with int variables over dictionary.

Given that we're processing a 100MB CSV file, I wonder how much of this
performance is related to drive read speed.  We're running these tests off
an SSD, what would happen if we ran from DDR?
```
$ sudo mkdir /mnt/ramdisk
$ sudo mount -t tmpfs -o size=1024m tmpfs /mnt/ramdisk/
$ cp -R ../assignment/ /mnt/ramdisk/
$ cd /mnt/ramdisk
$ python -m cProfile --sort time ./src/poor_perf_v6.py

2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29042 function calls (29025 primitive calls) in 1.270 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.257    1.257    1.269    1.269 poor_perf_v6.py:11(analyze)
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```
Not a significant difference, if any.  Maybe with a massive dataset.

OK, how about we cdef those ugly ints...
```
$ python -m cProfile --sort time ./src/poor_perf_v7.py

2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29139 function calls (29112 primitive calls) in 0.992 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.978    0.978    0.991    0.991 {src.poor_perf_v7.analyze}
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
       11    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)

.........................abbreviated for length.................................
```
Now let's static define filename as a str
```
$ python -m cProfile --sort time ./src/poor_perf_v8.py

2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29139 function calls (29112 primitive calls) in 0.975 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.961    0.961    0.973    0.973 {src.poor_perf_v8.analyze}
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
       11    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)

.........................abbreviated for length.................................
```
We're under a second now, but we're not really just using python anymore are we.
I mean, at what point do you just recode the entire thing in C?

What are these calls to codecs.utf_8_decode anyways?
