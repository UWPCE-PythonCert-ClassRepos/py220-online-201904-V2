# Lesson 06 - Profiling and performance

These tests are being run on the following hardware:

Core i7-6700k @ 4.3GHz, 32GB DDR4, Linux Mint 19 (4.15), fairly old SSD drive.

### General commands used

First, there is no good\_perf.py file.  The current good_perf is poor_perf_v15.pyx
which is a cython build, or v14 for Python. (Not including the C builds)

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson06/assignment/submission/
$
$ python ./src/good_perf_setup.py build_ext --inplace
$ python -m cProfile --sort time ./src/poor_perf_v14.py
$ python -m cProfile --sort time ./src/poor_perf_v15.py
$
$ pylint ./src/
$ pytest ./tests/
$ 
```

## Conclusion

I'm surprised by the amount I was able to improve the performance.
The first program given to us was pretty bad, had extra loops
and assignments that didn't work, plus lots of extra if's.  It 
clocked in at 2.422.  Following is a list of notable times:

```
poor_pref_v00.py     =  2.422 # Original time
poor_pref_v01.py     = 19.159 # Parsing the dates correctly for comparison
poor_pref_v02.py     =  2.226 # Removed broken unnecessary append
poor_pref_v03.py     =  2.173 # Replaced if's with else if's
poor_pref_v04.py     =  1.253 # Removed the extra loop
poor_pref_v05.py     =  2.148 # Using a generator for file content
poor_pref_v06.py     =  1.248 # Replaced dictionary with int's
poor_pref_v07.pyx    =  0.992 # Cython int's
poor_pref_v08.pyx    =  0.975 # Cython int's and str filename
poor_pref_v09.java   =  1.831 # Sloppy Java
poor_pref_v09.class  =  0.995 # Sloppy Java compiled
poor_pref_v10.java   =  1.838 # Sloppy Java with switch
poor_pref_v10.class  =  0.938 # Sloppy Java compiled with switch
poor_pref_v11.py     =  4.643 # Pandas
poor_pref_v12.py     =  4.797 # Pandas with less assignment
poor_pref_v13.py     =  0.751 # Changed CSV reader for line in file split(',')
poor_pref_v14.py     =  0.469 # Added if to filter other if's
poor_pref_v15.pyx    =  0.354 # Cythonized int's and str from #14
poor_pref_v16.c      =  0.193 # Sloppy C
poor_perf_v17.c      =  0.171 # Slightly better C?
```
I have linted the ones for submission - the ones during the trial phases are not linted.

## Staring Out

Jumping right in, we run from the command line:
```
$ cp ./src/poor_pref.py ./src/poor_pref_v00.py
$ mv ./src/poor_pref.py ./src/poor_pref_v01.py
$ python -m cProfile --sort time ./src/poor_pref_v00.py
```
Giving us the result of:
```
{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         1056798 function calls (1056781 primitive calls) in 2.422 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    2.320    2.320    2.382    2.382 poor_pref_v00.py:11(analyze)
        1    0.038    0.038    2.420    2.420 poor_pref_v00.py:62(main)
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
$ python -m cProfile --sort time ./src/poor_pref_v01.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         46125855 function calls (46125773 primitive calls) in 19.159 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
2000000    8.070    0.000   14.430    0.000 _strptime.py:318(_strptime)
     1    2.819    2.819   19.153   19.153 poor_pref_v01.py:11(analyze)
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
     1    0.003    0.003   19.157   19.157 poor_pref_v01.py:65(main)
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
$ cp ./src/poor_pref_v00.py ./src/poor_pref_v02.py
```
We're going to take out the append altogether, right now it's just wasted
operations.
```
$ python -m cProfile --sort time ./src/poor_pref_v02.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         56798 function calls (56781 primitive calls) in 2.226 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    2.198    2.198    2.224    2.224 poor_pref_v02.py:11(analyze)
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
$ cp ./src/poor_pref_v02.py ./src/poor_pref_v03.py
$ python -m cProfile --sort time ./src/poor_pref_v03.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         56798 function calls (56781 primitive calls) in 2.173 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    2.146    2.146    2.171    2.171 poor_pref_v03.py:11(analyze)
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
$ python -m cProfile --sort time ./src/poor_pref_v04.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         29042 function calls (29025 primitive calls) in 1.253 seconds

Ordered by: internal time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       1    1.239    1.239    1.251    1.251 poor_pref_v04.py:11(analyze)
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
$ python -m cProfile --sort time ./src/poor_pref_v05.py

{'2013': 8362, '2014': 8332, '2015': 8055, '2016': 8532, '2017': 8363, '2018': 8305}
'ao' was found 35966 times
         1029043 function calls (1029026 primitive calls) in 2.148 seconds

Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000001    1.549    0.000    1.562    0.000 poor_pref_v05.py:11(generate_line)
        1    0.583    0.583    2.146    2.146 poor_pref_v05.py:18(analyze)
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
$ python -m cProfile --sort time ./src/poor_perf_v06.py
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29042 function calls (29025 primitive calls) in 1.248 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.234    1.234    1.246    1.246 poor_perf_v06.py:11(analyze)
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
$ python -m cProfile --sort time ./src/poor_perf_v06.py

2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29042 function calls (29025 primitive calls) in 1.270 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.257    1.257    1.269    1.269 poor_perf_v06.py:11(analyze)
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

## Cython

OK, how about we cdef those ugly ints...
```
$ python -m cProfile --sort time ./src/poor_perf_v07.py

2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29139 function calls (29112 primitive calls) in 0.992 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.978    0.978    0.991    0.991 {src.poor_perf_v07.analyze}
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
$ python -m cProfile --sort time ./src/poor_perf_v08.py

2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

'ao' was found 35966 times
         29139 function calls (29112 primitive calls) in 0.975 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.961    0.961    0.973    0.973 {src.poor_perf_v08.analyze}
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

## Rabbit Hole

I haven't coded much java in months, so I just did this off the cuff with a bit
of google-fu mixed in.  But I wanted a comparison against another language.
We're not profiling here like we did on Python, but we can still time it.  I
tried to structure the Java in the same way as the Python code, for better
or for worse.

```
$ time java ./poor_perf_v09.java

2013:8362    2014:8332    2015:8055    2016:8532    2017:8363    2018:8305

'ao' was found 35966 times

real	0m0.939s
user	0m1.831s
sys	0m0.161s
```
Not great, although I haven't spent time in Java for a while.  What about
if we compile it first?
```
$ javac ./poor_perf_v09.java
$ java JavaPerf

2013:8362    2014:8332    2015:8055    2016:8532    2017:8363    2018:8305

'ao' was found 35966 times

real	0m0.621s
user	0m0.995s
sys	0m0.088s
```

For 10 we replace the if statements with a swtich.

```
$ time java ./poor_perf_v10.java

2013:8362    2014:8332    2015:8055    2016:8532    2017:8363    2018:8305

'ao' was found 35966 times

real	0m0.918s
user	0m1.838s
sys	0m0.148s
```
and compiled
```
$ javac ./poor_pref_v10.java
$ time java JavaPerf

2013:8362    2014:8332    2015:8055    2016:8532    2017:8363    2018:8305

'ao' was found 35966 times

real	0m0.605s
user	0m0.938s
sys	0m0.098s
```

Not a big difference there, and we should get back to Python anyways...

## Python again

For 11 we're going to try Pandas

```
$ python -m cProfile --sort time ./src/poor_perf_v11.py

'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

         14249454 function calls (14242882 primitive calls) in 4.643 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.383    1.383    1.385    1.385 {method 'read' of 'pandas._libs.parsers.TextReader' objects}
  7000000    0.966    0.000    1.712    0.000 strings.py:306(<lambda>)
  7000019    0.747    0.000    0.747    0.000 {method 'search' of 're.Pattern' objects}
        7    0.726    0.104    2.439    0.348 {pandas._libs.lib.map_infer_mask}
        8    0.348    0.043    0.348    0.044 {built-in method builtins.sum}
        8    0.163    0.020    0.163    0.020 {built-in method pandas._libs.missing.isnaobj}
      364    0.030    0.000    0.030    0.000 {built-in method marshal.loads}
        4    0.029    0.007    0.029    0.007 {pandas._libs.lib.infer_dtype}
        2    0.026    0.013    0.031    0.015 managers.py:1841(_stack_arrays)
    56/41    0.016    0.000    0.028    0.001 {built-in method _imp.create_dynamic}
        1    0.015    0.015    1.466    1.466 parsers.py:403(_read)
     1837    0.011    0.000    0.017    0.000 <frozen importlib._bootstrap_external>:74(_path_stat)
  968/960    0.011    0.000    0.035    0.000 {built-in method builtins.__build_class__}
      921    0.010    0.000    0.010    0.000 {method 'sub' of 're.Pattern' objects}
      613    0.009    0.000    0.009    0.000 {method 'findall' of 're.Pattern' objects}
     2429    0.007    0.000    0.007    0.000 {built-in method posix.stat}
       62    0.005    0.000    0.005    0.000 accessor.py:88(_create_delegator_method)
      832    0.005    0.000    0.018    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
       16    0.004    0.000    0.004    0.000 {built-in method numpy.empty}
      364    0.003    0.000    0.003    0.000 {method 'read' of '_io.FileIO' objects}
      364    0.003    0.000    0.006    0.000 <frozen importlib._bootstrap_external>:914(get_data)
      610    0.003    0.000    0.027    0.000 <frozen importlib._bootstrap>:882(_find_spec)
   227/84    0.003    0.000    0.007    0.000 sre_parse.py:475(_parse)
.........................abbreviated for length.................................
```
Holy smokes, my Pandas are molasses.  To be fair this is the first time I've
coded in Pandas so perhaps it's not optimized?  Probably just a lot of overhead
going on.

Maybe just stuff everything into the return and forget about printing?
```
$ python -m cProfile --sort time ./src/poor_perf_v12.py
         14249452 function calls (14242880 primitive calls) in 4.797 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.458    1.458    1.460    1.460 {method 'read' of 'pandas._libs.parsers.TextReader' objects}
  7000000    0.933    0.000    1.697    0.000 strings.py:306(<lambda>)
        7    0.794    0.113    2.491    0.356 {pandas._libs.lib.map_infer_mask}
  7000019    0.764    0.000    0.764    0.000 {method 'search' of 're.Pattern' objects}
        8    0.363    0.045    0.363    0.045 {built-in method builtins.sum}
        8    0.171    0.021    0.171    0.021 {built-in method pandas._libs.missing.isnaobj}
      364    0.032    0.000    0.032    0.000 {built-in method marshal.loads}
        4    0.031    0.008    0.031    0.008 {pandas._libs.lib.infer_dtype}
        2    0.028    0.014    0.033    0.017 managers.py:1841(_stack_arrays)
        1    0.017    0.017    1.546    1.546 parsers.py:403(_read)
    56/41    0.017    0.000    0.029    0.001 {built-in method _imp.create_dynamic}
  968/960    0.011    0.000    0.036    0.000 {built-in method builtins.__build_class__}
      921    0.010    0.000    0.010    0.000 {method 'sub' of 're.Pattern' objects}
      613    0.009    0.000    0.009    0.000 {method 'findall' of 're.Pattern' objects}
     2429    0.007    0.000    0.007    0.000 {built-in method posix.stat}
       16    0.005    0.000    0.005    0.000 {built-in method numpy.empty}
       62    0.005    0.000    0.005    0.000 accessor.py:88(_create_delegator_method)
      832    0.005    0.000    0.018    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
      364    0.003    0.000    0.003    0.000 {method 'read' of '_io.FileIO' objects}
      364    0.003    0.000    0.006    0.000 <frozen importlib._bootstrap_external>:914(get_data)
      610    0.003    0.000    0.027    0.000 <frozen importlib._bootstrap>:882(_find_spec)
   227/84    0.003    0.000    0.007    0.000 sre_parse.py:475(_parse)
.........................abbreviated for length.................................
```
That didn't make a difference, didn't really expect it to either to be honest.
Still ends up being millions of function calls from pandas overhead.  Also,
perhaps there's a better way to do it in Pandas.  However just opening the
dataframe took 1.5 seconds, which is .3 too long.

OK, v06 was the last pure Python version, so we're going to proceed from there.
After we get that optimized more, we can reintroduce cython, but it's a bit of
a PITA to be compiling every time.

Following is an analysis based on which lines of code instead of specific
functions.  This comes from a Pypi package called pprofile.

```
$ pprofile --exclude-syspath ./src/poor_perf_v13.py > output.txt
'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

Command line: ./src/poor_perf_v13.py
Total duration: 19.944s
File: ./src/poor_perf_v13.py
File duration: 19.7768s (99.16%)
Line #|      Hits|         Time| Time per hit|      %|Source code
------+----------+-------------+-------------+-------+-----------
     1|         0|            0|            0|  0.00%|#!/usr/bin/env python3
     2|         0|            0|            0|  0.00%|
     3|         2|  2.69413e-05|  1.34706e-05|  0.00%|import datetime
     4|         1|  1.83582e-05|  1.83582e-05|  0.00%|import csv
(call)|         1|   0.00912309|   0.00912309|  0.05%|# <frozen importlib._bootstrap>:978 _find_and_load
     5|         0|            0|            0|  0.00%|
     6|         0|            0|            0|  0.00%|
     7|         2|  1.16825e-05|  5.84126e-06|  0.00%|def analyze(filename):
     8|         1|  5.48363e-06|  5.48363e-06|  0.00%|    found = 0
     9|         0|            0|            0|  0.00%|
    10|         1|  5.96046e-06|  5.96046e-06|  0.00%|    _2013 = 0
    11|         1|  5.48363e-06|  5.48363e-06|  0.00%|    _2014 = 0
    12|         1|  5.72205e-06|  5.72205e-06|  0.00%|    _2015 = 0
    13|         1|  5.48363e-06|  5.48363e-06|  0.00%|    _2016 = 0
    14|         1|  6.19888e-06|  6.19888e-06|  0.00%|    _2017 = 0
    15|         1|  5.72205e-06|  5.72205e-06|  0.00%|    _2018 = 0
    16|         0|            0|            0|  0.00%|
    17|         1|  1.54972e-05|  1.54972e-05|  0.00%|    start = datetime.datetime.now()
    18|         0|            0|            0|  0.00%|
    19|         1|   6.4373e-05|   6.4373e-05|  0.00%|    with open(filename) as csvfile:
(call)|         1|  5.24521e-05|  5.24521e-05|  0.00%|# /usr/lib/python3.7/_bootlocale.py:33 getpreferredencoding
(call)|         1|  4.17233e-05|  4.17233e-05|  0.00%|# /usr/lib/python3.7/codecs.py:309 __init__
    20|         1|  1.21593e-05|  1.21593e-05|  0.00%|        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    21|         0|            0|            0|  0.00%|
    22|   1000001|      2.93384|  2.93383e-06| 14.71%|        for row in reader:
(call)|     13875|     0.157998|  1.13873e-05|  0.79%|# /usr/lib/python3.7/codecs.py:319 decode
    23|   1000000|      2.20949|  2.20949e-06| 11.08%|            lrow = list(row)
    24|         0|            0|            0|  0.00%|
    25|   1000000|      2.08952|  2.08952e-06| 10.48%|            if "ao" in lrow[6]:
    26|     35966|    0.0737531|  2.05063e-06|  0.37%|                found += 1
    27|         0|            0|            0|  0.00%|
    28|   1000000|      2.11182|  2.11182e-06| 10.59%|            if lrow[5][6:] == "2013":
    29|      8362|    0.0172274|   2.0602e-06|  0.09%|                _2013 += 1
    30|    991638|      2.09301|  2.11065e-06| 10.49%|            elif lrow[5][6:] == "2014":
    31|      8332|    0.0171816|  2.06213e-06|  0.09%|                _2014 += 1
    32|    983306|      2.07171|  2.10688e-06| 10.39%|            elif lrow[5][6:] == "2015":
    33|      8055|    0.0166647|  2.06887e-06|  0.08%|                _2015 += 1
    34|    975251|      2.05191|  2.10398e-06| 10.29%|            elif lrow[5][6:] == "2016":
    35|      8532|    0.0176413|  2.06766e-06|  0.09%|                _2016 += 1
    36|    966719|      2.03698|   2.1071e-06| 10.21%|            elif lrow[5][6:] == "2017":
    37|      8363|    0.0171769|  2.05391e-06|  0.09%|                _2017 += 1
    38|    958356|      2.00124|   2.0882e-06| 10.03%|            elif lrow[5][6:] == "2018":
    39|      8305|    0.0173182|  2.08528e-06|  0.09%|                _2018 += 1
    40|         0|            0|            0|  0.00%|
    41|         1|  1.07288e-05|  1.07288e-05|  0.00%|    print(f"'ao' was found {found} times")
    42|         1|  6.19888e-06|  6.19888e-06|  0.00%|    print(
    43|         1|   3.8147e-06|   3.8147e-06|  0.00%|        f"2013:{_2013}\t"
    44|         0|            0|            0|  0.00%|        f"2014:{_2014}\t"
    45|         0|            0|            0|  0.00%|        f"2015:{_2015}\t"
    46|         0|            0|            0|  0.00%|        f"2016:{_2016}\t"
    47|         0|            0|            0|  0.00%|        f"2017:{_2017}\t"
    48|         0|            0|            0|  0.00%|        f"2018:{_2018}\n"
    49|         0|            0|            0|  0.00%|    )
    50|         1|  7.86781e-06|  7.86781e-06|  0.00%|    end = datetime.datetime.now()
    51|         0|            0|            0|  0.00%|    return (
    52|         1|  3.33786e-06|  3.33786e-06|  0.00%|        start,
    53|         1|   2.6226e-06|   2.6226e-06|  0.00%|        end,
    54|         0|            0|            0|  0.00%|        {
    55|         1|  2.38419e-06|  2.38419e-06|  0.00%|            "2013": _2013,
    56|         1|   2.6226e-06|   2.6226e-06|  0.00%|            "2014": _2014,
    57|         1|  2.86102e-06|  2.86102e-06|  0.00%|            "2015": _2015,
    58|         1|   2.6226e-06|   2.6226e-06|  0.00%|            "2016": _2016,
    59|         1|  4.76837e-06|  4.76837e-06|  0.00%|            "2017": _2017,
    60|         1|   3.8147e-06|   3.8147e-06|  0.00%|            "2018": _2018,
    61|         0|            0|            0|  0.00%|        },
    62|         1|  3.09944e-06|  3.09944e-06|  0.00%|        found,
    63|         0|            0|            0|  0.00%|    )
    64|         0|            0|            0|  0.00%|
    65|         0|            0|            0|  0.00%|
    66|         2|  1.00136e-05|  5.00679e-06|  0.00%|def main():
    67|         1|  4.05312e-06|  4.05312e-06|  0.00%|    filename = "data/dataset.csv"
    68|         1|  2.19345e-05|  2.19345e-05|  0.00%|    analyze(filename)
(call)|         1|      19.9348|      19.9348| 99.95%|# ./src/poor_perf_v13.py:7 analyze
    69|         0|            0|            0|  0.00%|
    70|         0|            0|            0|  0.00%|
    71|         1|  5.00679e-06|  5.00679e-06|  0.00%|if __name__ == "__main__":
    72|         1|  1.21593e-05|  1.21593e-05|  0.00%|    main()
(call)|         1|      19.9348|      19.9348| 99.95%|# ./src/poor_perf_v13.py:66 main
```

Couple lines jump out at me there...
```
for row in reader:
    lrow = list(row)
```
Cumulative 25% of our times is spent on these lines.  Perhaps we try parsing the
file in a different method...
```
'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

Command line: ./src/poor_perf_v13.py
Total duration: 20.9319s
File: ./src/poor_perf_v13.py
File duration: 20.7552s (99.16%)
Line #|      Hits|         Time| Time per hit|      %|Source code
------+----------+-------------+-------------+-------+-----------
     1|         0|            0|            0|  0.00%|#!/usr/bin/env python3
     2|         0|            0|            0|  0.00%|
     3|         2|  1.88351e-05|  9.41753e-06|  0.00%|import datetime
     4|         0|            0|            0|  0.00%|
     5|         0|            0|            0|  0.00%|
     6|         2|  6.67572e-06|  3.33786e-06|  0.00%|def analyze(filename):
     7|         1|  3.09944e-06|  3.09944e-06|  0.00%|    found = 0
     8|         0|            0|            0|  0.00%|
     9|         1|  3.33786e-06|  3.33786e-06|  0.00%|    _2013 = 0
    10|         1|  2.86102e-06|  2.86102e-06|  0.00%|    _2014 = 0
    11|         1|  3.09944e-06|  3.09944e-06|  0.00%|    _2015 = 0
    12|         1|  3.09944e-06|  3.09944e-06|  0.00%|    _2016 = 0
    13|         1|   2.6226e-06|   2.6226e-06|  0.00%|    _2017 = 0
    14|         1|  3.09944e-06|  3.09944e-06|  0.00%|    _2018 = 0
    15|         0|            0|            0|  0.00%|
    16|         1|  8.58307e-06|  8.58307e-06|  0.00%|    start = datetime.datetime.now()
    17|         0|            0|            0|  0.00%|
    18|         1|  3.31402e-05|  3.31402e-05|  0.00%|    with open(filename) as csvfile:
(call)|         1|  2.21729e-05|  2.21729e-05|  0.00%|# /usr/lib/python3.7/_bootlocale.py:33 getpreferredencoding
(call)|         1|  2.24113e-05|  2.24113e-05|  0.00%|# /usr/lib/python3.7/codecs.py:309 __init__
    19|   1000001|      2.38885|  2.38885e-06| 11.41%|        for line in csvfile:
(call)|     13875|     0.176653|  1.27317e-05|  0.84%|# /usr/lib/python3.7/codecs.py:319 decode
    20|   1000000|      2.51121|  2.51121e-06| 12.00%|            lrow = line.split(',')
    21|         0|            0|            0|  0.00%|
    22|   1000000|      2.29874|  2.29874e-06| 10.98%|            if "ao" in lrow[6]:
    23|     35966|    0.0805304|  2.23907e-06|  0.38%|                found += 1
    24|         0|            0|            0|  0.00%|
    25|   1000000|      2.26555|  2.26555e-06| 10.82%|            if lrow[5][6:] == "2013":
    26|      8362|    0.0186727|  2.23304e-06|  0.09%|                _2013 += 1
    27|    991638|      2.26206|  2.28113e-06| 10.81%|            elif lrow[5][6:] == "2014":
    28|      8332|    0.0186644|  2.24008e-06|  0.09%|                _2014 += 1
    29|    983306|      2.23747|  2.27546e-06| 10.69%|            elif lrow[5][6:] == "2015":
    30|      8055|    0.0181003|  2.24708e-06|  0.09%|                _2015 += 1
    31|    975251|      2.21934|  2.27566e-06| 10.60%|            elif lrow[5][6:] == "2016":
    32|      8532|    0.0191708|  2.24692e-06|  0.09%|                _2016 += 1
    33|    966719|      2.20518|  2.28109e-06| 10.53%|            elif lrow[5][6:] == "2017":
    34|      8363|    0.0180504|  2.15837e-06|  0.09%|                _2017 += 1
    35|    958356|      2.17547|     2.27e-06| 10.39%|            elif lrow[5][6:] == "2018":
    36|      8305|    0.0179615|  2.16273e-06|  0.09%|                _2018 += 1
    37|         0|            0|            0|  0.00%|
    38|         1|  1.14441e-05|  1.14441e-05|  0.00%|    print(f"'ao' was found {found} times")
    39|         1|  5.96046e-06|  5.96046e-06|  0.00%|    print(
    40|         1|  4.29153e-06|  4.29153e-06|  0.00%|        f"2013:{_2013}\t"
    41|         0|            0|            0|  0.00%|        f"2014:{_2014}\t"
    42|         0|            0|            0|  0.00%|        f"2015:{_2015}\t"
    43|         0|            0|            0|  0.00%|        f"2016:{_2016}\t"
    44|         0|            0|            0|  0.00%|        f"2017:{_2017}\t"
    45|         0|            0|            0|  0.00%|        f"2018:{_2018}\n"
    46|         0|            0|            0|  0.00%|    )
    47|         1|  7.62939e-06|  7.62939e-06|  0.00%|    end = datetime.datetime.now()
    48|         0|            0|            0|  0.00%|    return (
    49|         1|  2.86102e-06|  2.86102e-06|  0.00%|        start,
    50|         1|  2.86102e-06|  2.86102e-06|  0.00%|        end,
    51|         0|            0|            0|  0.00%|        {
    52|         1|  2.38419e-06|  2.38419e-06|  0.00%|            "2013": _2013,
    53|         1|  2.38419e-06|  2.38419e-06|  0.00%|            "2014": _2014,
    54|         1|  2.38419e-06|  2.38419e-06|  0.00%|            "2015": _2015,
    55|         1|  2.86102e-06|  2.86102e-06|  0.00%|            "2016": _2016,
    56|         1|   2.6226e-06|   2.6226e-06|  0.00%|            "2017": _2017,
    57|         1|   1.0252e-05|   1.0252e-05|  0.00%|            "2018": _2018,
    58|         0|            0|            0|  0.00%|        },
    59|         1|  2.86102e-06|  2.86102e-06|  0.00%|        found,
    60|         0|            0|            0|  0.00%|    )
    61|         0|            0|            0|  0.00%|
    62|         0|            0|            0|  0.00%|
    63|         2|  5.72205e-06|  2.86102e-06|  0.00%|def main():
    64|         1|  2.14577e-06|  2.14577e-06|  0.00%|    filename = "data/dataset.csv"
    65|         1|  1.50204e-05|  1.50204e-05|  0.00%|    analyze(filename)
(call)|         1|      20.9318|      20.9318|100.00%|# ./src/poor_perf_v13.py:6 analyze
    66|         0|            0|            0|  0.00%|
    67|         0|            0|            0|  0.00%|
    68|         1|   2.6226e-06|   2.6226e-06|  0.00%|if __name__ == "__main__":
    69|         1|  9.77516e-06|  9.77516e-06|  0.00%|    main()
(call)|         1|      20.9319|      20.9319|100.00%|# ./src/poor_perf_v13.py:63 main
```
So we're spending a bit less time on those specific lines of code.  However,
the total processing time for the file is reduced dramatically.

```
$ python -m cProfile --sort time ./src/poor_perf_v13.py

'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

         1028558 function calls (1028547 primitive calls) in 0.751 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.572    0.572    0.749    0.749 poor_perf_v13.py:6(analyze)
  1000000    0.165    0.000    0.165    0.000 {method 'split' of 'str' objects}
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        6    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```
We're down to .75 seconds before we cythonize!  This exceeded my expectations
by a margin.  We're outperforming my Java code, although it's poorly written
Java that could also stand for a lot of optimizing.  Now we're spending lots
of time on those if statements.  What if we add an if to check if year > 2012
before making it do the remaining if's, should cut down on the number of
operations.
```
$ python -m cProfile --sort time ./src/poor_perf_v14.py
'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

         1028558 function calls (1028547 primitive calls) in 0.469 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.298    0.298    0.469    0.469 poor_perf_v14.py:6(analyze)
  1000000    0.159    0.000    0.159    0.000 {method 'split' of 'str' objects}
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        6    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```
Under a half second.
```
'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

Command line: ./src/poor_perf_v14.py
Total duration: 9.34853s
File: ./src/poor_perf_v14.py
File duration: 9.19317s (98.34%)
Line #|      Hits|         Time| Time per hit|      %|Source code
------+----------+-------------+-------------+-------+-----------
     1|         0|            0|            0|  0.00%|#!/usr/bin/env python3
     2|         0|            0|            0|  0.00%|
     3|         2|  2.12193e-05|  1.06096e-05|  0.00%|import datetime
     4|         0|            0|            0|  0.00%|
     5|         0|            0|            0|  0.00%|
     6|         2|  6.19888e-06|  3.09944e-06|  0.00%|def analyze(filename):
     7|         1|  2.86102e-06|  2.86102e-06|  0.00%|    found = 0
     8|         0|            0|            0|  0.00%|
     9|         1|  3.33786e-06|  3.33786e-06|  0.00%|    _2013 = 0
    10|         1|  2.86102e-06|  2.86102e-06|  0.00%|    _2014 = 0
    11|         1|  2.86102e-06|  2.86102e-06|  0.00%|    _2015 = 0
    12|         1|  2.86102e-06|  2.86102e-06|  0.00%|    _2016 = 0
    13|         1|  2.86102e-06|  2.86102e-06|  0.00%|    _2017 = 0
    14|         1|  3.09944e-06|  3.09944e-06|  0.00%|    _2018 = 0
    15|         0|            0|            0|  0.00%|
    16|         1|  9.53674e-06|  9.53674e-06|  0.00%|    start = datetime.datetime.now()
    17|         0|            0|            0|  0.00%|
    18|         1|  3.50475e-05|  3.50475e-05|  0.00%|    with open(filename) as csvfile:
(call)|         1|  2.21729e-05|  2.21729e-05|  0.00%|# /usr/lib/python3.7/_bootlocale.py:33 getpreferredencoding
(call)|         1|  2.24113e-05|  2.24113e-05|  0.00%|# /usr/lib/python3.7/codecs.py:309 __init__
    19|   1000001|      2.14944|  2.14944e-06| 22.99%|        for line in csvfile:
(call)|     13875|     0.155281|  1.11914e-05|  1.66%|# /usr/lib/python3.7/codecs.py:319 decode
    20|   1000000|      2.25409|  2.25409e-06| 24.11%|            lrow = line.split(',')
    21|         0|            0|            0|  0.00%|
    22|   1000000|      2.06572|  2.06572e-06| 22.10%|            if "ao" in lrow[6]:
    23|     35966|    0.0723741|  2.01229e-06|  0.77%|                found += 1
    24|         0|            0|            0|  0.00%|
    25|   1000000|      2.07814|  2.07814e-06| 22.23%|            if "2012" < lrow[5][6:]:
    26|     58257|     0.123345|  2.11725e-06|  1.32%|                if lrow[5][6:] == "2013":
    27|      8362|    0.0170243|  2.03591e-06|  0.18%|                    _2013 += 1
    28|     49895|     0.105087|  2.10617e-06|  1.12%|                elif lrow[5][6:] == "2014":
    29|      8332|    0.0168929|  2.02747e-06|  0.18%|                    _2014 += 1
    30|     41563|    0.0868902|  2.09057e-06|  0.93%|                elif lrow[5][6:] == "2015":
    31|      8055|    0.0163043|  2.02412e-06|  0.17%|                    _2015 += 1
    32|     33508|     0.069766|  2.08207e-06|  0.75%|                elif lrow[5][6:] == "2016":
    33|      8532|    0.0172503|  2.02184e-06|  0.18%|                    _2016 += 1
    34|     24976|    0.0524621|   2.1005e-06|  0.56%|                elif lrow[5][6:] == "2017":
    35|      8363|    0.0168536|  2.01525e-06|  0.18%|                    _2017 += 1
    36|     16613|    0.0345905|  2.08213e-06|  0.37%|                elif lrow[5][6:] == "2018":
    37|      8305|    0.0167525|  2.01716e-06|  0.18%|                    _2018 += 1
    38|         0|            0|            0|  0.00%|
    39|         1|   1.0252e-05|   1.0252e-05|  0.00%|    print(f"'ao' was found {found} times")
    40|         1|  7.15256e-06|  7.15256e-06|  0.00%|    print(
    41|         1|  4.29153e-06|  4.29153e-06|  0.00%|        f"2013:{_2013}\t"
    42|         0|            0|            0|  0.00%|        f"2014:{_2014}\t"
    43|         0|            0|            0|  0.00%|        f"2015:{_2015}\t"
    44|         0|            0|            0|  0.00%|        f"2016:{_2016}\t"
    45|         0|            0|            0|  0.00%|        f"2017:{_2017}\t"
    46|         0|            0|            0|  0.00%|        f"2018:{_2018}\n"
    47|         0|            0|            0|  0.00%|    )
    48|         1|  6.91414e-06|  6.91414e-06|  0.00%|    end = datetime.datetime.now()
    49|         0|            0|            0|  0.00%|    return (
    50|         1|  3.09944e-06|  3.09944e-06|  0.00%|        start,
    51|         1|   2.6226e-06|   2.6226e-06|  0.00%|        end,
    52|         0|            0|            0|  0.00%|        {
    53|         1|   2.6226e-06|   2.6226e-06|  0.00%|            "2013": _2013,
    54|         1|   2.6226e-06|   2.6226e-06|  0.00%|            "2014": _2014,
    55|         1|  8.34465e-06|  8.34465e-06|  0.00%|            "2015": _2015,
    56|         1|   2.6226e-06|   2.6226e-06|  0.00%|            "2016": _2016,
    57|         1|  3.33786e-06|  3.33786e-06|  0.00%|            "2017": _2017,
    58|         1|  3.09944e-06|  3.09944e-06|  0.00%|            "2018": _2018,
    59|         0|            0|            0|  0.00%|        },
    60|         1|  3.57628e-06|  3.57628e-06|  0.00%|        found,
    61|         0|            0|            0|  0.00%|    )
    62|         0|            0|            0|  0.00%|
    63|         0|            0|            0|  0.00%|
    64|         2|  5.72205e-06|  2.86102e-06|  0.00%|def main():
    65|         1|  2.14577e-06|  2.14577e-06|  0.00%|    filename = "data/dataset.csv"
    66|         1|  1.45435e-05|  1.45435e-05|  0.00%|    analyze(filename)
(call)|         1|      9.34844|      9.34844|100.00%|# ./src/poor_perf_v14.py:6 analyze
    67|         0|            0|            0|  0.00%|
    68|         0|            0|            0|  0.00%|
    69|         1|  2.86102e-06|  2.86102e-06|  0.00%|if __name__ == "__main__":
    70|         1|  9.53674e-06|  9.53674e-06|  0.00%|    main()
(call)|         1|      9.34846|      9.34846|100.00%|# ./src/poor_perf_v14.py:64 main
```
Now we're spending a lot more time on that first if, but significantly less time
cascading down the remaining if-else-if chain.

From 2.422 to .469 is a 80.64% reduction in execution time, before cython.

Now we'll cythonize this bad boy...
```
$ python -m cProfile --sort time ./src/poor_perf_v15.py
'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

         28654 function calls (28639 primitive calls) in 0.354 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.340    0.340    0.353    0.353 {src.poor_perf_v15.analyze}
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.005    0.000    0.013    0.000 codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 {built-in method marshal.loads}
        2    0.000    0.000    0.000    0.000 {built-in method _imp.create_builtin}
        6    0.000    0.000    0.000    0.000 {built-in method builtins.__build_class__}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.create_dynamic}
        9    0.000    0.000    0.000    0.000 datetime.py:473(__new__)
.........................abbreviated for length.................................
```

.354 seconds.  That's an 85.38% reduction in execution time.

I think we're just about done.

## C

Nevermind, not quite done, decided to code it again, in C.  I haven't coded C
in a probably a decade, so forgive the code if it's terrible.  That said,
since this is performance hour, I just wanted to see what I could come up with.
I have no clue how / if you can profile C, but again I can time it.

```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson06/assignment/submission/src
$ gcc ./poor_perf_v16.c
$ time ./a.out
ao found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

real    0m0.193s
user    0m0.177s
sys     0m0.016s
```

I hear atoi is bad to use, let's try strtol instead...
```
$ gcc ./poor_perf_v17.c
$ time ./a.out
ao found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305

real	0m0.171s
user	0m0.163s
sys     0m0.008s
```

Maybe some improvement, at this point though, without looping the entire program
thousands of times it's really difficult to make a fair comparison.  Running
this one results in 0.16 - 0.21s times, but the average seemed slightly higher
than v16.