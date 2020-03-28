from yandex_market_language.models import Shop
from faker import Faker

fake = Faker()


def generate_random_shop(
    name=fake.company_suffix(),
    company=fake.company(),
    url=fake.url(),
):
    return Shop(
        name=name,
        company=company,
        url=url
    )


ShopFactory = generate_random_shop
