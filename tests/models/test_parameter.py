from tests.cases import ModelTestCase, ET
from tests.factories import ParameterFactory
from yandex_market_language.exceptions import ValidationError
from yandex_market_language.models import Parameter


class ParameterModelTestCase(ModelTestCase):
    def test_to_dict(self):
        name, value, unit = "Size", "33", "M"
        p = ParameterFactory(name, value, unit)
        d = p.to_dict()
        self.assertEqual(d["name"], name)
        self.assertEqual(d["value"], value)
        self.assertEqual(d["unit"], unit)

    def test_to_xml(self):
        name, value, unit = "Size", "33", "M"
        p = ParameterFactory(name, value, unit)
        el = p.to_xml()
        expected_el = ET.Element("param", {"name": name, "unit": unit})
        expected_el.text = value
        self.assertElementsEquals(el, expected_el)

    def test_value_property(self):
        p = ParameterFactory()
        with self.assertRaises(ValidationError) as e:

            class Err:
                def __str__(self):
                    return 1

            p.value = Err()

            self.assertEqual(str(e), "value must be a string")

    def test_from_xml(self):
        p = ParameterFactory()
        el = p.to_xml()
        parsed_p = Parameter.from_xml(el)
        self.assertEqual(p.to_dict(), parsed_p.to_dict())
