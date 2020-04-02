from datetime import datetime
from unittest import mock

from tests.cases import ModelTestCase, ET, fake
from tests.factories import (
    AbstractOfferFactory,
    SimplifiedOfferFactory,
    ArbitraryOfferFactory,
    AbstractBookOfferFactory,
    AudioBookOfferFactory,
    BookOfferFactory,
    MusicVideoOfferFactory,
    MedicineOfferFactory, EventTicketOfferFactory, AlcoholOfferFactory)
from yandex_market_language import models
from yandex_market_language.exceptions import ValidationError
from yandex_market_language.models.offers import (
    AbstractOffer,
    SimplifiedOffer,
    ArbitraryOffer,
    BookOffer,
    AbstractBookOffer,
    AudioBookOffer,
    MusicVideoOffer,
    MedicineOffer,
    EventTicketOffer, AlcoholOffer)


class BaseOfferModelTestCase(ModelTestCase):
    def test_cls_type(self):
        self.assertEqual(AbstractOffer.__TYPE__, None)

    def test_to_xml_offer_type(self):
        o = AbstractOfferFactory().create()
        o.__TYPE__ = "test"
        el = o.to_xml()
        self.assertEqual(el.attrib["type"], "test")

    def test_to_xml_available_attr(self):
        o = AbstractOfferFactory(available=False).create()
        el = o.create_xml()
        self.assertEqual(el.attrib["available"], "false")
        o.available = True
        el = o.create_xml()
        self.assertEqual(el.attrib["available"], "true")
        o.available = None
        el = o.create_xml()
        self.assertEqual(el.attrib.get("available"), None)

    def test_to_dict(self):
        o = AbstractOfferFactory().create()
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
            "supplier",
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
        o = AbstractOfferFactory().create()
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

        ET.SubElement(expected_el, "supplier", {"ogrn": o.supplier})

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
        o = AbstractOfferFactory().create()
        o.min_quantity = None
        self.assertEqual(o._min_quantity, "1")

    def test_expiry_property_dost_not_match_format_error(self):
        with self.assertRaises(ValidationError) as e:
            expiry = "err"
            AbstractOfferFactory(expiry=expiry).create()
            expected_err = "time data {d} does not match format '{f}'".format(
                d=expiry, f=models.offers.EXPIRY_FORMAT
            )
            self.assertEqual(str(e), expected_err)

    def test_expiry_property_datetime_to_str(self):
        dt = datetime.now()
        o = AbstractOfferFactory(expiry=dt).create()
        self.assertEqual(o._expiry, dt.strftime(models.offers.EXPIRY_FORMAT))

    def test_expiry_property_wrong_value_specified(self):
        with self.assertRaises(ValidationError) as e:
            AbstractOfferFactory(expiry=1).create()
            self.assertEqual(str(e), "expiry must be a valid datetime")

    def test_expiry_property_none(self):
        o = AbstractOfferFactory(expiry=None).create()
        self.assertEqual(o._expiry, None)
        self.assertEqual(o.expiry, None)

    def test_group_id_not_valid_maximum_length(self):
        with self.assertRaises(ValidationError) as e:
            group_id = fake.pyint(min_value=1000000000, max_value=9999999999)
            AbstractOfferFactory(group_id=group_id).create()
            self.assertEqual(
                str(e), "group_id must be an integer, maximum 9 characters."
            )

    @mock.patch("yandex_market_language.models.Age.from_xml")
    @mock.patch("yandex_market_language.models.Condition.from_xml")
    @mock.patch("yandex_market_language.models.Price.from_xml")
    @mock.patch("yandex_market_language.models.Dimensions.from_xml")
    @mock.patch("yandex_market_language.models.Parameter.from_xml")
    @mock.patch("yandex_market_language.models.Option.from_xml")
    @mock.patch.multiple(AbstractOffer, __abstractmethods__=set())
    def test_from_xml(
        self,
        option_p,
        parameter_p,
        dimensions_p,
        price_p,
        condition_p,
        age_p,
    ):
        o = AbstractOfferFactory().create()
        el = o.to_xml()
        options = o.delivery_options + o.pickup_options
        option_p.side_effect = options
        parameter_p.side_effect = o.parameters
        dimensions_p.return_value = o.dimensions
        price_p.return_value = o.price
        condition_p.return_value = o.condition
        age_p.return_value = o.age
        kwargs = AbstractOffer.from_xml(el)
        self.assertEqual(o.to_dict(), AbstractOffer(**kwargs).to_dict())
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
        expected_el = AbstractOfferFactory(**values).create().to_xml()

        name_el = ET.Element("name")
        name_el.text = name
        expected_el.insert(0, name_el)

        self.assertElementsEquals(el, expected_el)

    def from_xml(self):
        o = SimplifiedOfferFactory().create()
        el = o.to_xml()
        parsed_o = SimplifiedOffer.from_xml(el)
        self.assertEqual(o.to_dict(), parsed_o.to_dict())


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

        # Change offer type for AbstractOffer cls and create base element
        AbstractOfferFactory.__cls__.__TYPE__ = ArbitraryOffer.__TYPE__
        expected_el = AbstractOfferFactory(**values).create().to_xml()

        # Add model
        model_el = ET.SubElement(expected_el, "model")
        model_el.text = model

        # Add typePrefix
        type_prefix_el = ET.SubElement(expected_el, "typePrefix")
        type_prefix_el.text = type_prefix

        self.assertElementsEquals(el, expected_el)

    def from_xml(self):
        o = ArbitraryOfferFactory().create()
        el = o.to_xml()
        parsed_o = ArbitraryOffer.from_xml(el)
        self.assertEqual(o.to_dict(), parsed_o.to_dict())


