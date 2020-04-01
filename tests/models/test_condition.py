from tests.cases import ModelTestCase, ET
from tests.factories import ConditionFactory
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError
from yandex_market_language.models import Condition


class ConditionModelTestCase(ModelTestCase):
    def test_to_dict(self):
        typ, reason = "used", "idk why"
        c = ConditionFactory(typ, reason)
        d = c.to_dict()
        self.assertEqual(d["condition_type"], typ)
        self.assertEqual(d["reason"], reason)

    def test_to_xml(self):
        c = ConditionFactory()
        el = c.to_xml()

        expected_el = ET.Element("condition", {"type": c.condition_type})
        reason_el = ET.SubElement(expected_el, "reason")
        reason_el.text = c.reason

        self.assertElementsEquals(el, expected_el)

    def test_condition_type_property_raises_validation_error(self):
        choices = models.condition.CONDITION_CHOICES
        expected_message = (
            "condition_type attribute must be a value from a list: "
            "{list}".format(list=", ".join(choices))
        )
        with self.assertRaises(ValidationError) as e:
            ConditionFactory(condition_type="err")
            self.assertEqual(str(e), expected_message)

    def test_from_xml(self):
        c = ConditionFactory()
        el = c.to_xml()
        parsed_c = Condition.from_xml(el)
        self.assertEqual(c.to_dict(), parsed_c.to_dict())
