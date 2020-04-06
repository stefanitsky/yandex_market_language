from tests import cases, factories
from yandex_market_language import models


class PromoTest(cases.ModelTestCase):
    def test_to_dict(self):
        p = factories.Promo()
        d = p.to_dict()
        expected_dict = dict(
            promo_id=p.promo_id,
            promo_type=p.promo_type,
            start_date=p.start_date,
            end_date=p.end_date,
            description=p.description,
            url=p.url,
        )
        self.assertEqual(d, expected_dict)

    def test_to_xml(self):
        p = factories.Promo()
        el = p.to_xml()

        attribs = {"id": p.promo_id, "type": p.promo_type}
        expected_el = cases.ET.Element("promo", attribs)
        for tag, attr in models.Promo.MAPPING.items():
            el_ = cases.ET.SubElement(expected_el, tag)
            el_.text = getattr(p, attr)

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        p = factories.Promo()
        el = p.to_xml()
        parsed_p = models.Promo.from_xml(el)
        self.assertEqual(p.to_dict(), parsed_p.to_dict())