class AbstractBookOfferTestCase(ModelTestCase):

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
    ]

    def test_to_dict(self):
        o = AbstractBookOfferFactory().create()
        d = o.to_dict()
        keys = d.keys()
        self.assertTrue(all(k in keys for k in self.KEYS))
        for k in self.KEYS:
            self.assertEqual(d[k], getattr(o, k))

    def test_to_xml(self):
        f = AbstractBookOfferFactory()
        o = f.create()
        el = o.to_xml()

        # Get arbitrary offer values
        values = f.get_values()
        book_offer_values = {}
        for k in self.KEYS:
            book_offer_values[k] = values.pop(k)

        # Change offer type for AbstractOffer cls and create base element
        expected_el = AbstractOfferFactory(**values).create().to_xml()

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
        ):
            el_ = ET.SubElement(expected_el, tag)
            el_.text = str(book_offer_values[attr])

        self.assertElementsEquals(el, expected_el)

    def from_xml(self):
        o = AbstractBookOfferFactory().create()
        el = o.to_xml()
        kwargs = AbstractBookOffer.from_xml(el)
        self.assertEqual(o.to_dict(), kwargs)


class BookOfferTestCase(ModelTestCase):
    def test_type(self):
        self.assertEqual(BookOffer.__TYPE__, "book")

    def test_to_dict(self):
        o = BookOfferFactory().create()
        d = o.to_dict()
        self.assertEqual(d["type"], o.__TYPE__)
        keys = ("binding", "page_extent")
        self.assertTrue(all(k in d for k in keys))
        for k in keys:
            self.assertEqual(d[k], getattr(o, k))

    def test_to_xml(self):
        f = BookOfferFactory()
        o = f.create()
        el = o.to_xml()

        # Get values and pop book values
        values = f.get_values()
        values.pop("binding")
        values.pop("page_extent")

        # Change __TYPE__ to "book"
        AbstractBookOfferFactory.__cls__.__TYPE__ = BookOffer.__TYPE__
        abstract_offer = AbstractBookOfferFactory(**values).create()

        # Create expected element manually
        expected_el = abstract_offer.to_xml()
        binding_el = ET.SubElement(expected_el, "binding")
        binding_el.text = o.binding
        page_extent_el = ET.SubElement(expected_el, "page_extent")
        page_extent_el.text = o._page_extent

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        o = BookOfferFactory().create()
        el = o.to_xml()
        parsed_o = BookOffer.from_xml(el)
        self.assertEqual(o.to_dict(), parsed_o.to_dict())

    def test_page_extent_raises_error(self):
        with self.assertRaises(ValidationError) as e:
            v = fake.pyint(min_value=-100, max_value=-1)
            BookOfferFactory(page_extent=v).create()
            self.assertEqual(str(e), "page_extent must be positive int")


