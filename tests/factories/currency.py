from yandex_market_language.models.currency import (
    Currency,
    CURRENCY_CHOICES,
    RATE_CHOICES
)
from faker import Faker

fake = Faker()


def generate_random_currency(
    currency=fake.random_element(CURRENCY_CHOICES),
    rate=fake.random_element(RATE_CHOICES + (1, 2.0, 3.0)),
    plus=fake.random_element(["1", 2, 3.0]),
):
    return Currency(currency=currency, rate=rate, plus=plus)


CurrencyFactory = generate_random_currency
