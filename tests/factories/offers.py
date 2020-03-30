from unittest import mock

from yandex_market_language.models.offers import BaseOffer, SimplifiedOffer
from yandex_market_language.models.currency import CURRENCY_CHOICES
from faker import Faker

from .price import PriceFactory

fake = Faker()


@mock.patch.multiple(BaseOffer, __abstractmethods__=set())
def create_random_base_offer(
    vendor=fake.pystr(),
    vendor_code=fake.pystr(),
    offer_id=str(fake.pyint()),
    bid=str(fake.pyint()),
    url=fake.url(),
    price=PriceFactory(),
    old_price=str(fake.pyint()),
    enable_auto_discounts=fake.pybool(),
    currency=fake.random_element(CURRENCY_CHOICES),
    category_id=str(fake.pyint()),
    pictures=None,
    delivery=True,
    pickup=True,
) -> BaseOffer:
    if pictures is None:
        pictures = [fake.url() for _ in range(3)]

    return BaseOffer(
        vendor=vendor,
        vendor_code=vendor_code,
        offer_id=offer_id,
        bid=bid,
        url=url,
        price=price,
        old_price=old_price,
        enable_auto_discounts=enable_auto_discounts,
        currency=currency,
        category_id=category_id,
        pictures=pictures,
        delivery=delivery,
        pickup=pickup,
    )


def create_random_simplified_offer(name=fake.pystr()) -> SimplifiedOffer:
    base_offer = create_random_base_offer()
    return SimplifiedOffer(
        name=name,
        **base_offer.to_dict()
    )


BaseOfferFactory = create_random_base_offer
SimplifiedOfferFactory = create_random_simplified_offer
