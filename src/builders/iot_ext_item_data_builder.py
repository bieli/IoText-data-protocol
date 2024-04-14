import json
import decimal
from decimal import Decimal
from typing import List, Optional

from src.codecs.iot_ext_codec import IoTextCodec
from src.codecs.item_codec import ItemCodec
from src.codecs.metric_data_item_codec import MetricDataItemCodec
from src.tools.crc16 import Tools
from src.types.item import Item
from src.types.item_type import ItemTypes
from src.types.metric_data import MetricDataTypes
from src.types.metric_data_item import MetricValueType, MetricDataItem


class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)

def defaultencode(o):
    if isinstance(o, Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")


class IoTextItemDataBuilder:
    def __init__(
        self, timestamp: int, device_name: str, add_crc16: bool = False
    ) -> None:
        self.timestamp: int = timestamp
        self.device_name: str = device_name
        self.output: List[Item] = []
        self.metrics: List[Item] = []
        self.add_crc16 = add_crc16

    def add_measure(
        self,
        metric_name: str,
        metric_value: MetricValueType,
        data_type: Optional[MetricDataTypes] = None,
    ) -> None:
        item = Item(
            kind=ItemTypes.METRIC_ITEM,
            name=metric_name,
            metric=MetricDataItemCodec.from_value(
                metric_value, metric_data_type=data_type
            ),
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

    def to_json(self) -> str:
        self.__str__()
        return IoTextItemDataBuilder.to_json_from_iotext_struct(self.output)

    @staticmethod
    def iotext_to_json(
        iotext_msg,
    ) -> str:
        iotext_msg_struct = IoTextCodec.decode(iotext_msg)
        return IoTextItemDataBuilder.to_json_from_iotext_struct(
            iotext_msg_struct, is_named_metric=False
        )

    @staticmethod
    def iotext_to_json_named_metrics(iotext_msg) -> str:
        iotext_msg_struct = IoTextCodec.decode(iotext_msg)
        return IoTextItemDataBuilder.to_json_from_iotext_struct(
            iotext_msg_struct, is_named_metric=True
        )

    @staticmethod
    def iotext_to_json_one_object(iotext_msg) -> str:
        iotext_msg_struct = IoTextCodec.decode(iotext_msg)
        data_row = {}
        for item in iotext_msg_struct:
            if item.metric is not None:
                data_row[item.name] = item.metric.value
            else:
                data_row[item.kind] = item.name
            data_row.update(data_row)
        return json.dumps(data_row, default=defaultencode)

    @staticmethod
    def to_json_from_iotext_struct(
        iotext_msg_struct, is_named_metric: bool = False
    ) -> str:
        data_row = []
        for item in iotext_msg_struct:
            data_item = {
                item.kind: item.name,
            }
            if item.metric is not None:
                if is_named_metric:
                    data_item = {
                        item.name: item.metric.value,
                        "t": item.metric.data_type,
                    }
                else:
                    val = {"v": item.metric.value, "t": item.metric.data_type}
                    data_item.update(val)
            data_row.append(data_item)
        return json.dumps(data_row)

    @staticmethod
    def from_json(json_iotext_msg) -> List[Item]:
        data_row_from_json = json.loads(json_iotext_msg)
        items = []
        for item in data_row_from_json:
            if len(item.keys()) == 1:
                if "t" in item.keys():
                    val = list(item.values())[0]
                    items.append(
                        Item(kind=ItemTypes.TIMESTAMP_MILIS, name=val, metric=None),
                    )
                elif "d" in item.keys():
                    val = list(item.values())[0]
                    items.append(
                        Item(kind=ItemTypes.DEVICE_ID, name=val, metric=None),
                    )
                elif "c" in item.keys():
                    val = list(item.values())[0]
                    items.append(
                        Item(kind=ItemTypes.CRC, name=val, metric=None),
                    )
                else:
                    raise ValueError(
                        "Not recognized type item in keys: '" + str(item.keys()) + "'"
                    )
            else:
                if "m" in item.keys():
                    if "t" in item.keys():
                        if item["t"] == "i":
                            data_type = MetricDataTypes.INTEGER
                            val = int(item["v"])
                        elif item["t"] == "b":
                            data_type = MetricDataTypes.BOOL
                            val = True if item["v"] == "1" else False
                        elif item["t"] == "d":
                            data_type = MetricDataTypes.DECIMAL
                            val = Decimal(str(item["v"]))
                        elif item["t"] == "t":
                            data_type = MetricDataTypes.TEXT
                            val = str(item["v"])
                        elif item["t"] == "D":
                            data_type = MetricDataTypes.DECIMALS_LIST
                            val = MetricDataItemCodec.from_values_list(
                                data_type, item["v"]
                            )
                        elif item["t"] == "B":
                            data_type = MetricDataTypes.BOOLS_LIST
                            val = MetricDataItemCodec.from_values_list(
                                data_type, item["v"]
                            )
                        elif item["t"] == "I":
                            data_type = MetricDataTypes.INTEGERS_LIST
                            val = MetricDataItemCodec.from_values_list(
                                data_type, item["v"]
                            )
                        elif item["t"] == "T":
                            data_type = MetricDataTypes.TEXTS_LIST
                            val = MetricDataItemCodec.from_values_list(
                                data_type, item["v"]
                            )
                        else:
                            raise ValueError(
                                "Not recognized metric type: '" + item["t"] + "'"
                            )
                    items.append(
                        Item(
                            kind=ItemTypes.METRIC_ITEM,
                            name=item["m"],
                            metric=MetricDataItem(
                                data_type=data_type,
                                value=val,
                            ),
                        )
                    )
        return items
