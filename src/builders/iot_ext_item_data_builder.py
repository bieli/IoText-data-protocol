from typing import List

from src.codecs.item_codec import ItemCodec
from src.codecs.metric_data_item_codec import MetricDataItemCodec
from src.tools.crc16 import Tools
from src.types.item import Item
from src.types.item_type import ItemTypes
from src.types.metric_data_item import MetricValueType


class IoTextItemDataBuilder:
    def __init__(
        self, timestamp: int, device_name: str, add_crc16: bool = False
    ) -> None:
        self.timestamp: int = timestamp
        self.device_name: str = device_name
        self.output: List[Item] = []
        self.metrics: List[Item] = []
        self.add_crc16 = add_crc16

    def add_measure(self, metric_name: str, metric_value: MetricValueType) -> None:
        item = Item(
            kind=ItemTypes.METRIC_ITEM,
            name=metric_name,
            metric=MetricDataItemCodec.from_value(metric_value),
        )
        self.metrics.append(item)

    def __prepare_msg(self, items_separator=","):
        return items_separator.join([ItemCodec.encode(item) for item in self.output])

    def __str__(self, items_separator=",") -> str:
        self.output.append(Item(ItemTypes.TIMESTAMP_MILIS, str(self.timestamp)))
        self.output.append(Item(ItemTypes.DEVICE_ID, self.device_name))
        for metric_item in self.metrics:
            self.output.append(metric_item)
        if self.add_crc16:
            msg = self.__prepare_msg(items_separator=items_separator)
            self.output.append(Item(ItemTypes.CRC, Tools.crc16(msg)))
        return self.__prepare_msg(items_separator=items_separator)
