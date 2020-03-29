from datetime import datetime

from .base import BaseModel, XMLElement
from .shop import Shop

DATE_FORMAT = "YYYY-MM-DD hh:mm"


class Feed(BaseModel):
    """
    YML Feed model.

    Docs: https://yandex.ru/support/partnermarket/export/yml.html
    """
    def __init__(self, shop: Shop, date: datetime.date = None):
        self.shop = shop
        self._date = date

        # Set default date if not specified
        if self._date is None:
            self._date = datetime.now()

        # Format date by YML required format
        self.date = self._date.strftime(DATE_FORMAT)

    def create_dict(self, **kwargs) -> dict:
        return dict(
            shop=self.shop.to_dict(),
            date=self.date,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        feed_el = XMLElement("yml_catalog", {"date": self.date})
        self.shop.to_xml(feed_el)
        return feed_el
