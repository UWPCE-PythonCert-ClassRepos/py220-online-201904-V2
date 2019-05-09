# Lesson 06 - Profiling and performance

These tests are being run on the following hardware:

Core i7-6700k @ 4.3GHz, 32GB DDR4, Linux Mint 19 (4.15), fairly worn SSD drive.

First, the good\_perf.py file simple loads the analyze function from the best
performing version.

I am submitting this with the pytest file pointing to the original poor_perf.py
delivered to us and the fastest Cython build for the best python-based
comparison.

As far as linting goes, I have linted my program to generate the dataset, and
the python files in the submission/src folder.  I am not linting all the trials.
This means if you run pylint ./src/ from inside submission it _should_ be all
10's, if you do this in trials it will fail miserably.

I'd like to take this opportunity to explain some of my objectives of this
Python class.  I have a B.S. Comp Sci but outside of this class have done very
little programming for that past decade.  I wanted to bring my knowledge back up
to speed a bit and make myself employable again, part of this self improvement
process is playing with other lanaguges, such as Java and C.  So for part of
this assignment I coded things in Java and C for speed comparisons.  Please note
that all assignment requirements are met from a strictly Python perspective,
this just turned into a bigger journey into coding, which has been a very
positive learning experience.

The included <span>ANALYSIS.md</span> file in this same folder is the record
I kept of progress and test results as I progressed through the assignment.

pprofile was a useful package found on Pypi that profiled based on time spent
on each line of code vs time spent in each function, this let me determine I
was wasting time on if's, and that an additional if to rule them all would
speed things up.

## General commands used

Makefile is a work in progress, I have little experience creating them, but am
giving it a shot - it does appear to be working for the .c and .pyx files.

If you're trying to run something and gettin a module not found error, there's
a good chance you need to bulid the file first.  Try 'make all', see below.


```
$ pwd
~/git/py220-online-201904-V2/students/douglas_klos/lesson06/assignment/submission/
$
$ ./src/generate_data.py
$
$ python ./src/poor_perf_v15_setup.py build_ext --inplace
$ ./src/good_perf.py
$
$ python -m cProfile --sort time ./src/poor_perf_v14.py
$ python -m cProfile --sort time ./src/poor_perf_v15.py
$
$ pprofile --exclude-syspath ./src/poor_perf_v14.py > output14.txt
$
$ pylint ./src/
$ pytest ./tests/
$
$ make clean
$ make all
$
$ make clean
$ make poor_perf_v15
$ make poor_perf_v27
$ ./src/poor_perf_v27
```

## Conclusion

I'm surprised by the amount I was able to improve the performance.
The first program given to us was pretty bad, had extra loops
and assignments that didn't work, plus lots of extra if's.  It
clocked in at 2.422 seconds.  Following is a list of times, notable ones
in bold are included in the submission folder, the others are relegated to
the trials folder.

21 & 23 are also interesting since I made use of map and lambda in them, they
were however a tad slower, I still like them.

These times are only relative to each other, and dependent upon the
environment they were run in, such as CPU, OS, and background processes
at the time they were run.  They are not to be used for cross machine or cross
dataset comparison.  They are only valid relative to each other using the same
dataset.

% Decrease = ((Original Number - New Number) ÷ Original Number) × 100

### Noteable times
<pre>
poor_pref_v00.py     =  2.422 # Original time
poor_pref_v14.py     =  0.411 # 83.03% reduction in execution time
poor_pref_v15.pyx    =  0.347 # 85.67% reduction in execution time
poor_perf_v27.c      =  0.155 # 93.6% reduction in execution time
</pre>

### All times
<pre>
<b>poor_pref_v00.py     =  2.422 # Original time</b>
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
<b>poor_pref_v14.py     =  0.411 # Added if to filter other if's</b>
<b>poor_pref_v15.pyx    =  0.347 # Cythonized int's and str from #14</b>
poor_pref_v16.c      =  0.193 # Sloppy C
poor_perf_v17.c      =  0.171 # Slightly better C?
poor_perf_v18.c      =  0.164 # 100 loops / 100
poor_perf_v19.c      =  0.162 # Pickier C, bad inputs will seg fauilt.
poor_perf_v20.py     =  717m27.297s # Clearly something went wrong... Yeah I let it run...
poor_perf_v21.py     =  0.448 # refactored and introduced map.
poor_perf_v22.pyx    =  XXXXX # Cythonized v21, breaks map somehow.
<b>poor_perf_v23.py     =  0.470 # Fun with map</b>
poor_perf_v24.py     =  5.138 # Tried a JIT compiler called numba.
poor_perf_v25.py     =  1.570 # Replaced if's with regex
poor_perf_v26.c      =  0.160 # Replaced if's with else if<
<b>poor_perf_v27.c      =  0.155 # Added proper struct</b>
</pre>
