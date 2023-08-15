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
