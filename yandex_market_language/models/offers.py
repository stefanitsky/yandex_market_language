from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import warnings

from yandex_market_language.exceptions import ValidationError

from .abstract import AbstractModel, XMLElement, XMLSubElement
from .price import Price
from .option import Option
from .parameter import Parameter
from .condition import Condition
from .dimensions import Dimensions
from .age import Age
from . import fields


EXPIRY_FORMAT = "YYYY-MM-DDThh:mm"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class AbstractOffer(
    fields.EnableAutoDiscountField,
    fields.DeliveryOptionsField,
    fields.PickupOptionsField,
    AbstractModel,
    ABC
):
    """
    Abstract offer model for all other offer models.
    """

    __TYPE__ = None

    def __init__(
        self,
        offer_id,
        url,
        price: Price,
        currency: str,
        category_id,
        vendor=None,
        vendor_code=None,
        bid=None,
        cbid=None,
        old_price=None,
        enable_auto_discounts=None,
        pictures: List[str] = None,
        supplier=None,
        delivery=True,
        pickup=True,
        delivery_options: List[Option] = None,
        pickup_options: List[Option] = None,
        store=None,
        description: str = None,
        sales_notes: str = None,
        min_quantity=1,
        manufacturer_warranty=None,
        country_of_origin=None,
        adult=None,
        barcodes: List[str] = None,
        parameters: List[Parameter] = None,
        condition: Condition = None,
        credit_template_id: str = None,
        expiry=None,
        weight=None,
        dimensions: Dimensions = None,
        downloadable=None,
        available=None,
        age: Age = None,
        group_id=None,
    ):
        self.vendor = vendor
        self.vendor_code = vendor_code
        self.offer_id = offer_id
        self.bid = bid
        self.cbid = cbid
        self.url = url
        self.price = price
        self.old_price = old_price
        self.enable_auto_discounts = enable_auto_discounts
        self.currency = currency
        self.category_id = category_id
        self.pictures = pictures
        self.supplier = supplier
        self.delivery = delivery
        self.pickup = pickup
        self.delivery_options = delivery_options
        self.pickup_options = pickup_options
        self.store = store
        self.description = description
        self.sales_notes = sales_notes
        self.min_quantity = min_quantity
        self.manufacturer_warranty = manufacturer_warranty
        self.country_of_origin = country_of_origin
        self.adult = adult
        self.barcodes = barcodes
        self.parameters = parameters
        self.condition = condition
        self.credit_template_id = credit_template_id
        self.expiry = expiry
        self.weight = weight
        self.dimensions = dimensions
        self.downloadable = downloadable
        self.available = available
        self.age = age
        self.group_id = group_id

    @property
    def cbid(self):
        return self._cbid

    @cbid.setter
    def cbid(self, value):
        if value:
            warnings.warn(
                "The attribute cbid is deprecated. "
                "Use the attribute bid instead.",
                DeprecationWarning
            )
        self._cbid = value

    @property
    def delivery(self) -> bool:
        return True if self._delivery == "true" else False

    @delivery.setter
    def delivery(self, value):
        if value is None:
            value = True
        self._delivery = self._is_valid_bool(value, "delivery")

    @property
    def pickup(self) -> bool:
        return True if self._delivery == "true" else False

    @pickup.setter
    def pickup(self, value):
        if value is None:  # sets default True value for pickup
            value = True
        self._pickup = self._is_valid_bool(value, "pickup")

    @property
    def store(self) -> Optional[bool]:
        return self._str_to_bool(self._store)

    @store.setter
    def store(self, value):
        self._store = self._is_valid_bool(value, "store", True)

    @property
    def min_quantity(self) -> int:
        return int(self._min_quantity)

    @min_quantity.setter
    def min_quantity(self, value):
        if value is None:  # sets default value for min_quantity
            self._min_quantity = "1"
        else:
            self._min_quantity = self._is_valid_int(value, "min_quantity")

    @property
    def manufacturer_warranty(self) -> Optional[bool]:
        return self._str_to_bool(self._manufacturer_warranty)

    @manufacturer_warranty.setter
    def manufacturer_warranty(self, value):
        self._manufacturer_warranty = self._is_valid_bool(
            value, "manufacturer_warranty", True
        )

    @property
    def adult(self) -> Optional[bool]:
        return self._str_to_bool(self._adult)

    @adult.setter
    def adult(self, value):
        self._adult = self._is_valid_bool(value, "adult", True)

    @property
    def parameters(self) -> List[Parameter]:
        return self._parameters or []

    @parameters.setter
    def parameters(self, params):
        self._parameters = params or []

    @property
    def expiry(self) -> Optional[datetime]:
        if self._expiry:
            return datetime.strptime(self._expiry, EXPIRY_FORMAT)
        else:
            return None

    @expiry.setter
    def expiry(self, dt):
        self._expiry = self._is_valid_datetime(
            dt, EXPIRY_FORMAT, "expiry", True
        )

    @property
    def weight(self) -> Optional[float]:
        return float(self._weight) if self._weight else None

    @weight.setter
    def weight(self, value):
        self._weight = self._is_valid_float(value, "weight", True)

    @property
    def downloadable(self) -> Optional[bool]:
        return self._str_to_bool(self._downloadable)

    @downloadable.setter
    def downloadable(self, value):
        self._downloadable = self._is_valid_bool(value, "downloadable", True)

    @property
    def available(self) -> Optional[bool]:
        return self._str_to_bool(self._available)

    @available.setter
    def available(self, value):
        self._available = self._is_valid_bool(value, "available", True)

    @property
    def group_id(self) -> Optional[int]:
        return int(self._group_id) if self._group_id else None

    @group_id.setter
    def group_id(self, value):
        value = self._is_valid_int(value, "group_id", True)

        # Validate group id and raise an error if it's not valid
        if len(str(value)) > 9:
            raise ValidationError(
                "group_id must be an integer, maximum 9 characters."
            )

        self._group_id = str(value) if value else None

    @abstractmethod
    def create_dict(self, **kwargs) -> dict:
        return dict(
            type=self.__TYPE__,
            vendor=self.vendor,
            vendor_code=self.vendor_code,
            offer_id=self.offer_id,
            bid=self.bid,
            url=self.url,
            price=self.price.to_dict(),
            old_price=self.old_price,
            enable_auto_discounts=self.enable_auto_discounts,
            currency=self.currency,
            category_id=self.category_id,
            pictures=self.pictures,
            supplier=self.supplier,
            delivery=self.delivery,
            pickup=self.pickup,
            delivery_options=[o.to_dict() for o in self.delivery_options],
            pickup_options=[o.to_dict() for o in self.pickup_options],
            store=self.store,
            description=self.description,
            sales_notes=self.sales_notes,
            min_quantity=self.min_quantity,
            manufacturer_warranty=self.manufacturer_warranty,
            country_of_origin=self.country_of_origin,
            adult=self.adult,
            barcodes=self.barcodes,
            parameters=[p.to_dict() for p in self.parameters],
            condition=self.condition.to_dict() if self.condition else None,
            credit_template_id=self.credit_template_id,
            expiry=self.expiry,
            weight=self.weight,
            dimensions=self.dimensions.to_dict() if self.dimensions else None,
            downloadable=self.downloadable,
            available=self.available,
            age=self.age.to_dict() if self.age else None,
            group_id=self.group_id,
            **kwargs
        )

    @abstractmethod
    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = XMLElement("offer", {"id": self.offer_id})

        # Add offer type
        if self.__TYPE__:
            offer_el.attrib["type"] = self.__TYPE__

        # Add offer bid attribute
        if self.bid:
            offer_el.attrib["bid"] = self.bid

        # Add offer cbid attribute (deprecated)
        if self.cbid:
            offer_el.attrib["cbid"] = self.cbid

        # Add offer available attribute
        if self.available is not None:
            offer_el.attrib["available"] = self._available

        # Add simple values
        for tag, attr in {
            "vendor": "vendor",
            "vendorCode": "vendor_code",
            "url": "url",
            "oldprice": "old_price",
            "enable_auto_discounts": "_enable_auto_discounts",
            "currencyId": "currency",
            "categoryId": "category_id",
            "delivery": "_delivery",
            "pickup": "_pickup",
            "store": "_store",
            "description": "description",
            "sales_notes": "sales_notes",
            "min-quantity": "_min_quantity",
            "manufacturer_warranty": "_manufacturer_warranty",
            "country_of_origin": "country_of_origin",
            "adult": "_adult",
            "expiry": "_expiry",
            "weight": "_weight",
            "downloadable": "_downloadable",
            "group_id": "_group_id",
            **kwargs,
        }.items():
            value = getattr(self, attr)
            if value:
                el = XMLSubElement(offer_el, tag)
                el.text = value

        # Add price
        self.price.to_xml(offer_el)

        # Add pictures
        if self.pictures:
            for url in self.pictures:
                picture_el = XMLSubElement(offer_el, "picture")
                picture_el.text = url

        # Add supplier
        if self.supplier:
            XMLSubElement(offer_el, "supplier", {"ogrn": self.supplier})

        # Add delivery options
        if self.delivery_options:
            delivery_options_el = XMLSubElement(offer_el, "delivery-options")
            for o in self.delivery_options:
                o.to_xml(delivery_options_el)

        # Add pickup options
        if self.pickup_options:
            pickup_options_el = XMLSubElement(offer_el, "pickup-options")
            for o in self.pickup_options:
                o.to_xml(pickup_options_el)

        # Add barcodes
        if self.barcodes:
            for b in self.barcodes:
                b_el = XMLSubElement(offer_el, "barcode")
                b_el.text = b

        # Add parameters
        if self.parameters:
            for p in self.parameters:
                p.to_xml(offer_el)

        # Add condition
        if self.condition:
            self.condition.to_xml(offer_el)

        # Add credit template
        if self.credit_template_id:
            XMLSubElement(
                offer_el, "credit-template", {"id": self.credit_template_id}
            )

        # Add dimensions
        if self.dimensions:
            self.dimensions.to_xml(offer_el)

        # Add age
        if self.age:
            self.age.to_xml(offer_el)

        return offer_el

    @staticmethod
    @abstractmethod
    def from_xml(offer_el: XMLElement, **mapping) -> dict:
        """
        Abstract method for parsing the xml element into a dictionary.
        """
        kwargs = {}
        mapping = {
            "vendorCode": "vendor_code",
            "oldprice": "old_price",
            "currencyId": "currency",
            "categoryId": "category_id",
            "min-quantity": "min_quantity",
            **mapping
        }

        pictures = []
        barcodes = []
        parameters = []

        for el in offer_el:
            if el.tag == "picture":
                pictures.append(el.text)
            elif el.tag == "delivery-options":
                delivery_options = []
                for option_el in el:
                    delivery_options.append(Option.from_xml(option_el))
                kwargs["delivery_options"] = delivery_options
            elif el.tag == "pickup-options":
                pickup_options = []
                for option_el in el:
                    pickup_options.append(Option.from_xml(option_el))
                kwargs["pickup_options"] = pickup_options
            elif el.tag == "barcode":
                barcodes.append(el.text)
            elif el.tag == "param":
                parameters.append(Parameter.from_xml(el))
            elif el.tag == "credit-template":
                kwargs["credit_template_id"] = el.attrib["id"]
            elif el.tag == "dimensions":
                kwargs["dimensions"] = Dimensions.from_xml(el)
            elif el.tag == "price":
                kwargs["price"] = Price.from_xml(el)
            elif el.tag == "condition":
                kwargs["condition"] = Condition.from_xml(el)
            elif el.tag == "age":
                kwargs["age"] = Age.from_xml(el)
            elif el.tag == "supplier":
                kwargs["supplier"] = el.attrib["ogrn"]
            else:
                k = mapping.get(el.tag, el.tag)
                kwargs[k] = el.text

        if pictures:
            kwargs["pictures"] = pictures
        if barcodes:
            kwargs["barcodes"] = barcodes
        if parameters:
            kwargs["parameters"] = parameters

        kwargs["offer_id"] = offer_el.attrib["id"]
        kwargs["bid"] = offer_el.attrib.get("bid")
        kwargs["cbid"] = offer_el.attrib.get("cbid")
        kwargs["available"] = offer_el.attrib.get("available")

        return kwargs


