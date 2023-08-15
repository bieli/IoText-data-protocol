ci:
	black src/
	black tests/
benchmark:
	py.test benchmarks/IoText_codecs_benchmark_test.py --benchmark-histogram

