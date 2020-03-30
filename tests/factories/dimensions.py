from faker import Faker

from yandex_market_language.models import Dimensions

fake = Faker()


def create_random_dimensions(
    length=fake.pyfloat(),
    width=fake.pyfloat(),
    height=fake.pyfloat(),
) -> Dimensions:
    return Dimensions(length, width, height)


DimensionsFactory = create_random_dimensions
