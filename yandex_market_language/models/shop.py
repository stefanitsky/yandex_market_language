from typing import List

from .base import BaseModel, XMLElement, XMLSubElement
from .currency import Currency
from .category import Category
from .option import Option
from . import fields

from yandex_market_language.exceptions import ValidationError


class Shop(
    fields.EnableAutoDiscountField,
    fields.DeliveryOptionsField,
    fields.PickupOptionsField,
    BaseModel
):
    def __init__(
        self,
        name: str,
        company: str,
        url: str,
        currencies: List[Currency],
        categories: List[Category],
        platform: str = None,
        version: str = None,
        agency: str = None,
        email: str = None,
        delivery_options: List[Option] = None,
        pickup_options: List[Option] = None,
        enable_auto_discounts=None,
    ):
        self.name = name
        self.company = company
        self.url = url
        self.platform = platform
        self.version = version
        self.agency = agency
        self.email = email
        self.currencies = currencies
        self.categories = categories
        self.delivery_options = delivery_options
        self.pickup_options = pickup_options
        self.enable_auto_discounts = enable_auto_discounts

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        if len(value) > 512:
            raise ValidationError("The maximum url length is 512 characters.")
        self._url = value

    def create_dict(self, **kwargs) -> dict:
        return dict(
            name=self.name,
            company=self.company,
            url=self.url,
            platform=self.platform,
            version=self.version,
            agency=self.agency,
            email=self.email,
            currencies=[c.to_dict() for c in self.currencies],
            categories=[c.to_dict() for c in self.categories],
            delivery_options=[o.to_dict() for o in self.delivery_options],
            pickup_options=[o.to_dict() for o in self.pickup_options],
            enable_auto_discounts=self.enable_auto_discounts,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        shop_el = XMLElement("shop")

        # Add simple elements
        for tag in (
            "name",
            "company",
            "url",
            "platform",
            "version",
            "agency",
            "email",
        ):
            value = getattr(self, tag)
            if value:
                el = XMLSubElement(shop_el, tag)
                el.text = value

        # Add enable_auto_discounts
        if self._enable_auto_discounts:
            enable_auto_discounts_el = XMLSubElement(
                shop_el, "enable_auto_discounts"
            )
            enable_auto_discounts_el.text = self._enable_auto_discounts

        # Add currencies
        currencies_el = XMLSubElement(shop_el, "currencies")
        for c in self.currencies:
            c.to_xml(currencies_el)

        # Add categories
        categories_el = XMLSubElement(shop_el, "categories")
        for c in self.categories:
            c.to_xml(categories_el)

        # Add delivery options
        if self.delivery_options:
            delivery_options_el = XMLSubElement(shop_el, "delivery-options")
            for o in self.delivery_options:
                o.to_xml(delivery_options_el)

        # Add pickup options
        if self.pickup_options:
            pickup_options_el = XMLSubElement(shop_el, "pickup-options")
            for o in self.pickup_options:
                o.to_xml(pickup_options_el)

        return shop_el

    @staticmethod
    def from_xml(shop_el: XMLElement) -> "Shop":
        kwargs = {}

        for el in shop_el:
            if el.tag == "currencies":
                currencies = []
                for currency_el in el:
                    currencies.append(Currency.from_xml(currency_el))
                kwargs["currencies"] = currencies
            elif el.tag == "categories":
                categories = []
                for category_el in el:
                    categories.append(Category.from_xml(category_el))
                kwargs["categories"] = categories
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
            else:
                kwargs[el.tag] = el.text

        return Shop(**kwargs)
