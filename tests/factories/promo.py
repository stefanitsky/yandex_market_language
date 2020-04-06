from yandex_market_language import models
from faker import Faker

fake = Faker()


def create_random_promo(
    promo_id=fake.pystr(),
) -> "models.Promo":
    return models.Promo(
        promo_id=promo_id
    )


Promo = create_random_promo
