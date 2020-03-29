from unittest import mock

from yandex_market_language.models.offers import BaseOffer, SimplifiedOffer
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
    old_price=str(fake.pyint())
) -> BaseOffer:
    return BaseOffer(
        vendor=vendor,
        vendor_code=vendor_code,
        offer_id=offer_id,
        bid=bid,
        url=url,
        price=price,
        old_price=old_price,
    )


def create_random_simplified_offer(name=fake.pystr()) -> SimplifiedOffer:
    base_offer = create_random_base_offer()
    return SimplifiedOffer(
        name=name,
        **base_offer.to_dict()
    )


BaseOfferFactory = create_random_base_offer
SimplifiedOfferFactory = create_random_simplified_offer
