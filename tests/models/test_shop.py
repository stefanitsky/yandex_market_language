from unittest import mock

from tests.cases import ModelTestCase, fake
from tests import factories
from yandex_market_language import exceptions, models


class ShopModelTestCase(ModelTestCase):
    def test_to_dict(self):
        shop = factories.ShopFactory()
        shop_dict = shop.to_dict()
        keys = sorted(list(shop_dict.keys()))
        expected_keys = sorted([
            "name",
            "company",
            "url",
            "platform",
            "version",
            "agency",
            "email",
            "currencies",
            "categories",
            "delivery_options",
            "pickup_options",
            "enable_auto_discounts",
            "offers",
            "gifts",
            "promos",
        ])
        self.assertEqual(keys, expected_keys)
        for k in (
            "name",
            "company",
            "url",
            "platform",
            "version",
            "agency",
            "email",
            "enable_auto_discounts",
        ):
            self.assertEqual(shop_dict[k], getattr(shop, k))

    def test_to_xml(self):
        shop = factories.ShopFactory()
        shop_el = shop.to_xml()
        keys = sorted(list(el.tag for el in shop_el))
        expected_keys = sorted([
            "name",
            "company",
            "url",
            "platform",
            "version",
            "agency",
            "email",
            "currencies",
            "categories",
            "delivery-options",
            "pickup-options",
            "enable_auto_discounts",
            "offers",
            "gifts",
            "promos",
        ])
        self.assertEqual(keys, expected_keys)
        for el in shop_el:
            if el.tag in (
                "currencies",
                "categories",
                "delivery-options",
                "pickup-options",
                "offers",
                "gifts",
                "promos",
            ):
                continue
            elif el.tag == "enable_auto_discounts":
                self.assertEqual(el.text, shop._enable_auto_discounts)
            else:
                self.assertEqual(el.text, getattr(shop, el.tag))

    def test_url_validation_error(self):
        with self.assertRaises(exceptions.ValidationError) as e:
            factories.ShopFactory(url=fake.pystr(513, 513))
            self.assertEqual(
                str(e), "The maximum url length is 512 characters."
            )

    @mock.patch("yandex_market_language.models.Promo.from_xml")
    @mock.patch("yandex_market_language.models.Gift.from_xml")
    @mock.patch("yandex_market_language.models.BookOffer.from_xml")
    @mock.patch("yandex_market_language.models.ArbitraryOffer.from_xml")
    @mock.patch("yandex_market_language.models.SimplifiedOffer.from_xml")
    @mock.patch("yandex_market_language.models.Option.from_xml")
    @mock.patch("yandex_market_language.models.Category.from_xml")
    @mock.patch("yandex_market_language.models.Currency.from_xml")
    def test_from_xml(
        self,
        currency_p,
        category_p,
        option_p,
        simplified_from_xml_p,
        arbitrary_from_xml_p,
        book_from_xml_p,
        gift_from_xml_p,
        promo_from_xml_p,
    ):
        simplified_offers = [
            factories.SimplifiedOfferFactory().create() for _ in range(3)
        ]
        arbitrary_offers = [
            factories.ArbitraryOfferFactory().create() for _ in range(3)
        ]
        book_offers = [factories.BookOfferFactory().create() for _ in range(3)]
        offers = simplified_offers + arbitrary_offers + book_offers

        shop = factories.ShopFactory(offers=offers)
        shop_el = shop.to_xml()
        options = shop.delivery_options + shop.pickup_options

        currency_p.side_effect = shop.currencies
        category_p.side_effect = shop.categories
        option_p.side_effect = options
        simplified_from_xml_p.side_effect = simplified_offers
        arbitrary_from_xml_p.side_effect = arbitrary_offers
        book_from_xml_p.side_effect = book_offers
        gift_from_xml_p.side_effect = shop.gifts
        promo_from_xml_p.side_effect = shop.promos

        parsed_shop = models.Shop.from_xml(shop_el)
        self.assertEqual(shop.to_dict(), parsed_shop.to_dict())
        self.assertEqual(currency_p.call_count, len(shop.currencies))
        self.assertEqual(category_p.call_count, len(shop.categories))
        self.assertEqual(option_p.call_count, len(options))
        self.assertEqual(simplified_from_xml_p.call_count, 3)
        self.assertEqual(arbitrary_from_xml_p.call_count, 3)
        self.assertEqual(book_from_xml_p.call_count, 3)
        self.assertEqual(gift_from_xml_p.call_count, len(shop.gifts))
        self.assertEqual(promo_from_xml_p.call_count, len(shop.promos))

    def test_unexpected_offer_type_error(self):
        shop = factories.ShopFactory()
        shop_el = shop.to_xml()
        offer_type = "error"
        shop_el.find("offers")[0].attrib["type"] = offer_type
        with self.assertRaises(exceptions.ParseError) as e:
            models.Shop.from_xml(shop_el)
            self.assertEqual(
                str(e),
                "Got unexpected offer type: {0}".format(offer_type)
            )
