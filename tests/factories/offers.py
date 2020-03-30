from unittest import mock

from yandex_market_language.models.offers import (
    BaseOffer,
    SimplifiedOffer,
    EXPIRY_FORMAT
)
from yandex_market_language.models.currency import CURRENCY_CHOICES
from faker import Faker

from .price import PriceFactory
from .option import OptionFactory
from .parameter import ParameterFactory
from .condition import ConditionFactory
from .dimensions import DimensionsFactory
from .age import AgeFactory


fake = Faker()


class BaseOfferFactory:

    __cls__ = BaseOffer

    def __init__(
        self,
        vendor=fake.pystr(),
        vendor_code=fake.pystr(),
        offer_id=str(fake.pyint()),
        bid=str(fake.pyint()),
        url=fake.url(),
        price=PriceFactory(),
        old_price=str(fake.pyint()),
        enable_auto_discounts=fake.pybool(),
        currency=fake.random_element(CURRENCY_CHOICES),
        category_id=str(fake.pyint()),
        pictures=None,
        delivery=None,
        pickup=None,
        delivery_options=None,
        pickup_options=None,
        description=fake.text(),
        sales_notes=fake.text(),
        min_quantity=fake.pyint(),
        manufacturer_warranty=fake.pybool(),
        country_of_origin=fake.random_element(["Австралия", "Австрия"]),
        adult=fake.pybool(),
        barcodes=None,
        parameters=None,
        condition=ConditionFactory(),
        credit_template_id=fake.pystr(),
        expiry=fake.date(EXPIRY_FORMAT),
        weight=fake.pyfloat(),
        dimensions=DimensionsFactory(),
        downloadable=fake.pybool(),
        available=fake.random_element([True, False, None]),
        age=AgeFactory(),
        group_id=fake.pyint(),
    ):
        if pictures is None:
            pictures = [fake.url() for _ in range(3)]
        if delivery_options is None:
            delivery_options = [OptionFactory() for _ in range(3)]
        if pickup_options is None:
            pickup_options = [OptionFactory() for _ in range(3)]
        if barcodes is None:
            barcodes = [fake.pystr() for _ in range(3)]
        if parameters is None:
            parameters = [ParameterFactory() for _ in range(3)]

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

    def get_values(self, **kwargs) -> dict:
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
            delivery_options=self.delivery_options,
            pickup_options=self.pickup_options,
            description=self.description,
            sales_notes=self.sales_notes,
            min_quantity=self.min_quantity,
            manufacturer_warranty=self.manufacturer_warranty,
            country_of_origin=self.country_of_origin,
            adult=self.adult,
            barcodes=self.barcodes,
            parameters=self.parameters,
            condition=self.condition,
            credit_template_id=self.credit_template_id,
            expiry=self.expiry,
            weight=self.weight,
            dimensions=self.dimensions,
            downloadable=self.downloadable,
            available=self.available,
            age=self.age,
            group_id=self.group_id,
            **kwargs,
        )

    @mock.patch.multiple(BaseOffer, __abstractmethods__=set())
    def create(self, **kwargs) -> "__cls__":
        return self.__cls__(**self.get_values(**kwargs))


class SimplifiedOfferFactory(BaseOfferFactory):

    __cls__ = SimplifiedOffer

    def __init__(self, name=fake.pystr(), **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def get_values(self) -> dict:
        return super().get_values(name=self.name)
