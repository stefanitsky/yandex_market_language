from typing import List

from .base import BaseModel, XMLElement, XMLSubElement
from .currency import Currency
from .category import Category
from .option import Option

from yandex_market_language.exceptions import ValidationError


class Shop(BaseModel):
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

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        if len(value) > 512:
            raise ValidationError("The maximum url length is 512 characters.")
        self._url = value

    @property
    def delivery_options(self):
        return self._delivery_options

    @delivery_options.setter
    def delivery_options(self, options):
        self._delivery_options = options if options else []

    @property
    def pickup_options(self):
        return self._pickup_options

    @pickup_options.setter
    def pickup_options(self, options):
        self._pickup_options = options if options else []

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
            el = XMLSubElement(shop_el, tag)
            el.text = getattr(self, tag)

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
