from yandex_market_language import models
from faker import Faker

fake = Faker()


def create_random_gift(
    id=fake.pystr(), name=fake.word(), pictures=None
) -> "models.Gift":
    if pictures is None:
        pictures = [fake.url() for _ in range(3)]

    return models.Gift(id, name, pictures)


GiftFactory = create_random_gift
