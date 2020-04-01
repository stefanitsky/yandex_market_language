import os

from xml.etree import ElementTree as ET
from unittest import TestCase

from yandex_market_language import models
from yandex_market_language.parser import YMLParser


VALID_XML_PATH = os.path.join(
    os.path.dirname(__file__),
    "fixtures/valid_feed.xml"
)


class YMLParserTestCase(TestCase):
    def test_parser_converts_valid_xml(self):
        p = YMLParser(VALID_XML_PATH)
        feed = p.parse()
        xml_feed = ET.tostring(ET.parse(VALID_XML_PATH).getroot())
        expected_xml_feed = ET.tostring(feed.to_xml())
        self.assertIsInstance(feed, models.Feed)
        self.assertEqual(xml_feed, expected_xml_feed)