class SimplifiedOffer(AbstractOffer):
    """
    Simplified offer.
    In a simplified type, the manufacturer, type and name of the goods
    are indicated in one element - name.

    Yandex.Market docs:
    https://yandex.ru/support/partnermarket/offers.html
    """

    __TYPE__ = None

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(name=self.name)

    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = super().create_xml()
        name_el = XMLElement("name")
        name_el.text = self.name
        offer_el.insert(0, name_el)
        return offer_el

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "SimplifiedOffer":
        kwargs = AbstractOffer.from_xml(offer_el, **mapping)
        return SimplifiedOffer(**kwargs)


class ArbitraryOffer(AbstractOffer):
    """
    Arbitrary offer.
    In an arbitrary type, the manufacturer, type and name of the product
    must be indicated in separate elements - model, vendor & typePrefix.

    Yandex.Market docs:
    https://yandex.ru/support/partnermarket/export/vendor-model.html
    """

    __TYPE__ = "vendor.model"

    def __init__(
        self,
        model: str,
        vendor: str,
        type_prefix: str = None,
        **kwargs
    ):
        super().__init__(vendor=vendor, **kwargs)
        self.model = model
        self.type_prefix = type_prefix

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(
            model=self.model,
            type_prefix=self.type_prefix
        )

    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = super().create_xml()

        # Add model element
        model_el = XMLSubElement(offer_el, "model")
        model_el.text = self.model

        # Add typePrefix element
        if self.type_prefix:
            type_prefix_el = XMLSubElement(offer_el, "typePrefix")
            type_prefix_el.text = self.type_prefix

        return offer_el

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "ArbitraryOffer":
        mapping.update({
            "typePrefix": "type_prefix",
        })
        kwargs = AbstractOffer.from_xml(offer_el, **mapping)
        return ArbitraryOffer(**kwargs)


