from tests import cases, factories
from yandex_market_language import models


class GiftTest(cases.ModelTestCase):
    def test_to_dict(self):
        g = factories.GiftFactory()
        d = g.to_dict()
        expected_dict = dict(id=g.id, name=g.name, pictures=g.pictures)
        self.assertEqual(d, expected_dict)

    def test_to_xml(self):
        g = factories.GiftFactory()
        el = g.to_xml()

        # Create expected element
        expected_el = cases.ET.Element("gift", {"id": g.id})
        name_el = cases.ET.SubElement(expected_el, "name")
        name_el.text = g.name
        for url in g.pictures:
            p_el = cases.ET.SubElement(expected_el, "picture")
            p_el.text = url

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        g = factories.GiftFactory()
        el = g.to_xml()
        parsed_g = models.Gift.from_xml(el)
        self.assertEqual(g.to_dict(), parsed_g.to_dict())
