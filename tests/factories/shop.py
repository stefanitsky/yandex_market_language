from yandex_market_language.models import Shop
from faker import Faker

from .currency import CurrencyFactory
from .category import CategoryFactory
from .option import OptionFactory
from .offers import (
    SimplifiedOfferFactory,
    ArbitraryOfferFactory,
    BookOfferFactory
)

fake = Faker()


def generate_random_shop(
    name=fake.company_suffix(),
    company=fake.company(),
    url=fake.url(),
    platform=fake.pystr(),
    version=fake.pystr(),
    agency=fake.pystr(),
    email=fake.pystr(),
    currencies=None,
    categories=None,
    delivery_options=None,
    pickup_options=None,
    enable_auto_discounts=fake.pybool(),
    offers=None,
):
    if currencies is None:
        currencies = [CurrencyFactory() for _ in range(3)]
    if categories is None:
        categories = [CategoryFactory() for _ in range(3)]
    if delivery_options is None:
        delivery_options = [OptionFactory() for _ in range(3)]
    if pickup_options is None:
        pickup_options = [OptionFactory() for _ in range(3)]
    if offers is None:
        offers = [
            SimplifiedOfferFactory().create(),
            ArbitraryOfferFactory().create(),
            BookOfferFactory().create(),
        ]

    return Shop(
        name=name,
        company=company,
        url=url,
        platform=platform,
        version=version,
        agency=agency,
        email=email,
        currencies=currencies,
        categories=categories,
        delivery_options=delivery_options,
        pickup_options=pickup_options,
        enable_auto_discounts=enable_auto_discounts,
        offers=offers,
    )


ShopFactory = generate_random_shop
