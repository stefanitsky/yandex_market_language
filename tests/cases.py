from operator import attrgetter
from unittest import TestCase
from xml.etree import ElementTree as ET
from faker import Faker

fake = Faker()


class ModelTestCase(TestCase):
    def assertElementsEquals(self, el, expected_el):
        # Sort elements by key
        el[:] = sorted(el, key=attrgetter("tag"))
        expected_el[:] = sorted(expected_el, key=attrgetter("tag"))

        # Check if elements are equal
        self.assertEqual(ET.tostring(el), ET.tostring(expected_el))
