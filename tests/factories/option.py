from yandex_market_language.models import Option
from faker import Faker

fake = Faker()


def create_random_option(
    cost=str(fake.pyint()),
    days=fake.random_element(["2", "3", "3-5", "1-3"]),
    order_before=fake.random_element(["13", "15", "18"])
) -> Option:
    return Option(cost=cost, days=days, order_before=order_before)


OptionFactory = create_random_option
