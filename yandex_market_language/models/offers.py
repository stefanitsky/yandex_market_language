from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from yandex_market_language.exceptions import ValidationError

from .base import BaseModel, XMLElement, XMLSubElement
from .price import Price
from .option import Option
from .parameter import Parameter
from .condition import Condition
from .dimensions import Dimensions
from .age import Age
from . import fields


EXPIRY_FORMAT = "YYYY-MM-DDThh:mm"


class BaseOffer(
    fields.EnableAutoDiscountField,
    fields.DeliveryOptionsField,
    fields.PickupOptionsField,
    BaseModel,
    ABC
):

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
        old_price=None,
        enable_auto_discounts=None,
        pictures: List[str] = None,
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
        self.url = url
        self.price = price
        self.old_price = old_price
        self.enable_auto_discounts = enable_auto_discounts
        self.currency = currency
        self.category_id = category_id
        self.pictures = pictures
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
        if value is None:
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
        if value is None:
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
        if isinstance(dt, datetime):
            self._expiry = dt.strftime(EXPIRY_FORMAT)
        elif isinstance(dt, str):
            try:
                datetime.strptime(dt, EXPIRY_FORMAT)
            except ValueError as e:
                raise ValidationError(e)
            self._expiry = dt
        elif dt is None:
            self._expiry = None
        else:
            raise ValidationError("expiry must be a valid datetime")

    @property
    def weight(self) -> Optional[float]:
        return float(self._weight)

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

        if len(str(value)) > 9:
            raise ValidationError(
                "group_id must be an integer, maximum 9 characters."
            )
        else:
            self._group_id = str(value)

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
            age=self.age,
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

        # Add offer available attribute
        if self.available is not None:
            offer_el.attrib["available"] = self._available

        # Add simple values
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
                kwargs["delivery_options"] = Option.from_xml(el)
            elif el.tag == "pickup-options":
                kwargs["pickup_options"] = Option.from_xml(el)
            elif el.tag == "barcode":
                barcodes.append(el.text)
            elif el.tag == "param":
                pass
            elif el.tag == "credit-template":
                kwargs["credit_template_id"] = el.attrib["id"]
            elif el.tag == "dimensions":
                kwargs["dimensions"] = Dimensions.from_xml(el)
            elif el.tag == "price":
                kwargs["price"] = Price.from_xml(el)
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

        return kwargs


class SimplifiedOffer(BaseOffer):
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
        kwargs = BaseOffer.from_xml(offer_el, **mapping)
        return SimplifiedOffer(**kwargs)


class ArbitraryOffer(BaseOffer):
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
        kwargs = BaseOffer.from_xml(offer_el, **mapping)
        return ArbitraryOffer(**kwargs)


class BookOffer(BaseOffer):
    """
    Special offer type for books.

    Yandex.Market docs:
    https://yandex.ru/support/partnermarket/export/books.html
    """

    __TYPE__ = "book"

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
        binding=None,
        page_extent=None,
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
        self.binding = binding
        self.page_extent = page_extent

    @property
    def year(self) -> Optional[int]:
        return int(self._year) if self._year else None

    @year.setter
    def year(self, value):
        self._year = self._is_valid_int(value, "year", True)

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
            binding=self.binding,
            page_extent=self.page_extent,
            **kwargs
        )

    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = super().create_xml(**kwargs)

        for tag, attr in (
            ("name", "name"),
            ("publisher", "publisher"),
            ("ISBN", "isbn"),
            ("author", "author"),
            ("series", "series"),
            ("year", "_year"),
            ("volume", "_volume"),
            ("part", "_part"),
            ("language", "language"),
            ("table_of_contents", "table_of_contents"),
            ("binding", "binding"),
            ("page_extent", "_page_extent"),
        ):
            v = getattr(self, attr)
            if v:
                el = XMLSubElement(offer_el, tag)
                el.text = v

        return offer_el

    @staticmethod
    def from_xml(offer_el: XMLElement, **mapping) -> "BookOffer":
        mapping.update({
            "publisher": "publisher",
            "ISBN": "isbn",
        })
        kwargs = BaseOffer.from_xml(offer_el, **mapping)
        return BookOffer(**kwargs)
