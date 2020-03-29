from abc import ABC, abstractmethod
from .base import BaseModel, XMLElement, XMLSubElement
from .price import Price
from .fields import EnableAutoDiscountField


class BaseOffer(BaseModel, EnableAutoDiscountField, ABC):
    def __init__(
        self,
        offer_id,
        url,
        price: Price,
        vendor=None,
        vendor_code=None,
        bid=None,
        old_price=None,
        enable_auto_discounts=None,
    ):
        self.vendor = vendor
        self.vendor_code = vendor_code
        self.offer_id = offer_id
        self.bid = bid
        self.url = url
        self.price = price
        self.old_price = old_price
        self.enable_auto_discounts = enable_auto_discounts

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
            ("url", "url"),
            ("oldprice", "old_price"),
            ("enable_auto_discounts", "_enable_auto_discounts"),
        ):
            value = getattr(self, attr)
            if value:
                el = XMLSubElement(offer_el, tag)
                el.text = value

        # Add vendor code
        if self.vendor_code:
            vendor_code_el = XMLSubElement(offer_el, "vendorCode")
            vendor_code_el.text = self.vendor_code

        # Add price
        self.price.to_xml(offer_el)

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
