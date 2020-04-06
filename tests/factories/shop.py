from yandex_market_language import models
from tests import factories
from faker import Faker

fake = Faker()


def generate_random_shop(
    name=fake.company_suffix(),
    company=fake.company(),
    url=fake.url(),
    platform=fake.pystr(),
    version=fake.pystr(),
    agency=fake.pystr(),
    email=fake.pystr(),
    currencies=None,
    categories=None,
    delivery_options=None,
    pickup_options=None,
    enable_auto_discounts=fake.pybool(),
    offers=None,
    gifts=None,
    promos=None,
) -> "models.Shop":
    if currencies is None:
        currencies = [factories.CurrencyFactory() for _ in range(3)]
    if categories is None:
        categories = [factories.CategoryFactory() for _ in range(3)]
    if delivery_options is None:
        delivery_options = [factories.OptionFactory() for _ in range(3)]
    if pickup_options is None:
        pickup_options = [factories.OptionFactory() for _ in range(3)]
    if offers is None:
        offers = [
            factories.SimplifiedOfferFactory().create(),
            factories.ArbitraryOfferFactory().create(),
            factories.BookOfferFactory().create(),
        ]
    if gifts is None:
        gifts = [factories.GiftFactory() for _ in range(3)]
    if promos is None:
        promos = [factories.Promo() for _ in range(3)]

    return models.Shop(
        name=name,
        company=company,
        url=url,
        platform=platform,
        version=version,
        agency=agency,
        email=email,
        currencies=currencies,
        categories=categories,
        delivery_options=delivery_options,
        pickup_options=pickup_options,
        enable_auto_discounts=enable_auto_discounts,
        offers=offers,
        gifts=gifts,
        promos=promos,
    )


ShopFactory = generate_random_shop
