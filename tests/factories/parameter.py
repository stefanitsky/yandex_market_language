from faker import Faker

from yandex_market_language.models import Parameter
fake = Faker()


def create_random_parameter(
    name=fake.pystr(),
    value=fake.pystr(),
    unit=fake.pystr(),
) -> Parameter:
    return Parameter(name, value, unit)


ParameterFactory = create_random_parameter
