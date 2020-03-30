from abc import ABC, abstractmethod
from typing import List, Optional

from yandex_market_language.exceptions import ValidationError

from .base import BaseModel, XMLElement, XMLSubElement
from .price import Price
from .option import Option
from . import fields


class BaseOffer(
    fields.EnableAutoDiscountField,
    fields.DeliveryOptionsField,
    fields.PickupOptionsField,
    BaseModel,
    ABC
):
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
        description: str = None,
        sales_notes: str = None,
        min_quantity=1,
        manufacturer_warranty=None,
        country_of_origin=None,
        adult=None,
        barcodes: List[str] = None,
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
        self.description = description
        self.sales_notes = sales_notes
        self.min_quantity = min_quantity
        self.manufacturer_warranty = manufacturer_warranty
        self.country_of_origin = country_of_origin
        self.adult = adult
        self.barcodes = barcodes

    @staticmethod
    def _value_to_bool(value, attr: str, allow_none: bool = False):
        if value in ["true", "false"]:
            return value
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif value is None and allow_none:
            return None
        else:
            raise ValidationError(
                "The {attr} parameter should be boolean. "
                "Got {t} instead.".format(attr=attr, t=type(value))
            )

    @property
    def delivery(self) -> bool:
        return True if self._delivery == "true" else False

    @delivery.setter
    def delivery(self, value):
        if value is None:
            value = True
        self._delivery = self._value_to_bool(value, "delivery")

    @property
    def pickup(self) -> bool:
        return True if self._delivery == "true" else False

    @pickup.setter
    def pickup(self, value):
        if value is None:
            value = True
        self._pickup = self._value_to_bool(value, "pickup")

    @property
    def min_quantity(self) -> int:
        return int(self._min_quantity)

    @min_quantity.setter
    def min_quantity(self, value):
        if value is None:
            self._min_quantity = "1"
        else:
            try:
                int(value)
                self._min_quantity = str(value)
            except (TypeError, ValueError):
                raise ValidationError("min_quantity must be a number")

    @property
    def manufacturer_warranty(self) -> Optional[bool]:
        return {"true": True, "false": False}.get(
            self._manufacturer_warranty, None
        )

    @manufacturer_warranty.setter
    def manufacturer_warranty(self, value):
        self._manufacturer_warranty = self._value_to_bool(
            value, "manufacturer_warranty", True
        )

    @property
    def adult(self) -> Optional[bool]:
        return {"true": True, "false": False}.get(
            self._adult, None
        )

    @adult.setter
    def adult(self, value):
        self._adult = self._value_to_bool(value, "adult", True)

    @abstractmethod
    def create_dict(self, **kwargs) -> dict:
        return dict(
            vendor=self.vendor,
            vendor_code=self.vendor_code,
            offer_id=self.offer_id,
            bid=self.bid,
            url=self.url,
            price=self.price,
            old_price=self.old_price,
            enable_auto_discounts=self.enable_auto_discounts,
            currency=self.currency,
            category_id=self.category_id,
            pictures=self.pictures,
            delivery=self.delivery,
            pickup=self.pickup,
            delivery_options=[o.to_dict() for o in self.delivery_options],
            pickup_options=[o.to_dict() for o in self.pickup_options],
            description=self.description,
            sales_notes=self.sales_notes,
            min_quantity=self.min_quantity,
            manufacturer_warranty=self.manufacturer_warranty,
            country_of_origin=self.country_of_origin,
            adult=self.adult,
            barcodes=self.barcodes,
            **kwargs
        )

    @abstractmethod
    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = XMLElement("offer", {"id": self.offer_id})

        # Add offer bid attribute
        if self.bid:
            offer_el.attrib["bid"] = self.bid

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
            ("description", "description"),
            ("sales_notes", "sales_notes"),
            ("min-quantity", "_min_quantity"),
            ("manufacturer_warranty", "_manufacturer_warranty"),
            ("country_of_origin", "country_of_origin"),
            ("adult", "_adult"),
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

        return offer_el


class SimplifiedOffer(BaseOffer):
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)

    def create_dict(self, **kwargs) -> dict:
        return super().create_dict(name=self.name)

    def create_xml(self, **kwargs) -> XMLElement:
        offer_el = super().create_xml()
        name_el = XMLElement("name")
        name_el.text = self.name
        offer_el.insert(0, name_el)
        return offer_el
