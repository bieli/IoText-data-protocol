from unittest import TestCase, skip

from src.codecs.metric_data_item_codec import MetricDataItemCodec
from src.types.metric_data import MetricDataTypes
from src.types.metric_data_item import MetricDataItem


class MetricDataItemCodecTest(TestCase):
    def test_decode(self):
        expected = MetricDataItem(MetricDataTypes.INTEGER, 1234)
        msg = "i:1234"

        result = MetricDataItemCodec.decode(msg)

        self.assertEqual(expected, result)

    def test_encode(self):
        expected = "d:100.09"
        mdi = MetricDataItem(MetricDataTypes.DECIMAL, 100.09)

        result = MetricDataItemCodec.encode(mdi)

        self.assertEqual(expected, result)

    def test_from_value_type_int(self):
        expected = MetricDataItem(MetricDataTypes.INTEGER, 42)

        result = MetricDataItemCodec.from_value(42)

        self.assertEqual(expected, result)

    def test_from_value_type_decimal(self):
        expected = MetricDataItem(MetricDataTypes.DECIMAL, 123.01)

        result = MetricDataItemCodec.from_value(123.01)

        self.assertEqual(expected, result)

    def test_from_value_type_text(self):
        expected = MetricDataItem(MetricDataTypes.TEXT, "xyZ")

        result = MetricDataItemCodec.from_value("xyZ")

        self.assertEqual(expected, result)

    def test_from_value_type_bool_true(self):
        expected = MetricDataItem(MetricDataTypes.BOOL, "1")

        result = MetricDataItemCodec.from_value(True)

        self.assertEqual(expected, result)

    def test_from_value_type_bool_true(self):
        expected = MetricDataItem(MetricDataTypes.BOOL, "0")

        result = MetricDataItemCodec.from_value(False)

        self.assertEqual(expected, result)

    def test_to_values_list_type_integers_list(self):
        list_of_ints = [0, -123, 555, -99999999]
        expected = "+0-123+555-99999999"

        result = MetricDataItemCodec.to_values_list(MetricDataTypes.INTEGERS_LIST, list_of_ints)

        self.assertEqual(expected, result)

    def test_to_values_list_type_decimals_list(self):
        list_of_ints = [0.12345, -1.123, 123123123.555, -111111111.99999999]
        expected = "+0.12345-1.123+123123123.555-111111111.99999999"

        result = MetricDataItemCodec.to_values_list(MetricDataTypes.DECIMALS_LIST, list_of_ints)

        self.assertEqual(expected, result)

    def test_to_values_list_type_bools_list(self):
        list_of_bools = [False, True, False, True]
        expected = "0101"

        result = MetricDataItemCodec.to_values_list(MetricDataTypes.BOOLS_LIST, list_of_bools)

        self.assertEqual(expected, result)

    def test_to_values_list_type_texts_list_without_bas64_paddings(self):
        list_of_texts = ['|', ':abc', '!!@', 'xy0z', '1abc,']
        expected = "Wyd8JywgJzphYmMnLCAnISFAJywgJ3h5MHonLCAnMWFiYywnXQ"

        result = MetricDataItemCodec.to_values_list(MetricDataTypes.TEXTS_LIST, list_of_texts)

        self.assertEqual(expected, result)

    def test_from_values_list_type_integers_list(self):
        expected = [0, -123, 555, -99999999]
        input_str = "+0-123+555-99999999"

        result = MetricDataItemCodec.from_values_list(MetricDataTypes.INTEGERS_LIST, input_str)

        self.assertEqual(expected, result)

    def test_from_values_list_type_decimals_list(self):
        expected = [0.12345, -1.123, 123123123.555, -111111111.99999999]
        input_str = "+0.12345-1.123+123123123.555-111111111.99999999"

        result = MetricDataItemCodec.from_values_list(MetricDataTypes.DECIMALS_LIST, input_str)

        self.assertEqual(expected, result)

    def test_from_values_list_type_bools_list(self):
        expected = [False, True, False, True]
        input_str = "0101"

        result = MetricDataItemCodec.from_values_list(MetricDataTypes.BOOLS_LIST, input_str)

        self.assertEqual(expected, result)

    def test_from_values_list_type_texts_list_without_base64_paddings(self):
        expected = ['|', ':abc', '!!@', 'xy0z', '1abc,']
        input_str = "Wyd8JywgJzphYmMnLCAnISFAJywgJ3h5MHonLCAnMWFiYywnXQ"

        result = MetricDataItemCodec.from_values_list(MetricDataTypes.TEXTS_LIST, input_str)

        self.assertEqual(expected, result)

    def test_base64_restore_padding_without_padding(self):
        expected = '123'
        input_str = "MTIz"

        result = MetricDataItemCodec.base64_restore_padding(input_str)

        self.assertEqual(expected, result)

    def test_base64_restore_padding_with_padding_original(self):
        expected = 'Hello from IoText data protocol'
        input_str = "SGVsbG8gZnJvbSBJb1RleHQgZGF0YSBwcm90b2NvbA=="

        result = MetricDataItemCodec.base64_restore_padding(input_str)

        self.assertEqual(expected, result)


    def test_base64_restore_padding_with_padding_removed(self):
        expected = 'Hello from IoText data protocol'
        # original base64 string has "==" at the end - removed for unit testing
        input_str = "SGVsbG8gZnJvbSBJb1RleHQgZGF0YSBwcm90b2NvbA"

        result = MetricDataItemCodec.base64_restore_padding(input_str)

        self.assertEqual(expected, result)
