import unittest

from src.tools.crc16 import Tools


class ToolsTest(unittest.TestCase):
    def test_should_crc16(self):
        self.assertEqual("5749", Tools.crc16("abc"))

    def test_should_iotext_message_with_crc16(self):
        example_iotext_msg = "t|123123123123,d|device_one,m|value=d:123.321"
        self.assertEqual("4C5A", Tools.crc16(example_iotext_msg))

    def test_should_crc16_with_empty_string(self):
        self.assertEqual("FFFF", Tools.crc16(""))
