from decimal import Decimal
from unittest import TestCase, skip

from src.codecs.iot_ext_codec import IoTextCodec
from src.types.item import Item
from src.types.item_type import ItemTypes, MetricDataItem
from src.types.metric_data import MetricDataTypes

MSG_1_EXAMPLE = (
    """t|3900237526042,d|device_name_001,m|val_water_001=i:1234,m|val_water_002=i:15,m|bulb_state=b:1,"""
    """m|connector_state=b:0,m|temp_01=d:34.4,m|temp_02=d:36.4,m|temp_03=d:10.4,m|pwr=d:12.231,"""
    """m|current=d:1.429,m|current_battery=d:1.548"""
)

MSG_1_EXAMPLE_AS_DATA_STRUCTS = [
    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="3900237526042", metric=None),
    Item(kind=ItemTypes.DEVICE_ID, name="device_name_001", metric=None),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="val_water_001",
        metric=MetricDataItem(data_type=MetricDataTypes.INTEGER, value=1234),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="val_water_002",
        metric=MetricDataItem(data_type=MetricDataTypes.INTEGER, value=15),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="bulb_state",
        metric=MetricDataItem(data_type=MetricDataTypes.BOOL, value=True),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="connector_state",
        metric=MetricDataItem(data_type=MetricDataTypes.BOOL, value=False),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="temp_01",
        metric=MetricDataItem(data_type=MetricDataTypes.DECIMAL, value=Decimal("34.4")),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="temp_02",
        metric=MetricDataItem(data_type=MetricDataTypes.DECIMAL, value=Decimal("36.4")),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="temp_03",
        metric=MetricDataItem(data_type=MetricDataTypes.DECIMAL, value=Decimal("10.4")),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="pwr",
        metric=MetricDataItem(
            data_type=MetricDataTypes.DECIMAL, value=Decimal("12.231")
        ),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="current",
        metric=MetricDataItem(
            data_type=MetricDataTypes.DECIMAL, value=Decimal("1.429")
        ),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="current_battery",
        metric=MetricDataItem(
            data_type=MetricDataTypes.DECIMAL, value=Decimal("1.548")
        ),
    ),
]

MSG_WITH_LISTS_EXAMPLE = (
    """t|3900237526142,d|device_name_002,m|ints_list=I:+1-22+333333,m|bools_list=B:0111"""
    """,m|decimals_list=D:-123.456+1234567890.98765+999.8"""
    """,m|texts_list=T:Wyd8JywgJzphYmMnLCAnISFAJywgJ3h5MHonLCAnMWFiYywnXQ"""
)

MSG_WITH_LISTS_EXAMPLE_AS_DATA_STRUCTS = [
    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="3900237526142", metric=None),
    Item(kind=ItemTypes.DEVICE_ID, name="device_name_002", metric=None),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="ints_list",
        metric=MetricDataItem(
            data_type=MetricDataTypes.INTEGERS_LIST,
            value=[1, -22, 333333],
        ),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="bools_list",
        metric=MetricDataItem(
            data_type=MetricDataTypes.BOOLS_LIST,
            value=[False, True, True, True],
        ),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="decimals_list",
        metric=MetricDataItem(
            data_type=MetricDataTypes.DECIMALS_LIST,
            value=[-123.456, 1234567890.98765, 999.8],
        ),
    ),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="texts_list",
        metric=MetricDataItem(
            data_type=MetricDataTypes.TEXTS_LIST,
            value=["|", ":abc", "!!@", "xy0z", "1abc,"],
        ),
    ),
]

MSG_EXAMPLE_WITH_CRC = """t|123123123123,d|device_one,m|value=d:123.321,c|70AA"""

MSG_EXAMPLE_WITH_CRC_AS_DATA_STRUCTS = [
    Item(kind=ItemTypes.TIMESTAMP_MILIS, name="123123123123", metric=None),
    Item(kind=ItemTypes.DEVICE_ID, name="device_one", metric=None),
    Item(
        kind=ItemTypes.METRIC_ITEM,
        name="value",
        metric=MetricDataItem(
            data_type=MetricDataTypes.DECIMAL, value=Decimal("123.321")
        ),
    ),
    Item(kind=ItemTypes.CRC, name="70AA", metric=None),
]


class IoTextCodecTest(TestCase):
    def test_decode(self):
        expected = MSG_1_EXAMPLE_AS_DATA_STRUCTS

        result = IoTextCodec.decode(MSG_1_EXAMPLE)

        self.assertEqual(expected, result)

    def test_encode(self):
        expected = MSG_1_EXAMPLE
        iotext_msg = MSG_1_EXAMPLE_AS_DATA_STRUCTS

        result = IoTextCodec.encode(iotext_msg)

        self.assertEqual(expected, result)

    def test_lists_encode(self):
        expected = MSG_WITH_LISTS_EXAMPLE
        iotext_list_msg = MSG_WITH_LISTS_EXAMPLE_AS_DATA_STRUCTS

        result = IoTextCodec.encode(iotext_list_msg)

        self.assertEqual(expected, result)

    def test_lists_decode(self):
        expected = MSG_WITH_LISTS_EXAMPLE_AS_DATA_STRUCTS
        iotext_list_msg = MSG_WITH_LISTS_EXAMPLE

        result = IoTextCodec.decode(iotext_list_msg)

        self.assertEqual(expected, result)

    def test_decode_msg_with_crc(self):
        expected = MSG_EXAMPLE_WITH_CRC_AS_DATA_STRUCTS

        result = IoTextCodec.decode(MSG_EXAMPLE_WITH_CRC)
        self.assertEqual(expected, result)
