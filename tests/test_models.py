from unittest.mock import patch

from faker import Faker
from unittest import TestCase
from xml.etree import ElementTree as ET
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError

from .factories import ShopFactory, CurrencyFactory


fake = Faker()


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
        ]
    )

    def test_to_dict(self):
        shop = ShopFactory()
        shop_dict = shop.to_dict()
        keys = sorted(list(shop_dict.keys()))
        self.assertEqual(keys, self.EXPECTED_KEYS)
        for k in self.EXPECTED_KEYS:
            self.assertEqual(shop_dict[k], getattr(shop, k))

    def test_to_xml(self):
        shop = ShopFactory()
        shop_el = shop.to_xml()
        keys = sorted(list(el.tag for el in shop_el))
        self.assertEqual(keys, self.EXPECTED_KEYS)
        for el in shop_el:
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

    def test_currency_validation_error(self):
        msg = (
            "Price data is accepted only in: "
            f"{', '.join(models.currency.CURRENCY_CHOICES)}"
        )
        with self.assertRaises(
            models.currency.CurrencyChoicesValidationError
        ) as e:
            CurrencyFactory(currency="UAN")
            self.assertEqual(str(e), msg)

        self.assertEqual(
            str(models.currency.CurrencyChoicesValidationError()),
            msg
        )

    def test_rate_validation_error(self):
        msg = (
            "The rate parameter can have the following values: "
            f"number (int or float), {', '.join(models.currency.RATE_CHOICES)}"
        )
        with self.assertRaises(ValidationError) as e:
            CurrencyFactory(rate="err")
            self.assertEqual(str(e), msg)

    def test_plus_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            CurrencyFactory(plus="err")
            self.assertEqual(str(e), "The plus parameter only can be int.")

    @patch("yandex_market_language.models.currency.XMLSubElement")
    def test_to_xml_with_parent_el(self, p):
        c = CurrencyFactory()
        c.to_xml(ET.Element("test"))
        self.assertEqual(p.call_count, 1)
