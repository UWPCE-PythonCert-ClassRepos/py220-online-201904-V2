all: poor_perf_v08.c 

poor_perf_v08.c: poor_perf_v08.pyx good_perf_setup.py
	python good_perf_setup.py build_ext --inplace

