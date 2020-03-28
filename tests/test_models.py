from faker import Faker
from unittest import TestCase
from xml.etree import ElementTree as ET
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError

from .factories import ShopFactory


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
    def test_to_dict(self):
        shop = ShopFactory()
        shop_dict = shop.to_dict()
        expected_keys = [
            "name",
            "company",
            "url",
        ]
        self.assertEqual(list(shop_dict.keys()), expected_keys)

    def test_to_xml(self):
        shop = ShopFactory()
        shop_el = shop.to_xml()
        expected_tags = [
            "name",
            "company",
            "url"
        ]
        self.assertEqual(list(el.tag for el in shop_el), expected_tags)
        for el in shop_el:
            self.assertEqual(el.text, getattr(shop, el.tag))

    def test_url_validation_error(self):
        with self.assertRaises(ValidationError) as e:
            ShopFactory(url=fake.pystr(513, 513))
            self.assertEqual(
                str(e), "The maximum url length is 512 characters."
            )
