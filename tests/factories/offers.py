from unittest import mock

from yandex_market_language.models.offers import BaseOffer, SimplifiedOffer
from yandex_market_language.models.currency import CURRENCY_CHOICES
from faker import Faker

from .price import PriceFactory
from .option import OptionFactory

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
        delivery=True,
        pickup=True,
        delivery_options=None,
        pickup_options=None,
    ):
        if pictures is None:
            pictures = [fake.url() for _ in range(3)]
        if delivery_options is None:
            delivery_options = [OptionFactory() for _ in range(3)]
        if pickup_options is None:
            pickup_options = [OptionFactory() for _ in range(3)]

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
