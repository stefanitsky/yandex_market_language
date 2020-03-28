from yandex_market_language.models import Shop
from faker import Faker

from .currency import CurrencyFactory

fake = Faker()


def generate_random_shop(
    name=fake.company_suffix(),
    company=fake.company(),
    url=fake.url(),
    currencies=None
):
    if currencies is None:
        currencies = [CurrencyFactory() for _ in range(3)]

    return Shop(
        name=name,
        company=company,
        url=url,
        currencies=currencies
    )


ShopFactory = generate_random_shop
