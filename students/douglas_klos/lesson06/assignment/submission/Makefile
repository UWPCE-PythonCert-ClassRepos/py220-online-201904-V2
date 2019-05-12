all: poor_perf_v15 poor_perf_v27

poor_perf_v15: ./src/poor_perf_v15.pyx ./src/poor_perf_v15_setup.py
	python ./src/poor_perf_v15_setup.py build_ext --inplace

# poor_perf_v19: ./src/poor_perf_v19.c
# 	gcc ./src/poor_perf_v19.c -o ./src/poor_perf_v19

# poor_perf_v22: ./src/poor_perf_v22.pyx ./src/poor_perf_v22_setup.py
# 	python ./src/poor_perf_v22_setup.py build_ext --inplace

poor_perf_v27: ./src/poor_perf_v27.c
	gcc ./src/poor_perf_v27.c -o ./src/poor_perf_v27

clean:
	# -rm ./src/*.o $(objects) poor_perf_v15
	-rm ./src/poor_perf_v15.*.so
	-rm ./src/poor_perf_v15.c
	# -rm ./src/poor_perf_v19
	-rm ./src/poor_perf_v27
	-rm -rf ./build/