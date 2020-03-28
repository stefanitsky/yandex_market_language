import os

from xml.etree import ElementTree as ET
from unittest import TestCase

from yandex_market_language.parser import YMLParser
from yandex_market_language import models


VALID_XML_PATH = os.path.join(
    os.path.dirname(__file__),
    "fixtures/valid_feed.xml"
)


class YMLParserTestCase(TestCase):
    def test_parser_init_with_path(self):
        p = YMLParser(VALID_XML_PATH)
        self.assertIsInstance(p._tree, ET.ElementTree)

    def test_parser_init_with_file(self):
        with open(VALID_XML_PATH) as f:
            p = YMLParser(f)
            self.assertIsInstance(p._tree, ET.ElementTree)

    def test_parser_converts_valid_xml(self):
        p = YMLParser(VALID_XML_PATH)
        self.assertIsInstance(p.parse(), models.Feed)
