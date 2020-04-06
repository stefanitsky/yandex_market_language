from yandex_market_language import models
from yandex_market_language.models.abstract import XMLElement


class Promo(models.AbstractModel):
    def __init__(
        self,
        promo_id: str,
        # promo_type: str,
    ):
        self.promo_id = promo_id

    def create_dict(self, **kwargs) -> dict:
        return dict(
            promo_id=self.promo_id,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"id": self.promo_id}
        promo_el = XMLElement("promo", attribs)

        ...

        return promo_el

    @staticmethod
    def from_xml(promo_el: XMLElement) -> "Promo":
        kwargs = dict(
            promo_id=promo_el.attrib.get("id"),
        )

        ...

        return Promo(**kwargs)
