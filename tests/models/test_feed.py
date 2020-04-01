from unittest import mock

from tests.cases import ModelTestCase
from tests.factories import ShopFactory
from yandex_market_language import models


class FeedModelTestCase(ModelTestCase):
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
        self.assertElementsEquals(feed_el[0], shop.to_xml())
        self.assertEqual(feed_el.tag, "yml_catalog")
        self.assertEqual(feed_el.get("date"), feed._date)

    @mock.patch("yandex_market_language.models.Shop.from_xml")
    def test_from_xml(self, p):
        shop = ShopFactory()
        feed = models.Feed(shop)
        feed_el = feed.to_xml()
        p.return_value = shop
        parsed_feed = models.Feed.from_xml(feed_el)
        self.assertEqual(p.call_count, 1)
        self.assertEqual(feed.to_dict(), parsed_feed.to_dict())
