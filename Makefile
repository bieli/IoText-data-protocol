test:
	pytest tests/
ci:
	black src/
	black tests/
	black benchmarks/
benchmark:
	py.test benchmarks/IoText_codecs_benchmark_test.py --benchmark-histogram

