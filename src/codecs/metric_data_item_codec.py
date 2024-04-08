import ast
import base64
import binascii
import re
from decimal import Decimal
from typing import Optional

from src.types.metric_data import MetricDataTypes
from src.types.metric_data_item import MetricDataItem, MetricValueType


class MetricDataItemCodec:
    INTEGERS_LIST_REGEXP = r"([+-][\d]+)"
    DECIMALS_LIST_REGEXP = r"([+-][\d.]+)"

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
        elif data_type in (
            MetricDataTypes.INTEGERS_LIST.value,
            MetricDataTypes.DECIMALS_LIST.value,
            MetricDataTypes.BOOLS_LIST.value,
            MetricDataTypes.TEXTS_LIST.value,
        ):
            value = MetricDataItemCodec.from_values_list(data_type, value)
        return MetricDataItem(MetricDataTypes(data_type), value)

    @staticmethod
    def encode(mdi: MetricDataItem, data_type_and_value_char: str = ":") -> str:
        value = mdi.value
        if mdi.data_type == MetricDataTypes.INTEGER.value:
            value = str(value)
        elif mdi.data_type == MetricDataTypes.BOOL.value:
            value = "1" if mdi.value == True or mdi.value == "1" else "0"
        elif mdi.data_type == MetricDataTypes.DECIMAL.value:
            value = str(value)
        elif mdi.data_type == MetricDataTypes.TEXT.value:
            value = str(value)
        elif mdi.data_type in (
            MetricDataTypes.INTEGERS_LIST.value,
            MetricDataTypes.DECIMALS_LIST.value,
            MetricDataTypes.BOOLS_LIST.value,
            MetricDataTypes.TEXTS_LIST.value,
        ):
            value = MetricDataItemCodec.to_values_list(mdi.data_type, value)
        return f"{mdi.data_type.value}{data_type_and_value_char}{value}"

    @staticmethod
    def from_value(
        value: MetricValueType, metric_data_type: Optional[MetricDataTypes] = None
    ) -> MetricDataItem:
        if metric_data_type is None:
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
        elif metric_data_type in (
            MetricDataTypes.INTEGERS_LIST,
            MetricDataTypes.DECIMALS_LIST,
            MetricDataTypes.BOOLS_LIST,
            MetricDataTypes.TEXTS_LIST,
        ):
            data_type = metric_data_type
            value = MetricDataItemCodec.from_values_list(
                data_type, MetricDataItemCodec.to_values_list(metric_data_type, value)
            )
        else:
            raise ValueError("Wrong data type selected!")
        return MetricDataItem(data_type, value)

    @staticmethod
    def to_values_list(data_type: MetricDataTypes, value: MetricValueType) -> str:
        list_of_values = []
        if type(value).__name__ == "list":
            if (
                data_type == MetricDataTypes.INTEGERS_LIST.value
                or data_type == MetricDataTypes.DECIMALS_LIST.value
            ):
                list_of_values = [
                    str(value_item) if value_item < 0 else "+" + str(value_item)
                    for value_item in value
                ]
            elif data_type == MetricDataTypes.BOOLS_LIST.value:
                list_of_values = ["1" if value_item else "0" for value_item in value]
            elif data_type == MetricDataTypes.TEXTS_LIST.value:
                ret = base64.b64encode(str(value).encode("utf-8"))
                removed_padding_equals_from_end = ret.decode("utf-8").rstrip("=")
                return removed_padding_equals_from_end

        list_as_str = "".join(list_of_values)
        return list_as_str

    @staticmethod
    def from_values_list(data_type: MetricDataTypes, value: str) -> MetricValueType:
        list_of_values = ""
        if data_type == MetricDataTypes.INTEGERS_LIST.value:
            values_as_str = re.findall(MetricDataItemCodec.INTEGERS_LIST_REGEXP, value)
            list_of_values = [int(value) for value in values_as_str]
        elif data_type == MetricDataTypes.DECIMALS_LIST.value:
            values_as_str = re.findall(MetricDataItemCodec.DECIMALS_LIST_REGEXP, value)
            list_of_values = [float(value) for value in values_as_str]
        elif data_type == MetricDataTypes.BOOLS_LIST.value:
            list_of_values = [
                True if value_item == "1" else False for value_item in value
            ]
        elif data_type == MetricDataTypes.TEXTS_LIST.value:
            list_of_values = ast.literal_eval(
                MetricDataItemCodec.base64_restore_padding(value)
            )
        return list_of_values

    @staticmethod
    def base64_restore_padding(base64_encoded_msg: str) -> str:
        decoded_msg = ""
        n = 0
        while n < 3:
            try:
                decoded_msg = base64.b64decode(base64_encoded_msg + "=" * n).decode(
                    "utf-8"
                )
            except binascii.Error as err:
                if "Incorrect padding" in str(err):
                    pass
                else:
                    raise ValueError(err)
            n += 1
        return decoded_msg
