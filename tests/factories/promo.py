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


def create_random_promo_gift(
    gift_id=None,
    offer_id=None,
) -> "models.PromoGift":
    if gift_id is None and offer_id is None:
        random_id_key = fake.random_element(["gift_id", "offer_id"])
        kwargs = {random_id_key: fake.pystr()}
    elif gift_id:
        kwargs = {"gift_id": gift_id}
    elif offer_id:
        kwargs = {"offer_id": offer_id}
    else:
        raise AttributeError("only one attr must be specified!")
    return models.PromoGift(**kwargs)


PromoGift = create_random_promo_gift


def create_random_promo(
    promo_id=fake.pystr(),
    promo_type="gift with purchase",
    start_date=str(fake.date()),
    end_date=str(fake.date()),
    description=fake.text(),
    url=fake.url(),
    purchase=Purchase(),
    promo_gifts=None,
) -> "models.Promo":
    if promo_gifts is None:
        promo_gifts = [PromoGift() for _ in range(3)]

    return models.Promo(
        promo_id=promo_id,
        promo_type=promo_type,
        start_date=start_date,
        end_date=end_date,
        description=description,
        url=url,
        purchase=purchase,
        promo_gifts=promo_gifts,
    )


Promo = create_random_promo
