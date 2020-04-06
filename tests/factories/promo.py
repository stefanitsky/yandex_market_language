from yandex_market_language import models
from faker import Faker

fake = Faker()


def create_random_product(
    offer_id=fake.pystr(),
    category_id=fake.pystr(),
) -> "models.Product":
    return models.Product(offer_id, category_id)


Product = create_random_product


def create_random_purchase(
    required_quantity=str(fake.pyint()),
    products=None,
) -> "models.Purchase":
    if products is None:
        products = [Product() for _ in range(3)]

    return models.Purchase(products, required_quantity)


Purchase = create_random_purchase


def create_random_promo(
    promo_id=fake.pystr(),
    promo_type="gift with purchase",
    start_date=str(fake.date()),
    end_date=str(fake.date()),
    description=fake.text(),
    url=fake.url(),
    purchase=Purchase(),
) -> "models.Promo":
    return models.Promo(
        promo_id=promo_id,
        promo_type=promo_type,
        start_date=start_date,
        end_date=end_date,
        description=description,
        url=url,
        purchase=purchase,
    )


Promo = create_random_promo

