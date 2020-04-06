from yandex_market_language import models
from tests import factories


def create_random_feed(
    shop=factories.ShopFactory()
) -> "models.Feed":
    return models.Feed(shop)


Feed = create_random_feed