class AbstractBookOffer(fields.YearField, AbstractOffer, ABC):
    """
    Abstract book offer for book & audio book offer types.
    """

    def __init__(
        self,
        name: str,
        publisher: str,
        age: Age,
        isbn: str = None,
        author: str = None,
        series: str = None,
        year=None,
        volume=None,
        part=None,
        language: str = None,
        table_of_contents=None,
        **kwargs
    ):
        super().__init__(age=age, **kwargs)
        self.name = name
        self.publisher = publisher
        self.isbn = isbn
        self.author = author
        self.series = series
        self.year = year
        self.volume = volume
        self.part = part
        self.language = language
        self.table_of_contents = table_of_contents

    @property
    def volume(self) -> Optional[int]:
        return int(self._volume) if self._volume else None

    @volume.setter
    def volume(self, value):
        self._volume = self._is_valid_int(value, "volume", True)

    @property
    def part(self) -> Optional[int]:
        return int(self._part) if self._part else None

    @part.setter
    def part(self, value):
        self._part = self._is_valid_int(value, "part", True)

    @abstractmethod
    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(
            name=self.name,
            publisher=self.publisher,
            isbn=self.isbn,
            author=self.author,
            series=self.series,
            year=self.year,
            volume=self.volume,
            part=self.part,
            language=self.language,
            table_of_contents=self.table_of_contents,
            **kwargs
        )

    @abstractmethod
    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = super().create_xml(
            name="name",
            publisher="publisher",
            ISBN="isbn",
            author="author",
            series="series",
            year="_year",
            volume="_volume",
            part="_part",
            language="language",
            table_of_contents="table_of_contents",
            **kwargs
        )

        return offer_el

    @staticmethod
    @abstractmethod
    def from_xml(offer_el: XMLElement, **mapping) -> dict:
        mapping.update({
            "publisher": "publisher",
            "ISBN": "isbn",
        })
        return AbstractOffer.from_xml(offer_el, **mapping)


