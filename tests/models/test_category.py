from tests.cases import ModelTestCase, ET
from tests.factories import CategoryFactory
from yandex_market_language.models import Category


class CategoryModelTestCase(ModelTestCase):
    def test_to_dict(self):
        c = CategoryFactory()
        d = c.to_dict()
        self.assertEqual(sorted(d.keys()), sorted(["id", "name", "parent_id"]))
        self.assertEqual(d["id"], c.category_id)
        self.assertEqual(d["name"], c.name)
        self.assertEqual(d["parent_id"], c.parent_id)

    def test_to_xml(self):
        c = CategoryFactory(parent_id=None)
        el = c.to_xml()
        expected_el = ET.Element("category", {"id": c.category_id})
        expected_el.text = c.name
        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        c = CategoryFactory()
        el = c.to_xml()
        parsed_c = Category.from_xml(el)
        self.assertEqual(c.to_dict(), parsed_c.to_dict())
