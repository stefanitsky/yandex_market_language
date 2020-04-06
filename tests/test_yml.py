import os
import re
from operator import attrgetter

from xml.etree import ElementTree as ET
from unittest import TestCase

from tests import factories
from yandex_market_language import models
from yandex_market_language import parse, convert


BASE_DIR = os.path.dirname(__file__)
VALID_XML_PATH = os.path.join(BASE_DIR, "fixtures/valid_feed.xml")
TEST_XML_PATH = os.path.join(BASE_DIR, "test.xml")

pattern = re.compile(r"\s+")


def clean_element_text(el: ET.Element):
    """
    Remove whitespaces, new lines & tabs from element text.
    """
    if el.text:
        el.text = str(el.text)
        el.text = re.sub(pattern, "", el.text)
    else:
        el.text = ""


class YMLTestCase(TestCase):
    def assertElementsEquals(self, el1, el2):
        clean_element_text(el1)
        clean_element_text(el2)
        self.assertEqual(el1.text, el2.text)
        self.assertEqual(el1.attrib, el2.attrib)

    def compare_elements(self, el1, el2):
        self.assertElementsEquals(el1, el2)

        # Debug message
        print("SUCCESS COMPARE: {0} == {1}".format(el1.tag, el2.tag))
        if el1.tag == "offer":
            print("ENTERED IN OFFER: ", el1.attrib["id"])

        # Sort elements by key
        el1[:] = sorted(el1, key=attrgetter("tag"))
        el2[:] = sorted(el2, key=attrgetter("tag"))

        # Call compare recursively
        for el1_, el2_ in zip(el1, el2):
            self.assertEqual(el1_.tag, el2_.tag)
            self.compare_elements(el1_, el2_)

    def test_parses_valid_xml(self):
        feed = parse(VALID_XML_PATH)

        source_xml = ET.parse(VALID_XML_PATH).getroot()
        expected_xml = feed.to_xml()

        self.assertIsInstance(feed, models.Feed)
        self.compare_elements(source_xml, expected_xml)

    def test_converts_valid_feed(self):
        feed = factories.Feed()
        convert(TEST_XML_PATH, feed)
        parsed_feed = parse(TEST_XML_PATH)
        os.remove(TEST_XML_PATH)
        self.assertEqual(feed.to_dict(), parsed_feed.to_dict())