class BookOffer(AbstractBookOffer):
    """
    Special offer type for books.

    Yandex.Market docs:
    https://yandex.ru/support/partnermarket/export/books.html
    """

    __TYPE__ = "book"

    def __init__(self, binding=None, page_extent=None, **kwargs):
        super().__init__(**kwargs)
        self.binding = binding
        self.page_extent = page_extent

    @property
    def page_extent(self) -> Optional[int]:
        return int(self._page_extent) if self._page_extent else None

    @page_extent.setter
    def page_extent(self, value):
        value = self._is_valid_int(value, "page_extent", True, False)
        if value <= 0:
            raise ValidationError("page_extent must be positive int")
        self._page_extent = str(value)

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(
            binding=self.binding, page_extent=self.page_extent
        )

    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = super().create_xml(
            binding="binding",
            page_extent="_page_extent"
        )
        return offer_el

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "BookOffer":
        kwargs = AbstractBookOffer.from_xml(offer_el, **mapping)
        return BookOffer(**kwargs)


class AudioBookOffer(AbstractBookOffer):
    """
    Audio book offer.

    Docs:
    https://yandex.ru/support/partnermarket/export/audiobooks.html
    """

    __TYPE__ = "audiobook"

    def __init__(
        self,
        performed_by: str = None,
        performance_type: str = None,
        storage: str = None,
        audio_format: str = None,
        recording_length: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.performed_by = performed_by
        self.performance_type = performance_type
        self.storage = storage
        self.audio_format = audio_format
        self.recording_length = recording_length

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(
            performed_by=self.performed_by,
            performance_type=self.performance_type,
            storage=self.storage,
            audio_format=self.audio_format,
            recording_length=self.recording_length
        )

    def create_xml(self, **kwargs) -> XMLElement:
        return super().create_xml(
            performed_by="performed_by",
            performance_type="performance_type",
            storage="storage",
            format="audio_format",
            recording_length="recording_length"
        )

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "AudioBookOffer":
        mapping.update({"format": "audio_format"})
        kwargs = AbstractBookOffer.from_xml(offer_el, **mapping)
        return AudioBookOffer(**kwargs)


class MusicVideoOffer(fields.YearField, AbstractOffer):
    """
    Music or video offer.

    Docs:
    https://yandex.ru/support/partnermarket/export/music-video.html
    """

    __TYPE__ = "artist.title"

    def __init__(
        self,
        title: str,
        artist: str = None,
        year=None,
        media: str = None,
        starring: str = None,
        director: str = None,
        original_name: str = None,
        country: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.artist = artist
        self.title = title
        self.year = year
        self.media = media
        self.starring = starring
        self.director = director
        self.original_name = original_name
        self.country = country

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(
            artist=self.artist,
            title=self.title,
            year=self.year,
            media=self.media,
            starring=self.starring,
            director=self.director,
            original_name=self.original_name,
            country=self.country,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        return super().create_xml(
            artist="artist",
            title="title",
            year="_year",
            media="media",
            starring="starring",
            director="director",
            originalName="original_name",
            country="country",
        )

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "MusicVideoOffer":
        mapping.update({
            "originalName": "original_name"
        })
        kwargs = AbstractOffer.from_xml(offer_el, **mapping)
        return MusicVideoOffer(**kwargs)


class MedicineOffer(AbstractOffer):
    """
    Medicine offer.

    Docs:
    https://yandex.ru/support/partnermarket/export/medicine.html
    """

    __TYPE__ = "medicine"

    def __init__(self, name, delivery, pickup, **kwargs):
        super().__init__(delivery=delivery, pickup=pickup, **kwargs)
        self.name = name

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(name=self.name)

    def create_xml(self, **kwargs) -> XMLElement:
        return super().create_xml(name="name")

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "MedicineOffer":
        kwargs = AbstractOffer.from_xml(offer_el)
        return MedicineOffer(**kwargs)


class EventTicketOffer(AbstractOffer):
    """
    EventTicket offer.

    Docs:
    https://yandex.ru/support/partnermarket/export/event-tickets.html
    """

    __TYPE__ = "event-ticket"

    def __init__(
        self,
        name: str,
        place: str,
        date,
        hall: str = None,
        hall_part: str = None,
        is_premiere=None,
        is_kids=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.place = place
        self.hall = hall
        self.hall_part = hall_part
        self.date = date
        self.is_premiere = is_premiere
        self.is_kids = is_kids

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, DATE_FORMAT)

    @date.setter
    def date(self, dt):
        self._date = self._is_valid_datetime(dt, DATE_FORMAT, "date")

    @property
    def is_premiere(self) -> Optional[bool]:
        return self._str_to_bool(self._is_premiere)

    @is_premiere.setter
    def is_premiere(self, value):
        self._is_premiere = self._is_valid_bool(value, "is_premiere", True)

    @property
    def is_kids(self) -> Optional[bool]:
        return self._str_to_bool(self._is_kids)

    @is_kids.setter
    def is_kids(self, value):
        self._is_kids = self._is_valid_bool(value, "is_kids", True)

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(
            name=self.name,
            place=self.place,
            hall=self.hall,
            hall_part=self.hall_part,
            date=self.date,
            is_premiere=self.is_premiere,
            is_kids=self.is_kids,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        return super().create_xml(
            name="name",
            place="place",
            hall="hall",
            hall_part="hall_part",
            date="_date",
            is_premiere="_is_premiere",
            is_kids="_is_kids",
        )

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "EventTicketOffer":
        kwargs = AbstractOffer.from_xml(offer_el)
        return EventTicketOffer(**kwargs)


class AlcoholOffer(AbstractOffer):
    """
    Alcohol offer.

    Docs:
    https://yandex.ru/support/partnermarket/export/alcohol.html
    """

    __TYPE__ = "alco"

    def __init__(
        self,
        name: str,
        vendor: str,
        barcodes: List[str],
        parameters: List[Parameter],
        **kwargs
    ):
        super().__init__(
            vendor=vendor,
            barcodes=barcodes,
            parameters=parameters,
            **kwargs
        )
        self.name = name

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(name=self.name)

    def create_xml(self, **kwargs) -> XMLElement:
        return super().create_xml(name="name")

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "AlcoholOffer":
        kwargs = AbstractOffer.from_xml(offer_el)
        return AlcoholOffer(**kwargs)
