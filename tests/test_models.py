from unittest import mock

from faker import Faker
from unittest import TestCase
from xml.etree import ElementTree as ET
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError

from .factories import ShopFactory, CurrencyFactory


fake = Faker()


class BaseModelTestCase(TestCase):
    def test_to_xml_with_parent(self):
        el = ET.Element("el")
        parent_el = mock.MagicMock()
        parent_el.append = mock.MagicMock()
        models.BaseModel._to_xml(el, parent_el)
        self.assertEqual(parent_el.append.call_count, 1)

    def test_clean_dict(self):
        d = {"a": 1, "b": 2, "c": None}
        cd = models.BaseModel._clean_dict(d)
        self.assertEqual(cd, {"a": 1, "b": 2})


class FeedModelTestCase(TestCase):
    def test_to_dict(self):
        shop = ShopFactory()
        feed = models.Feed(shop)
        feed_dict = feed.to_dict()
        self.assertEqual(sorted(list(feed_dict.keys())), ["date", "shop"])
        self.assertEqual(feed_dict["date"], feed.date)
        self.assertEqual(feed_dict["shop"], feed.shop.to_dict())

    def test_to_xml(self):
        shop = ShopFactory()
        feed = models.Feed(shop)
        feed_el = feed.to_xml()
        self.assertEqual(list(el.tag for el in feed_el), ["shop"])
        self.assertEqual(ET.tostring(feed_el[0]), ET.tostring(shop.to_xml()))
        self.assertEqual(feed_el.tag, "yml_catalog")
        self.assertEqual(feed_el.get("date"), feed.date)


class ShopModelTestCase(TestCase):
    EXPECTED_KEYS = sorted(
        [
            "name",
            "company",
            "url",
            "platform",
            "version",
            "agency",
            "email",
            "currencies",
        ]
    )

    def test_to_dict(self):
        shop = ShopFactory()
        shop_dict = shop.to_dict()
        keys = sorted(list(shop_dict.keys()))
        self.assertEqual(keys, self.EXPECTED_KEYS)
        for k in self.EXPECTED_KEYS:
            if k in ("currencies",):
                continue
            else:
                self.assertEqual(shop_dict[k], getattr(shop, k))

    def test_to_xml(self):
        shop = ShopFactory()
        shop_el = shop.to_xml()
        keys = sorted(list(el.tag for el in shop_el))
        self.assertEqual(keys, self.EXPECTED_KEYS)
        for el in shop_el:
            if el.tag in ("currencies",):
                continue
            else:
                self.assertEqual(el.text, getattr(shop, el.tag))

    def test_url_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            ShopFactory(url=fake.pystr(513, 513))
            self.assertEqual(
                str(e), "The maximum url length is 512 characters."
            )


class CurrencyModelTestCase(TestCase):
    def test_to_dict(self):
        c = CurrencyFactory()
        d = c.to_dict()
        keys = sorted(list(d.keys()))
        expected_keys = sorted(["id", "rate", "plus"])
        self.assertEqual(keys, expected_keys)
        self.assertEqual(c.currency, d["id"])
        self.assertEqual(c.rate, d["rate"])
        self.assertEqual(c.plus, d["plus"])

    def test_to_xml(self):
        c = CurrencyFactory()
        el = c.to_xml()
        expected_xml = ET.Element("currency", c.to_dict())
        self.assertEqual(ET.tostring(el), ET.tostring(expected_xml))

    def test_to_xml_none_plus_attr(self):
        c = CurrencyFactory(plus=None)
        el = c.to_xml()
        expected_attribs = {"id": c.currency, "rate": c.rate}
        expected_xml = ET.Element("currency", expected_attribs)
        self.assertEqual(ET.tostring(el), ET.tostring(expected_xml))

    def test_currency_validation_error(self):
        msg = "Price data is accepted only in: (formatted_choices)".format(
            formatted_choices=", ".join(models.currency.CURRENCY_CHOICES)
        )
        with self.assertRaises(
            models.currency.CurrencyChoicesValidationError
        ) as e:
            CurrencyFactory(currency="UAN")
            self.assertEqual(str(e), msg)

        self.assertEqual(
            str(models.currency.CurrencyChoicesValidationError()), msg
        )

    def test_rate_validation_error(self):
        msg = (
            "The rate parameter can have the following values: "
            "number (int or float), (rate_choices)".format(
                rate_choices=', '.join(models.currency.RATE_CHOICES)
            )
        )
        with self.assertRaises(ValidationError) as e:
            CurrencyFactory(rate="err")
            self.assertEqual(str(e), msg)

        self.assertEqual(str(models.currency.RateValidationError()), msg)

    def test_plus_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            CurrencyFactory(plus="err")
            self.assertEqual(str(e), "The plus parameter only can be int.")
