from datetime import datetime
from unittest import mock

from tests.cases import ModelTestCase, ET, fake
from tests.factories import (
    BaseOfferFactory,
    SimplifiedOfferFactory,
    ArbitraryOfferFactory,
    BookOfferFactory,
)
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError
from yandex_market_language.models.offers import (
    BaseOffer,
    SimplifiedOffer,
    ArbitraryOffer,
    BookOffer,
)


class BaseOfferModelTestCase(ModelTestCase):
    def test_cls_type(self):
        self.assertEqual(BaseOffer.__TYPE__, None)

    def test_to_xml_offer_type(self):
        o = BaseOfferFactory().create()
        o.__TYPE__ = "test"
        el = o.to_xml()
        self.assertEqual(el.attrib["type"], "test")

    def test_to_xml_available_attr(self):
        o = BaseOfferFactory(available=False).create()
        el = o.create_xml()
        self.assertEqual(el.attrib["available"], "false")
        o.available = True
        el = o.create_xml()
        self.assertEqual(el.attrib["available"], "true")
        o.available = None
        el = o.create_xml()
        self.assertEqual(el.attrib.get("available"), None)

    def test_to_dict(self):
        o = BaseOfferFactory().create()
        d = o.to_dict()
        expected_keys = [
            "type",
            "vendor",
            "vendor_code",
            "offer_id",
            "bid",
            "url",
            "price",
            "old_price",
            "enable_auto_discounts",
            "currency",
            "category_id",
            "pictures",
            "delivery",
            "pickup",
            "delivery_options",
            "pickup_options",
            "store",
            "description",
            "sales_notes",
            "min_quantity",
            "manufacturer_warranty",
            "country_of_origin",
            "adult",
            "barcodes",
            "parameters",
            "condition",
            "credit_template_id",
            "expiry",
            "weight",
            "dimensions",
            "downloadable",
            "available",
            "age",
            "group_id",
        ]
        self.assertEqual(sorted(d.keys()), sorted(expected_keys))

    def test_to_xml(self):
        o = BaseOfferFactory().create()
        el = o.to_xml()

        attributes = {"id": o.offer_id, "bid": o.bid}
        if o._available is not None:
            attributes["available"] = o._available

        expected_el = ET.Element("offer", attributes)

        for tag, attr in (
            ("vendor", "vendor"),
            ("vendorCode", "vendor_code"),
            ("url", "url"),
            ("oldprice", "old_price"),
            ("enable_auto_discounts", "_enable_auto_discounts"),
            ("currencyId", "currency"),
            ("categoryId", "category_id"),
            ("delivery", "_delivery"),
            ("pickup", "_pickup"),
            ("store", "_store"),
            ("description", "description"),
            ("sales_notes", "sales_notes"),
            ("min-quantity", "_min_quantity"),
            ("manufacturer_warranty", "_manufacturer_warranty"),
            ("country_of_origin", "country_of_origin"),
            ("adult", "_adult"),
            ("expiry", "_expiry"),
            ("weight", "_weight"),
            ("downloadable", "_downloadable"),
            ("group_id", "_group_id"),
        ):
            v = getattr(o, attr)
            if v:
                el_ = ET.SubElement(expected_el, tag)
                el_.text = getattr(o, attr)

        # Add price
        o.price.to_xml(expected_el)

        # Add pictures
        for url in o.pictures:
            el_ = ET.SubElement(expected_el, "picture")
            el_.text = url

        # Add delivery options
        delivery_options_el = ET.SubElement(expected_el, "delivery-options")
        for _ in o.delivery_options:
            _.to_xml(delivery_options_el)

        # Add pickup options
        pickup_options_el = ET.SubElement(expected_el, "pickup-options")
        for _ in o.pickup_options:
            _.to_xml(pickup_options_el)

        # Add barcodes
        for barcode in o.barcodes:
            el_ = ET.SubElement(expected_el, "barcode")
            el_.text = barcode

        # Add parameters
        for _ in o.parameters:
            _.to_xml(expected_el)

        # Add condition
        o.condition.to_xml(expected_el)

        # Add credit template
        ET.SubElement(
            expected_el, "credit-template", {"id": o.credit_template_id}
        )

        # Add dimensions
        o.dimensions.to_xml(expected_el)

        # Add age
        o.age.to_xml(expected_el)

        if o._available is not None:
            self.assertEqual(el.attrib.get("available"), o._available)
        self.assertElementsEquals(el, expected_el)

    def test_min_quantity_property_default(self):
        o = BaseOfferFactory().create()
        o.min_quantity = None
        self.assertEqual(o._min_quantity, "1")

    def test_expiry_property_dost_not_match_format_error(self):
        with self.assertRaises(ValidationError) as e:
            expiry = "err"
            BaseOfferFactory(expiry=expiry).create()
            expected_err = "time data {d} does not match format '{f}'".format(
                d=expiry, f=models.offers.EXPIRY_FORMAT
            )
            self.assertEqual(str(e), expected_err)

    def test_expiry_property_datetime_to_str(self):
        dt = datetime.now()
        o = BaseOfferFactory(expiry=dt).create()
        self.assertEqual(o._expiry, dt.strftime(models.offers.EXPIRY_FORMAT))

    def test_expiry_property_wrong_value_specified(self):
        with self.assertRaises(ValidationError) as e:
            BaseOfferFactory(expiry=1).create()
            self.assertEqual(str(e), "expiry must be a valid datetime")

    def test_expiry_property_none(self):
        o = BaseOfferFactory(expiry=None).create()
        self.assertEqual(o._expiry, None)
        self.assertEqual(o.expiry, None)

    def test_group_id_not_valid_maximum_length(self):
        with self.assertRaises(ValidationError) as e:
            group_id = fake.pyint(min_value=1000000000, max_value=9999999999)
            BaseOfferFactory(group_id=group_id).create()
            self.assertEqual(
                str(e), "group_id must be an integer, maximum 9 characters."
            )

    @mock.patch("yandex_market_language.models.Age.from_xml")
    @mock.patch("yandex_market_language.models.Condition.from_xml")
    @mock.patch("yandex_market_language.models.Price.from_xml")
    @mock.patch("yandex_market_language.models.Dimensions.from_xml")
    @mock.patch("yandex_market_language.models.Parameter.from_xml")
    @mock.patch("yandex_market_language.models.Option.from_xml")
    @mock.patch.multiple(BaseOffer, __abstractmethods__=set())
    def test_from_xml(
        self,
        option_p,
        parameter_p,
        dimensions_p,
        price_p,
        condition_p,
        age_p,
    ):
        o = BaseOfferFactory().create()
        el = o.to_xml()
        options = o.delivery_options + o.pickup_options
        option_p.side_effect = options
        parameter_p.side_effect = o.parameters
        dimensions_p.return_value = o.dimensions
        price_p.return_value = o.price
        condition_p.return_value = o.condition
        age_p.return_value = o.age
        kwargs = BaseOffer.from_xml(el)
        self.assertEqual(o.to_dict(), BaseOffer(**kwargs).to_dict())
        self.assertEqual(option_p.call_count, len(options))
        self.assertEqual(parameter_p.call_count, len(o.parameters))
        self.assertEqual(dimensions_p.call_count, 1)
        self.assertEqual(price_p.call_count, 1)
        self.assertEqual(condition_p.call_count, 1)
        self.assertEqual(age_p.call_count, 1)


