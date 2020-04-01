from tests.cases import ModelTestCase, ET
from tests.factories import AgeFactory
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError
from yandex_market_language.models import Age


class AgeModelTestCase(ModelTestCase):
    def test_to_dict(self):
        a = AgeFactory()
        d = a.to_dict()
        self.assertEqual(sorted(d.keys()), sorted(["unit", "value"]))
        self.assertEqual(d["unit"], a.unit)
        self.assertEqual(d["value"], a.value)

    def test_to_xml(self):
        a = AgeFactory()
        el = a.to_xml()
        expected_el = ET.Element("age", {"unit": a.unit})
        expected_el.text = a._value
        self.assertElementsEquals(el, expected_el)

    def test_unit_raises_validation_error(self):
        expected_err = (
            "unit must be a valid choice: {c}".format(
                c=", ".join(models.age.UNIT_CHOICES)
            )
        )
        with self.assertRaises(ValidationError) as e:
            AgeFactory(unit="err")
            self.assertEqual(str(e), expected_err)

    def test_value_wrong_type(self):
        with self.assertRaises(ValidationError) as e:
            AgeFactory(value="err")
            self.assertEqual(str(e), "value must be a valid int")

    def test_value_wrong_year_choice(self):
        expected_error = (
            "value for unit 'year' must be a valid choice: "
            "{c}".format(c=", ".join(str(c) for c in models.age.YEAR_CHOICES))
        )
        with self.assertRaises(ValidationError) as e:
            AgeFactory(unit="year", value=3)
            self.assertEqual(str(e), expected_error)

    def test_value_wrong_month_choice(self):
        expected_error = (
            "value for unit 'month' must be a valid choice: "
            "{c}".format(c=", ".join(str(c) for c in models.age.MONTH_CHOICES))
        )
        with self.assertRaises(ValidationError) as e:
            AgeFactory(unit="month", value=13)
            self.assertEqual(str(e), expected_error)

    def test_from_xml(self):
        a = AgeFactory()
        el = a.to_xml()
        parsed_a = Age.from_xml(el)
        self.assertEqual(a.to_dict(), parsed_a.to_dict())
