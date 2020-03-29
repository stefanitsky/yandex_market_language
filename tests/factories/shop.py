from yandex_market_language.models import Shop
from faker import Faker

from .currency import CurrencyFactory
from .category import CategoryFactory

fake = Faker()


def generate_random_shop(
    name=fake.company_suffix(),
    company=fake.company(),
    url=fake.url(),
    currencies=None,
    categories=None,
):
    if currencies is None:
        currencies = [CurrencyFactory() for _ in range(3)]
    if categories is None:
        categories = [CategoryFactory() for _ in range(3)]

    return Shop(
        name=name,
        company=company,
        url=url,
        currencies=currencies,
        categories=categories,
    )


ShopFactory = generate_random_shop