class SimplifiedOfferModelTestCase(ModelTestCase):
    def test_cls_type(self):
        self.assertEqual(SimplifiedOffer.__TYPE__, None)

    def test_to_dict(self):
        o = SimplifiedOfferFactory().create()
        d = o.to_dict()
        keys = d.keys()
        expected_keys = ["name"]
        self.assertTrue(all(k in keys for k in expected_keys))
        self.assertEqual(d["name"], o.name)

    def test_to_xml(self):
        f = SimplifiedOfferFactory()
        o = f.create()
        el = o.to_xml()

        values = f.get_values()
        name = values.pop("name")
        expected_el = BaseOfferFactory(**values).create().to_xml()

        name_el = ET.Element("name")
        name_el.text = name
        expected_el.insert(0, name_el)

        self.assertElementsEquals(el, expected_el)


class ArbitraryOfferTestCase(ModelTestCase):
    def test_cls_type(self):
        self.assertEqual(ArbitraryOffer.__TYPE__, "vendor.model")

    def test_to_dict(self):
        o = ArbitraryOfferFactory().create()
        d = o.to_dict()
        keys = d.keys()
        expected_keys = ["model", "vendor", "type_prefix"]
        self.assertTrue(all(k in keys for k in expected_keys))
        self.assertEqual(d["type"], o.__TYPE__)
        self.assertEqual(d["model"], o.model)
        self.assertEqual(d["vendor"], o.vendor)
        self.assertEqual(d["type_prefix"], o.type_prefix)

    def test_to_xml(self):
        f = ArbitraryOfferFactory()
        o = f.create()
        el = o.to_xml()

        # Get arbitrary offer values
        values = f.get_values()
        model = values.pop("model")
        type_prefix = values.pop("type_prefix")

        # Change offer type for BaseOffer cls and create base element
        BaseOfferFactory.__cls__.__TYPE__ = ArbitraryOffer.__TYPE__
        expected_el = BaseOfferFactory(**values).create().to_xml()

        # Add model
        model_el = ET.SubElement(expected_el, "model")
        model_el.text = model

        # Add typePrefix
        type_prefix_el = ET.SubElement(expected_el, "typePrefix")
        type_prefix_el.text = type_prefix

        self.assertElementsEquals(el, expected_el)


