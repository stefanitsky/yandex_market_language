from tests.cases import ModelTestCase, ET
from tests.factories import PriceFactory
from yandex_market_language.models import Price


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
        expected_el.text = p._value
        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        p = PriceFactory()
        el = p.to_xml()
        self.assertEqual(p.to_dict(), Price.from_xml(el).to_dict())
