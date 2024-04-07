import math
from unittest import TestCase, skip
from parameterized import parameterized
from src.builders.iot_ext_item_data_builder import IoTextItemDataBuilder


class IoTextItemDataBuilderTest(TestCase):
    @parameterized.expand(
        [
            (12.07, "d:12.07"),
            (True, "b:1"),
            (False, "b:0"),
            (42, "i:42"),
            ("abc", "t:abc"),
        ]
    )
    def test_should_add_measure_and_serialize_to_str(
        self, value, expected_output_suffix
    ):
        metric_name = "example_metric_name"
        expected = (
            f"t|3900237526042,d|DEV_NAME_002,m|{metric_name}={expected_output_suffix}"
        )
        builder = IoTextItemDataBuilder(3900237526042, "DEV_NAME_002")
        builder.add_measure(metric_name, value)

        self.assertEqual(expected, str(builder))

    def test_should_add_a_few_measures_and_serialize_to_str(self):
        expected = (
            "t|3900237526042,d|DEV_NAME_002,m|"
            "battery_level=d:12.07,m|open_door=b:1,m|open_window=b:0,m|counter_01=i:1234"
        )

        builder = IoTextItemDataBuilder(3900237526042, "DEV_NAME_002")
        builder.add_measure("battery_level", 12.07)
        builder.add_measure("open_door", True)
        builder.add_measure("open_window", False)
        builder.add_measure("counter_01", 1234)

        self.assertEqual(expected, str(builder))

    @parameterized.expand(
        [
            (12.07, "d:12.07", "3E3C"),
            (True, "b:1", "D1F8"),
            (False, "b:0", "1139"),
            (42, "i:42", "2350"),
            ("abc", "t:abc", "07A3"),
        ]
    )
    def test_should_add_measure_and_serialize_to_str_with_crc(
        self, value, expected_output_suffix, crc16_value
    ):
        metric_name = "example_metric_name"
        expected = f"t|3900237526042,d|DEV_NAME_002,m|{metric_name}={expected_output_suffix},c|{crc16_value}"
        builder = IoTextItemDataBuilder(3900237526042, "DEV_NAME_002", add_crc16=True)
        builder.add_measure(metric_name, value)

        self.assertEqual(expected, str(builder))

    def test_should_add_a_few_measures_and_serialize_to_str_with_crc(self):
        expected = (
            "t|3900237526042,d|DEV_NAME_002,m|"
            "battery_level=d:12.07,m|open_door=b:1,m|open_window=b:0,m|counter_01=i:1234,c|DCF7"
        )

        builder = IoTextItemDataBuilder(3900237526042, "DEV_NAME_002", add_crc16=True)
        builder.add_measure("battery_level", 12.07)
        builder.add_measure("open_door", True)
        builder.add_measure("open_window", False)
        builder.add_measure("counter_01", 1234)

        self.assertEqual(expected, str(builder))
