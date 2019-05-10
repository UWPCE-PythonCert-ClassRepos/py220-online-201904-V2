

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
First, execution time of around 2.4 seconds for a million records is better
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

# C

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

real    0m0.171s
user    0m0.163s
sys     0m0.008s
```

Maybe some improvement, at this point though, without looping the entire program
thousands of times it's really difficult to make a fair comparison.  Running
this one results in 0.16 - 0.21s times, but the average seemed slightly higher
than v16.

18 We're just adding in a loop counter too get a time for multiple runs of
the program, it goes too quickly to properly judge a single run.  This is for
100 loops through the program.

```
$ gcc ./poor_perf_v18.c
$ time ./a.out

real     0m16.446s = .16446s per loop
user     0m15.134s = .15134s per loop
sys      0m1.312s  = .01312s per loop
```

19 We're going to make a couple small changes and see how it reacts.  These
will make it more picky on data but it will still work with our data generator.
Replacing strlen(ptr)-4 with the static length of 6 that our data meets.

```
$ gcc ./poor_perf_v19.c
$ time ./a.out

real    0m15.262s = .15262s per loop
user    0m13.874s = .13874s per loop
sys     0m1.388s  = .01388s per loop
```

So about .153 seconds per loop

That's a 93.72% reduction in execution time over the original, terrible
poor_perf.py, and a 67.59% reduction in execution time over my best Python
implementation.  That said, I'm not returning the extensive dataset in C
that Python is at the end of the function.  Perhaps I'll code up a struct?

So v20 has been running for a couple hours and is still going strong, clearly
not a winner, but I'm curious if it still finishes with the correct results

```
'ao' was found 0 times
2013:89	2014:106	2015:104	2016:110	2017:88	2018:93


real    717m27.297s
user    717m9.587s
sys     0m11.837s
```



v21 we introduce Map and to my surprise it speed things up a tad!

```
$ time ./src/poor_perf_v21.py

'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305


real    0m0.437s
user    0m0.421s
sys     0m0.016s
```

81.96% improvment over the original.

v22 was suppose to be a cythonized v21, however cython appears to be doing some
odd stuff with map, as it's not passing the correct values.

v23 is probably the one I like the most, it was fun to write.  We've got a
couple of maps and a lambda doing the main iteration and function call.  It's
not as fast as the single map version, but I like it.

```
$ time ./src/poor_perf_v23.py

'ao' was found 35966 times
2013:8362	2014:8332	2015:8055	2016:8532	2017:8363	2018:8305


real    0m0.481s
user    0m0.469s
sys     0m0.012s
```

v24 we tried a JIT compiler called numba.  Didn't have good resultsl, but didn't
optimize code for it either.


```
$ time ./src/poor_perf_v24.py

'ao' was found 35966 times
2013:8362   2014:8332   2015:8055   2016:8532   2017:8363   2018:8305


real    0m5.138s
user    0m5.178s
sys     0m0.344s
```

I ran v14 in a loop of 100, good results...
```
$ time ./src/poor_perf_v24.py

real    0m41.166s = .41166 per loop
user    0m39.666s = .39666 per loop
sys     0m1.500s  = .01500 per loop
```

v23 100 times
```
real    0m47.176s
user    0m45.737s
sys     0m1.436s
```

v21 100 times
```
real    0m44.882s
user    0m43.312s
sys     0m1.496s
```

so v14 is still king of pure python, though maps are fun.

v15 100 times
```
real    0m34.734s
user    0m33.062s
sys     0m1.673s
```

Decided to cprofile my data generator
```
akeyla@reactor:~/git/py220-online-201904-V2/students/douglas_klos/lesson06/assignment/submission$ python -m cProfile --sort time ./src/generate_data.py 
         239956379 function calls (239956156 primitive calls) in 87.985 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  2000000   11.140    0.000   20.286    0.000 _strptime.py:318(_strptime)
  4999074    8.956    0.000   29.457    0.000 statistic_wordgen.py:27(gen_word)
 23319684    8.956    0.000   13.245    0.000 random.py:224(_randbelow)
 20319684    6.311    0.000   18.745    0.000 random.py:256(choice)
  2000000    4.111    0.000    4.111    0.000 {built-in method time.mktime}
  1000001    3.272    0.000   87.126    0.000 generate_data.py:19(generate_rows)
 31184545    3.033    0.000    3.033    0.000 {method 'getrandbits' of '_random.Random' objects}
