from tests.cases import ModelTestCase, ET
from tests.factories import DimensionsFactory
from yandex_market_language.models import Dimensions


class DimensionsModelTestCase(ModelTestCase):
    def test_to_dict(self):
        dim = DimensionsFactory()
        d = dim.to_dict()
        self.assertEqual(
            sorted(d.keys()), sorted(["length", "width", "height"])
        )
        self.assertEqual(d["length"], dim.length)
        self.assertEqual(d["width"], dim.width)
        self.assertEqual(d["height"], dim.height)

    def test_to_xml(self):
        dim = DimensionsFactory()
        el = dim.to_xml()
        expected_el = ET.Element("dimensions")
        expected_el.text = "/".join([dim._length, dim._width, dim._height])
        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        d = DimensionsFactory()
        el = d.to_xml()
        parsed_d = Dimensions.from_xml(el)
        self.assertEqual(d.to_dict(), parsed_d.to_dict())
