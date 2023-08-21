import time
import pytest
import json

from src.codecs.iot_ext_codec import IoTextCodec

MSG_1_EXAMPLE = """t|3900237526042,d|device_name_001,m|val_water_001=i:1234,m|val_water_002=i:15,m|bulb_state=b:1,m|connector_state=b:0,m|temp_01=d:34.4,m|temp_02=d:36.4,m|temp_03=d:10.4,m|pwr=d:12.231,m|current=d:1.429,m|current_battery=d:1.548"""
MSG_1_EXAMPLE_DECODED = IoTextCodec.decode(MSG_1_EXAMPLE)
MSG_1_EXAMPLE_JSON = """[{"t":3900237526042},{"d":"device_name_001"},{"m":[{"val_water_001":{"i":1234}},{"val_water_002":{"i":15}},{"bulb_state":{"b":1}},{"connector_state":{"b":0}},{"temp_01":{"d":"34.4"}},{"temp_02":{"d":"36.4"}},{"temp_03":{"d":"10.4"}},{"pwr":{"d":"12.231"}},{"current":{"d":"1.429"}},{"current_battery": {"d":"1.548"}}]}]"""

MIN_TESTS_ROUNDS = 100


@pytest.mark.benchmark(
    group="bench",
    min_time=0.1,
    max_time=0.5,
    min_rounds=MIN_TESTS_ROUNDS,
    timer=time.time,
    disable_gc=True,
    warmup=False,
)
def test_iotext_data_protocol_decode_python(benchmark):
    @benchmark
    def result():
        IoTextCodec.decode(MSG_1_EXAMPLE)

    # Extra code, to verify that the run
    # completed correctly.
    # Note: this code is not measured.
    assert result is None


@pytest.mark.benchmark(
    group="bench",
    min_time=0.1,
    max_time=0.5,
    min_rounds=MIN_TESTS_ROUNDS,
    timer=time.time,
    disable_gc=True,
    warmup=False,
)
def test_iotext_data_protocol_encode_python(benchmark):
    @benchmark
    def result():
        IoTextCodec.encode(MSG_1_EXAMPLE_DECODED)

    # Extra code, to verify that the run
    # completed correctly.
    # Note: this code is not measured.
    assert result is None


@pytest.mark.benchmark(
    group="bench",
    min_time=0.1,
    max_time=0.5,
    min_rounds=MIN_TESTS_ROUNDS,
    timer=time.time,
    disable_gc=True,
    warmup=False,
)
def test_json_decode_python(benchmark):
    @benchmark
    def result():
        json.loads(MSG_1_EXAMPLE_JSON)

    # Extra code, to verify that the run
    # completed correctly.
    # Note: this code is not measured.
    assert result is None