44087875/44087843    2.923    0.000    2.923    0.000 {built-in method builtins.len}
  1000000    2.438    0.000   34.045    0.000 statistic_wordgen.py:19(gen_text)
  2000000    2.322    0.000   24.373    0.000 {built-in method time.strptime}
  1000004    2.315    0.000    2.973    0.000 uuid.py:121(__init__)
  1000000    2.311    0.000   41.729    0.000 document_generator.py:111(gen_sentence)
  3000000    1.954    0.000    4.159    0.000 random.py:174(randrange)
  1000000    1.879    0.000   32.276    0.000 generate_data.py:46(rand_date)
  2000000    1.764    0.000   22.050    0.000 _strptime.py:568(_strptime_time)
  1000008    1.516    0.000    1.516    0.000 {method 'sub' of 're.Pattern' objects}
  1000000    1.467    0.000    1.467    0.000 uuid.py:264(__str__)
  2000002    1.339    0.000    1.849    0.000 locale.py:384(normalize)
  2000000    1.319    0.000    1.319    0.000 {method 'match' of 're.Pattern' objects}
 23319685    1.256    0.000    1.256    0.000 {method 'bit_length' of 'int' objects}
  1000000    1.230    0.000    1.230    0.000 {built-in method posix.urandom}
  1000000    1.157    0.000    5.360    0.000 uuid.py:757(uuid4)
  3000000    1.037    0.000    5.197    0.000 random.py:218(randint)
  1000008    0.979    0.000    0.979    0.000 {built-in method time.strftime}
 15718869    0.972    0.000    0.972    0.000 {method 'random' of '_random.Random' objects}
  2000002    0.941    0.000    4.451    0.000 locale.py:571(getlocale)
  1000000    0.934    0.000    0.934    0.000 {built-in method time.localtime}
  2000002    0.923    0.000    0.923    0.000 {built-in method _locale.setlocale}
        1    0.843    0.843   87.969   87.969 {method 'writelines' of '_io._IOBase' objects}
  6000563    0.785    0.000    0.785    0.000 {built-in method builtins.isinstance}
  2000002    0.763    0.000    5.214    0.000 _strptime.py:26(_getlang)
  1000010    0.750    0.000    1.127    0.000 re.py:271(_compile)
  2000002    0.738    0.000    2.587    0.000 locale.py:467(_parse_localename)
  6000088    0.684    0.000    0.684    0.000 {method 'get' of 'dict' objects}
  2000000    0.655    0.000    0.655    0.000 {method 'groupdict' of 're.Match' objects}
  1000000    0.613    0.000   42.437    0.000 document_generator.py:94(sentence)
  1000000    0.520    0.000    3.163    0.000 re.py:185(sub)
  4999540    0.515    0.000    0.515    0.000 {method 'append' of 'list' objects}
  4000001    0.358    0.000    0.358    0.000 {method 'toordinal' of 'datetime.date' objects}
  1000042    0.281    0.000    0.281    0.000 {built-in method from_bytes}
  1000263    0.272    0.000    0.272    0.000 {method 'join' of 'str' objects}
  1000079    0.231    0.000    0.231    0.000 {method 'replace' of 'str' objects}
  2000000    0.213    0.000    0.213    0.000 {method 'end' of 're.Match' objects}
  2000049    0.207    0.000    0.207    0.000 {method 'lower' of 'str' objects}
  2000000    0.186    0.000    0.186    0.000 {method 'keys' of 'dict' objects}
  1000004    0.179    0.000    0.179    0.000 {method 'count' of 'list' objects}
  2000000    0.169    0.000    0.169    0.000 {method 'weekday' of 'datetime.date' objects}
  1000004    0.126    0.000    0.126    0.000 {method 'strip' of 'str' objects}
  1000000    0.123    0.000    0.123    0.000 {method 'upper' of 'str' objects}
```
Lots of time in that strptime function.


We tried out a regular expression for v25 instead of if statements


100 loops...
```
real    2m37.009s = 1.5s per loop
user    2m35.327s
sys     0m1.644s
```
Not great, but was worth a shot.


v26 we replaced if's with else if.  I had to compare back to back with v19,
again loops of 100.

```
$ time ./src/poor_perf_v19

real	0m16.234s
user	0m14.439s
sys	0m1.691s

$ time ./src/poor_perf_v26

real	0m16.047s
user	0m14.463s
sys	0m1.584s
```

What I think to be proper C including a struct

```
$ ./src/poor_perf_v27

real    0m15.537s = .15537s per loop
user    0m13.922s = .13922s per loop
sys     0m1.616s  = .01616s per loop
```


We trie v27.c from a ramdisk again, no change...

```
$ sudo mkdir /mnt/ramdisk
$ sudo mount -t tmpfs -o size=1024m tmpfs /mnt/ramdisk/
$ cp -R ../assignment/ /mnt/ramdisk/
$ cd /mnt/ramdisk
$ time ./src/poor_perf_v06.py

