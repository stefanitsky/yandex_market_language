from tests.cases import ModelTestCase, ET
from tests.factories import PriceFactory
from yandex_market_language.exceptions import ValidationError


class PriceModelTestCase(ModelTestCase):
    def test_to_dict(self):
        p = PriceFactory()
        d = p.to_dict()
        self.assertEqual(sorted(d.keys()), sorted(["value", "is_starting"]))
        self.assertEqual(d["value"], p.value)
        self.assertEqual(d["is_starting"], p.is_starting)

    def test_to_xml(self):
        p = PriceFactory(is_starting=True)
        el = p.to_xml()
        expected_el = ET.Element("price", {"from": "true"})
        expected_el.text = p.value
        self.assertElementsEquals(el, expected_el)

    def test_value_property_error(self):
        with self.assertRaises(ValidationError) as e:
            PriceFactory(value="err")
            self.assertEqual(str(e), "price can be int or float type")