class AudioBookOfferTestCase(ModelTestCase):
    MAPPING = {
        "performed_by": "performed_by",
        "performance_type": "performance_type",
        "storage": "storage",
        "audio_format": "format",
        "recording_length": "recording_length",
    }

    def test_type(self):
        self.assertEqual(AudioBookOffer.__TYPE__, "audiobook")

    def test_to_dict(self):
        o = AudioBookOfferFactory().create()
        d = o.to_dict()

        keys = self.MAPPING.keys()
        self.assertTrue(all(k in d for k in keys))
        for k in keys:
            self.assertEqual(d[k], getattr(o, k))

    def test_to_xml(self):
        f = AudioBookOfferFactory()
        o = f.create()
        el = o.to_xml()

        values = f.get_values()
        audio_book_values = {}
        for k in self.MAPPING.keys():
            audio_book_values[k] = values.pop(k)

        AbstractBookOfferFactory.__cls__.__TYPE__ = AudioBookOffer.__TYPE__
        expected_el = AbstractBookOfferFactory(**values).create().to_xml()

        for k, tag in self.MAPPING.items():
            el_ = ET.SubElement(expected_el, tag)
            el_.text = audio_book_values[k]

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        o = AudioBookOfferFactory().create()
        parsed_o = AudioBookOffer.from_xml(o.to_xml())
        self.assertEqual(o.to_dict(), parsed_o.to_dict())


class MusicVideoOfferTestCase(ModelTestCase):
    KEYS = (
        "artist",
        "title",
        "year",
        "media",
        "starring",
        "director",
        "original_name",
        "country"
    )

    MAPPING = {
        "artist": "artist",
        "title": "title",
        "year": "year",
        "media": "media",
        "starring": "starring",
        "director": "director",
        "originalName": "original_name",
        "country": "country",
    }

    def test_type(self):
        self.assertEqual(MusicVideoOffer.__TYPE__, "artist.title")

    def test_to_dict(self):
        o = MusicVideoOfferFactory().create()
        d = o.to_dict()
        self.assertTrue(all(k in d for k in self.KEYS))
        for k in self.KEYS:
            self.assertEqual(d[k], getattr(o, k))

    def test_from_xml(self):
        o = MusicVideoOfferFactory().create()
        parsed_o = MusicVideoOffer.from_xml(o.to_xml())
        self.assertEqual(o.to_dict(), parsed_o.to_dict())


class MedicineOfferTestCase(ModelTestCase):
    def test_type(self):
        self.assertEqual(MedicineOffer.__TYPE__, "medicine")

    def test_to_dict(self):
        o = MedicineOfferFactory().create()
        d = o.to_dict()
        self.assertTrue("name" in d)
        self.assertEqual(d["name"], o.name)


class EventTicketOfferTestCase(ModelTestCase):
    def test_type(self):
        self.assertEqual(EventTicketOffer.__TYPE__, "event-ticket")

    def test_to_dict(self):
        o = EventTicketOfferFactory().create()
        d = o.to_dict()
        keys = (
            "name",
            "place",
            "date",
            "hall",
            "hall_part",
            "is_premiere",
            "is_kids",
        )
        self.assertTrue(all(k in d for k in keys))
        for k in keys:
            self.assertEqual(d[k], getattr(o, k))


class AlcoholOfferTestCase(ModelTestCase):
    def test_type(self):
        self.assertEqual(AlcoholOffer.__TYPE__, "alco")

    def test_to_dict(self):
        o = AlcoholOfferFactory().create()
        d = o.to_dict()
        self.assertTrue(all(k in d for k in ("name",)))
        self.assertEqual(d["name"], o.name)