real    0m15.800s
user    0m14.256s
sys     0m1.544s
```
I also tried v27 on 10 million records looping 10 times on a ramdisk, no
noticeable improvement from running from RAM at this size file.

One more test, v28, it's v14 converted to python2 :D

```
$ time /usr/bin/python2 ./src/poor_perf_v28.py


real    0m36.610s = .36610s per loop
user    0m35.239s = .35239s per loop
sys     0m1.340s  = .01340s per loop
```
lol, that's our best pure python time so far!

v29 a single if and a dictionary again
```
$ ./src/poor_pref_v29.py


real    0m42.966s
user    0m41.562s
sys     0m1.404s
```

Ran 14 again for comparison, int's still faster
```
$ ./src/poor_pref_v14.py

real    0m40.586s
user    0m39.346s
sys     0m1.240s
```

Remember these are loops of 100 throught the million records.  
Those dictionary hash calls take up time!

v30 we added an extra if.
```
if "2012" < lrow[5][6:] < "2019":
```
the < 2019 part

It didn't seem to make an improvement in my dataset, but if there were a 
significant number of dates above the 2018 cutoff point it would begin to
be an improvement.

## Parallel

Decided to try coding a multiprocess version of this.  Haven't recorded the
first few times, they weren't exciting, worse than the single thread.
But we're making progress!

As a baseline for the day, I'm rerunning specimen 14 in loops of 10
```
real    0m4.068s
user    0m3.948s
sys     0m0.120s
```

As of now, 'real' time is what we're concerned with, as the other two will
related to CPU time and kernel time used, but we want a wall-clock 
comparison, and that's real time.

Currently for parallel_v3
```
real    0m4.093s
user    0m4.828s
sys     0m1.533s
```

Yes, it's a tad slower in real time than the single thread, but I think we
can improve upon this.

Too funny, as it turns out, my very first parallel implementation is the
fastest so far!

parallel_v1
```
real    0m3.524s
user    0m5.254s
sys     0m0.727s
```
so .352 seconds per loop!  I had been reading user time before and saw that
it was much higher.  So what's different in version one, well, i'm not using
slicing, and it's actually reading the file twice instead of just once, but only
going half way through each time.

v5
```
real    0m32.128s
user    0m53.133s
sys     0m19.929s
```

v6 - trying generators to feed consume... not so much.  Apparently
profiling multiprocess is problematic, this gave me not much.
```
$ python -m cProfile --sort time ./src/parallel_v6.py 
'ao' was found 35233 times
2013:8326	2014:8289	2015:8013	2016:8497	2017:8326	2018:8258

         50882 function calls (50470 primitive calls) in 0.671 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.493    0.164    0.493    0.164 {built-in method posix.waitpid}
        1    0.098    0.098    0.615    0.615 parallel_v6.py:91(main)
        1    0.044    0.044    0.671    0.671 parallel_v6.py:2(<module>)
    13875    0.008    0.000    0.008    0.000 {built-in method _codecs.utf_8_decode}
    13875    0.004    0.000    0.012    0.000 codecs.py:319(decode)
        2    0.003    0.001    0.003    0.001 {built-in method posix.fork}
       34    0.002    0.000    0.002    0.000 {built-in method marshal.loads}
        6    0.001    0.000    0.001    0.000 {built-in method _imp.create_dynamic}
      132    0.001    0.000    0.002    0.000 {built-in method builtins.__build_class__}
      149    0.001    0.000    0.001    0.000 enum.py:375(__setattr__)
      111    0.001    0.000    0.002    0.000 <frozen importlib._bootstrap_external>:1356(find_spec)
      195    0.001    0.000    0.001    0.000 {built-in method posix.stat}
        7    0.001    0.000    0.002    0.000 enum.py:134(__new__)
```
pprofile just tells me I'm waiting for a thread.
```
   125|         1|  2.69413e-05|  2.69413e-05|  0.00%|        process1.join()
(call)|         1|      10.7872|      10.7872| 94.05%|# /usr/lib/python3.7/multiprocessing/process.py:133 join
   126|         1|  1.23978e-05|  1.23978e-05|  0.00%|        process2.join()
(call)|         1|     0.274074|     0.274074|  2.39%|# /usr/lib/python3.7/multiprocessing/process.py:133 join
```
```
real    0m0.522s
user    0m0.641s
sys     0m0.147s
```
I'm not getting consistent results with multiprocessing anyways.

EUREKA!

parallel_v7 is the first multithread to post correct answers and great times!
```
real    0m3.483s
user    0m5.444s
sys     0m0.620s
```

