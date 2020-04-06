from yandex_market_language import models
from yandex_market_language.models.abstract import XMLElement, XMLSubElement


class Promo(models.AbstractModel):

    MAPPING = {
        "start-date": "start_date",
        "end-date": "end_date",
        "description": "description",
        "url": "url",
    }

    def __init__(
        self,
        promo_id: str,
        promo_type: str,
        start_date=None,
        end_date=None,
        description=None,
        url=None,
    ):
        self.promo_id = promo_id
        self.promo_type = promo_type
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.url = url

    def create_dict(self, **kwargs) -> dict:
        return dict(
            promo_id=self.promo_id,
            promo_type=self.promo_type,
            start_date=self.start_date,
            end_date=self.end_date,
            description=self.description,
            url=self.url,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"id": self.promo_id, "type": self.promo_type}
        promo_el = XMLElement("promo", attribs)

        for tag, attr in self.MAPPING.items():
            v = getattr(self, attr)
            if v:
                el = XMLSubElement(promo_el, tag)
                el.text = v

        return promo_el

    @classmethod
    def from_xml(cls, promo_el: XMLElement) -> "Promo":
        kwargs = dict(
            promo_id=promo_el.attrib.get("id"),
            promo_type=promo_el.attrib.get("type"),
        )

        for el in promo_el:
            if el.tag in cls.MAPPING:
                kwargs[cls.MAPPING[el.tag]] = el.text

        return Promo(**kwargs)
