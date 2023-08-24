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
