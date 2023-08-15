from src.codecs.metric_data_item_codec import MetricDataItemCodec
from src.types.item import Item
from src.types.item_type import ItemTypes


class ItemCodec:
    @staticmethod
    def decode(
        item: str,
        split_kind_char: str = "|",
        split_data_item_char: str = "=",
        data_type_and_value_char: str = ":",
    ) -> Item:
        kind, name_and_data_item = item.split(split_kind_char)
        name_and_data_item = name_and_data_item.replace(kind + split_kind_char, "")
        name = name_and_data_item
        mdi = None
        if split_data_item_char in name_and_data_item:
            try:
                name, data_type_and_value = name_and_data_item.replace(
                    kind + split_kind_char, ""
                ).split(split_data_item_char)
                mdi = MetricDataItemCodec.decode(
                    data_type_and_value, data_type_and_value_char
                )
            except TypeError:
                pass
        return Item(ItemTypes(kind), name, mdi)

    @staticmethod
    def encode(
        item: Item, split_kind_char: str = "|", split_data_item_char: str = "="
    ) -> str:
        item_str = f"{item.kind.value}{split_kind_char}{item.name}"
        if item.metric is not None:
            item_str += (
                f"{split_data_item_char}{MetricDataItemCodec.encode(item.metric)}"
            )
        return item_str