class BookOfferTestCase(ModelTestCase):

    KEYS = [
        "name",
        "publisher",
        "isbn",
        "author",
        "series",
        "year",
        "volume",
        "part",
        "language",
        "table_of_contents",
        "binding",
        "page_extent",
    ]

    def test_cls_type(self):
        self.assertEqual(BookOffer.__TYPE__, "book")

    def test_to_dict(self):
        o = BookOfferFactory().create()
        d = o.to_dict()
        keys = d.keys()
        self.assertTrue(all(k in keys for k in self.KEYS))
        self.assertEqual(d["type"], o.__TYPE__)
        for k in self.KEYS:
            self.assertEqual(d[k], getattr(o, k))

    def test_to_xml(self):
        f = BookOfferFactory()
        o = f.create()
        el = o.to_xml()

        # Get arbitrary offer values
        values = f.get_values()
        book_offer_values = {}
        for k in self.KEYS:
            book_offer_values[k] = values.pop(k)

        # Change offer type for BaseOffer cls and create base element
        BaseOfferFactory.__cls__.__TYPE__ = BookOffer.__TYPE__
        expected_el = BaseOfferFactory(**values).create().to_xml()

        for tag, attr in (
            ("name", "name"),
            ("publisher", "publisher"),
            ("ISBN", "isbn"),
            ("author", "author"),
            ("series", "series"),
            ("year", "year"),
            ("volume", "volume"),
            ("part", "part"),
            ("language", "language"),
            ("table_of_contents", "table_of_contents"),
            ("binding", "binding"),
            ("page_extent", "page_extent"),
        ):
            el_ = ET.SubElement(expected_el, tag)
            el_.text = str(book_offer_values[attr])

        self.assertElementsEquals(el, expected_el)

    def test_page_extent_raises_error(self):
        with self.assertRaises(ValidationError) as e:
            v = fake.pyint(min_value=-100, max_value=-1)
            BookOfferFactory(page_extent=v).create()
            self.assertEqual(str(e), "page_extent must be positive int")
