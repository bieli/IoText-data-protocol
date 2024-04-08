import math
from decimal import Decimal
from unittest import TestCase, skip
from parameterized import parameterized
from src.builders.iot_ext_item_data_builder import IoTextItemDataBuilder
from src.types.item import Item
from src.types.item_type import ItemTypes
from src.types.metric_data import MetricDataTypes
from src.types.metric_data_item import MetricDataItem


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

    def test_should_convert_iotext_msg_to_json(self):
        expected = (
            '[{"t": "3900237526042"}, {"d": "DEV_NAME_002"}, '
            '{"m": "battery_level", "v": 12.07, "t": "d"}, {"m": "open_door", "v": "1", "t": "b"}, '
            '{"m": "open_window", "v": "0", "t": "b"}, {"m": "counter_01", "v": 1234, "t": "i"}, '
            '{"m": "ints_list", "v": [-12, 13, -14], "t": "I"}, '
            '{"c": "94DB"}]'
        )

        builder = IoTextItemDataBuilder(3900237526042, "DEV_NAME_002", add_crc16=True)
        builder.add_measure("battery_level", 12.07)
        builder.add_measure("open_door", True)
        builder.add_measure("open_window", False)
        builder.add_measure("counter_01", 1234)
        builder.add_measure(
            "ints_list", [-12, 13, -14], data_type=MetricDataTypes.INTEGERS_LIST
        )

        result = builder.to_json()

        self.assertEqual(expected, result)

    def test_should_convert_iotext_msg_from_json(self):
        expected_struct = [
            Item(kind=ItemTypes.TIMESTAMP_MILIS, name="3900237526042", metric=None),
            Item(kind=ItemTypes.DEVICE_ID, name="DEV_NAME_002", metric=None),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="battery_level",
                metric=MetricDataItem(
                    data_type=MetricDataTypes.DECIMAL,
                    value=Decimal("12.07"),
                ),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="open_door",
                metric=MetricDataItem(data_type=MetricDataTypes.BOOL, value=True),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="open_window",
                metric=MetricDataItem(data_type=MetricDataTypes.BOOL, value=False),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="counter_01",
                metric=MetricDataItem(data_type=MetricDataTypes.INTEGER, value=1234),
            ),
            Item(
                kind=ItemTypes.METRIC_ITEM,
                name="ints_list",
                metric=MetricDataItem(
                    data_type=MetricDataTypes.INTEGERS_LIST,
                    value=[-12, 13, -14],
                ),
            ),
            Item(
                kind=ItemTypes.CRC,
                name="9838",
                metric=None,
            ),
        ]

        iotext_msg_as_json = (
            '[{"t": "3900237526042"}, {"d": "DEV_NAME_002"}, '
            '{"m": "battery_level", "v": 12.07, "t": "d"}, {"m": "open_door", "v": "1", "t": "b"}, '
            '{"m": "open_window", "v": "0", "t": "b"}, {"m": "counter_01", "v": 1234, "t": "i"}, '
            '{"m": "ints_list", "v": "-12+13-14", "t": "I"}, '
            '{"c": "9838"}]'
        )

        iotext_msg_as_data_struct = IoTextItemDataBuilder.from_json(iotext_msg_as_json)

        self.assertEqual(iotext_msg_as_data_struct, expected_struct)

    def test_should_not_convert_from_json_with_wrong_item_type(self):
        unknown_item_type = "X"
        iotext_msg_as_json = '[{"' + unknown_item_type + '": "xyz"}]'

        with self.assertRaises(ValueError):
            IoTextItemDataBuilder.from_json(iotext_msg_as_json)

    def test_should_not_convert_from_json_with_wrong_data_type_in_metric(self):
        unknown_data_type_in_metric = "Z"
        iotext_msg_as_json = (
            '[{"t": "3900237526042"}, {"d": "DEV_NAME_002"}, {"m": "var", "v": 12.07, "t": "'
            + unknown_data_type_in_metric
            + '"}]'
        )

        with self.assertRaises(ValueError):
            IoTextItemDataBuilder.from_json(iotext_msg_as_json)

    @parameterized.expand(
        [
            (
                '[{"t": "123123123"}, {"d": "D1"}, {"m": "v1", "v": "txt", "t": "t"}]',
                [
                    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="123123123", metric=None),
                    Item(kind=ItemTypes.DEVICE_ID, name="D1", metric=None),
                    Item(
                        kind=ItemTypes.METRIC_ITEM,
                        name="v1",
                        metric=MetricDataItem(
                            data_type=MetricDataTypes.TEXT,
                            value="txt",
                        ),
                    ),
                ],
            ),
            (
                '[{"t": "123123123"}, {"d": "D1"}, {"m": "v1", "v": "-2+3-1", "t": "D"}]',
                [
                    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="123123123", metric=None),
                    Item(kind=ItemTypes.DEVICE_ID, name="D1", metric=None),
                    Item(
                        kind=ItemTypes.METRIC_ITEM,
                        name="v1",
                        metric=MetricDataItem(
                            data_type=MetricDataTypes.DECIMALS_LIST,
                            value="-2+3-1",
                        ),
                    ),
                ],
            ),
            (
                '[{"t": "123123123"}, {"d": "D1"}, {"m": "v1", "v": "10010", "t": "B"}]',
                [
                    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="123123123", metric=None),
                    Item(kind=ItemTypes.DEVICE_ID, name="D1", metric=None),
                    Item(
                        kind=ItemTypes.METRIC_ITEM,
                        name="v1",
                        metric=MetricDataItem(
                            data_type=MetricDataTypes.BOOLS_LIST,
                            value="10010",
                        ),
                    ),
                ],
            ),
            # (
            #     '[{"t": "123123123"}, {"d": "D1"}, {"m": "v1", "v": ["a", "b", "c"], "t": "T"}]',
            #     [
            #         Item(kind=ItemTypes.TIMESTAMP_MILIS, name="123123123", metric=None),
            #         Item(kind=ItemTypes.DEVICE_ID, name="D1", metric=None),
            #         Item(
            #             kind=ItemTypes.METRIC_ITEM,
            #             name="v1",
            #             metric=MetricDataItem(
            #                 data_type=MetricDataTypes.TEXTS_LIST,
            #                 value="YWJjCg",
            #             ),
            #         ),
            #     ],
            # ),
        ]
    )
    def test_should_convert_from_json_with_data_type_in_metric(
        self, iotext_msg_as_json, expected_result
    ):
        result = IoTextItemDataBuilder.from_json(iotext_msg_as_json)
        self.assertTrue(result, expected_result)
