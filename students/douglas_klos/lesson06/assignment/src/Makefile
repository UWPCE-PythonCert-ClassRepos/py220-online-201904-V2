all: poor_perf_v7.c 

poor_perf_v7.c: poor_perf_v7.pyx good_perf_setup.py
	python good_perf_setup.py build_ext --inplace

