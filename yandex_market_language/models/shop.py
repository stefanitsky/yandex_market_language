from typing import List, Optional

from .base import BaseModel, XMLElement, XMLSubElement
from .currency import Currency
from .category import Category
from .option import Option

from yandex_market_language.exceptions import ValidationError


ENABLE_AUTO_DISCOUNTS_CHOICES = ("yes", "true", "1", "no", "false", "0")


class EnableAutoDiscountsValidationError(ValidationError):
    def __str__(self):
        return (
            "enable_auto_discounts should be True, False or str from available"
            " values: {v}".format(v=", ".join(ENABLE_AUTO_DISCOUNTS_CHOICES))
        )


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

    @property
    def enable_auto_discounts(self) -> Optional[bool]:
        if self._enable_auto_discounts:
            if self._enable_auto_discounts in ["yes", "true", "1"]:
                return True
            elif self._enable_auto_discounts in ["no", "false", "0"]:
                return False
        return None

    @enable_auto_discounts.setter
    def enable_auto_discounts(self, value):
        if value in ["yes", "true", "1", "no", "false", "0"]:
            self._enable_auto_discounts = value
        elif value is True:
            self._enable_auto_discounts = "true"
        elif value is False:
            self._enable_auto_discounts = "false"
        elif value is None:
            self._enable_auto_discounts = value
        else:
            raise EnableAutoDiscountsValidationError

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
