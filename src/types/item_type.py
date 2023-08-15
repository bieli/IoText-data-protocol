from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .metric_data_item import MetricDataItem


class ItemTypes(str, Enum):
    TIMESTAMP_MILIS = "t"
    DEVICE_ID = "d"
    METRIC_ITEM = "m"
    HEALTH_CHECK = "h"
