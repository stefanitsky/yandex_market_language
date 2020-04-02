from datetime import datetime
from unittest import mock
from tests.cases import ModelTestCase, ET, fake
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError


@mock.patch.multiple(models.AbstractModel, __abstractmethods__=set())
class AbstractModelTestCase(ModelTestCase):
    @mock.patch("yandex_market_language.models.AbstractModel.create_xml")
    def test_to_xml_with_parent(self, p):
        parent_el = mock.MagicMock()
        parent_el.append = mock.MagicMock()
        p.return_value = ET.Element("test")
        base = models.AbstractModel()
        base.to_xml(parent_el)
        self.assertEqual(p.call_count, 1)
        self.assertEqual(parent_el.append.call_count, 1)

    @mock.patch("yandex_market_language.models.AbstractModel.create_dict")
    def test_clean_dict(self, p):
        d = {"a": 1, "b": 2, "c": None}
        p.return_value = d
        m = models.AbstractModel()
        cd = m.to_dict(clean=True)
        self.assertEqual(p.call_count, 1)
        self.assertEqual(cd, {"a": 1, "b": 2})

    def test_is_valid_int_returns_converted_int(self):
        v = fake.pyint()
        r = models.AbstractModel._is_valid_int(v, "test")
        self.assertEqual(r, str(v))

    def test_is_valid_int_returns_none(self):
        r = models.AbstractModel._is_valid_int(None, "test", True)
        self.assertEqual(r, None)

    def test_is_valid_int_returns_not_converted_int(self):
        v = fake.pyint()
        r = models.AbstractModel._is_valid_int(v, "test", convert_to_str=False)
        self.assertEqual(v, r)

    def test_is_valid_int_raises_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            models.AbstractModel._is_valid_int(None, "test")
            self.assertEqual(str(e), "test must be a valid int")

    def test_is_valid_float_returns_converted_float(self):
        v = fake.pyfloat()
        r = models.AbstractModel._is_valid_float(v, "test")
        self.assertEqual(r, str(v))

    def test_is_valid_float_returns_none(self):
        r = models.AbstractModel._is_valid_float(None, "test", True)
        self.assertEqual(r, None)

    def test_is_valid_float_returns_not_converted_float(self):
        v = fake.pyfloat()
        r = models.AbstractModel._is_valid_float(
            v, "test", convert_to_str=False
        )
        self.assertEqual(v, r)

    def test_is_valid_float_raises_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            models.AbstractModel._is_valid_float(None, "test")
            self.assertEqual(str(e), "test must be a valid float")

    def test_is_valid_bool(self):
        m = models.AbstractModel._is_valid_bool
        self.assertEqual(m(True, "test"), "true")
        self.assertEqual(m(False, "test"), "false")
        self.assertEqual(m("true", "test"), "true")
        self.assertEqual(m("false", "test"), "false")
        self.assertEqual(m(None, "test", True), None)
        with self.assertRaises(ValidationError) as e:
            v, a = None, "test"
            m(v, a)
            expected_msg = (
                "The {attr} parameter should be boolean. "
                "Got {t} instead.".format(attr=a, t=type(v))
            )
            self.assertEqual(str(e), expected_msg)

    def test_str_to_bool(self):
        m = models.AbstractModel._str_to_bool
        self.assertEqual(m("true"), True)
        self.assertEqual(m("false"), False)
        self.assertEqual(m("none"), None)

    def test_is_valid_datetime(self):
        dt_format = "%Y-%m-%d %H:%M"
        m = models.AbstractModel._is_valid_datetime
        dt = datetime.now()
        str_dt = dt.strftime(dt_format)
        self.assertEqual(m(dt, dt_format, "test"), dt.strftime(dt_format))
        self.assertEqual(m(str_dt, dt_format, "test"), str_dt)
        self.assertEqual(m(None, dt_format, "test", allow_none=True), None)
        with self.assertRaises(ValidationError) as e:
            m(None, dt_format, "test")
            self.assertEqual(str(e), "test must be a valid datetime")
