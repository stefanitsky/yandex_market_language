from yandex_market_language import models
from faker import Faker

fake = Faker()


def create_random_promo(
    promo_id=fake.pystr(),
    promo_type="gift with purchase",
    start_date=str(fake.date()),
    end_date=str(fake.date()),
    description=fake.text(),
    url=fake.url(),
) -> "models.Promo":
    return models.Promo(
        promo_id=promo_id,
        promo_type=promo_type,
        start_date=start_date,
        end_date=end_date,
        description=description,
        url=url,
    )


Promo = create_random_promo
