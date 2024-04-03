from enum import Enum


class MetricDataTypes(str, Enum):
    INTEGER = "i"
    BOOL = "b"
    DECIMAL = "d"
    TEXT = "t"
    INTEGERS_LIST = "I"
    BOOLS_LIST = "B"
    DECIMALS_LIST = "D"
    TEXTS_LIST = "T"
