from tests import cases, factories
from yandex_market_language import models


class PromoTest(cases.ModelTestCase):
    def test_to_dict(self):
        p = factories.Promo()
        d = p.to_dict()
        expected_dict = dict(
            promo_id=p.promo_id
        )
        self.assertEqual(d, expected_dict)

    def test_to_xml(self):
        p = factories.Promo()
        el = p.to_xml()
        expected_el = cases.ET.Element("promo", {"id": p.promo_id})
        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        p = factories.Promo()
        el = p.to_xml()
        parsed_p = models.Promo.from_xml(el)
        self.assertEqual(p.to_dict(), parsed_p.to_dict())
