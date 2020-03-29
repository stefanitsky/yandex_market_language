from yandex_market_language.models import Price
from faker import Faker

fake = Faker()


def create_random_price(
    value=str(fake.random_element(["3", "5.6"])),
    is_starting=fake.pybool()
) -> Price:
    return Price(value=value, is_starting=is_starting)


PriceFactory = create_random_price
