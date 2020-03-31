from unittest import TestCase
from xml.etree import ElementTree as ET
from faker import Faker

fake = Faker()


class ModelTestCase(TestCase):
    def assertElementsEquals(self, el, expected_el):
        self.assertEqual(ET.tostring(el), ET.tostring(expected_el))
