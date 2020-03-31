from tests.cases import ModelTestCase, ET
from tests.factories import OptionFactory


class OptionModelTestCase(ModelTestCase):
    def test_to_dict(self):
        o = OptionFactory()
        d = o.to_dict()
        self.assertEqual(
            sorted(d.keys()), sorted(["cost", "days", "order_before"])
        )
        self.assertEqual(d["cost"], o.cost)
        self.assertEqual(d["days"], o.days)
        self.assertEqual(d["order_before"], o.order_before)

    def test_to_xml(self):
        o = OptionFactory(order_before=None)
        el = o.to_xml()
        expected_el = ET.Element("option", {"cost": o.cost, "days": o.days})
        self.assertElementsEquals(el, expected_el)
