from decimal import Decimal

from src.types.metric_data import MetricDataTypes
from src.types.metric_data_item import MetricDataItem, MetricValueType


class MetricDataItemCodec:
    @staticmethod
    def decode(
        data_type_and_value: str, data_type_and_value_char: str = ":"
    ) -> MetricDataItem:
        data_type, value = data_type_and_value.split(data_type_and_value_char)
        if data_type == MetricDataTypes.INTEGER.value:
            value = int(value)
        elif data_type == MetricDataTypes.BOOL.value:
            value = value == "1"
        elif data_type == MetricDataTypes.DECIMAL.value:
            value = Decimal(value)
        elif data_type == MetricDataTypes.TEXT.value:
            value = str(value)
        return MetricDataItem(MetricDataTypes(data_type), value)

    @staticmethod
    def encode(mdi: MetricDataItem, data_type_and_value_char: str = ":") -> str:
        value = mdi.value
        if mdi.data_type == MetricDataTypes.INTEGER.value:
            value = str(value)
        elif mdi.data_type == MetricDataTypes.BOOL.value:
            value = "1" if mdi.value == True else "0"
        elif mdi.data_type == MetricDataTypes.DECIMAL.value:
            value = str(value)
        elif mdi.data_type == MetricDataTypes.TEXT.value:
            value = str(value)
        return f"{mdi.data_type.value}{data_type_and_value_char}{value}"

    @staticmethod
    def from_value(value: MetricValueType) -> MetricDataItem:
        if type(value).__name__ == "int":
            data_type = MetricDataTypes.INTEGER
        elif type(value).__name__ == "bool":
            data_type = MetricDataTypes.BOOL
            value = "1" if value == True else "0"
        elif isinstance(value, Decimal) or isinstance(value, float):
            data_type = MetricDataTypes.DECIMAL
        elif isinstance(value, str):
            data_type = MetricDataTypes.TEXT
        else:
            data_type = MetricDataTypes.TEXT
        return MetricDataItem(data_type, value)
