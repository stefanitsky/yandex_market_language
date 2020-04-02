from datetime import datetime

from .abstract import AbstractModel, XMLElement
from .shop import Shop

DATE_FORMAT = "%Y-%m-%d %H:%M"


class Feed(AbstractModel):
    """
    YML Feed model.

    Docs:
    https://yandex.ru/support/partnermarket/export/yml.html
    """
    def __init__(self, shop: Shop, date: datetime.date = None):
        self.shop = shop
        self.date = date

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, DATE_FORMAT)

    @date.setter
    def date(self, dt):
        dt = self._is_valid_datetime(dt, DATE_FORMAT, "date", True)
        if dt is None:
            dt = datetime.now().strftime(DATE_FORMAT)
        self._date = dt

    def create_dict(self, **kwargs) -> dict:
        return dict(
            shop=self.shop.to_dict(),
            date=self.date,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        feed_el = XMLElement("yml_catalog", {"date": self._date})
        self.shop.to_xml(feed_el)
        return feed_el

    @staticmethod
    def from_xml(el: XMLElement) -> "Feed":
        shop = Shop.from_xml(el[0])
        date = el.attrib.get("date")
        return Feed(shop, date=date)
