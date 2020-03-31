from tests.cases import ModelTestCase, ET
from tests.factories import DimensionsFactory
from yandex_market_language.exceptions import ValidationError


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

    def test_value_is_float_raises_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            DimensionsFactory(length="err")
            self.assertEqual(str(e), "length must be a valid float")
