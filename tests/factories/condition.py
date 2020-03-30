from faker import Faker


from yandex_market_language.models.condition import (
    Condition,
    CONDITION_CHOICES
)


fake = Faker()


def create_random_condition(
    condition_type=fake.random_element(CONDITION_CHOICES),
    reason=fake.text()
) -> Condition:
    return Condition(condition_type, reason)


ConditionFactory = create_random_condition
