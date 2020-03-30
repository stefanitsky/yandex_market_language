from faker import Faker

from yandex_market_language.models.age import (
    UNIT_CHOICES,
    MONTH_CHOICES,
    YEAR_CHOICES,
    Age,
)

fake = Faker()


def create_random_age(
    unit=fake.random_element(UNIT_CHOICES),
    value=None,
) -> Age:
    if value is None:
        if unit == "year":
            value = fake.random_element(YEAR_CHOICES)
        elif unit == "month":
            value = fake.random_element(MONTH_CHOICES)
    return Age(unit, value)


AgeFactory = create_random_age
