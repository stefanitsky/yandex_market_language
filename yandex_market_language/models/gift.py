from typing import List

from yandex_market_language.models import abstract


class Gift(abstract.AbstractModel):
    """
    Gift model.

    Docs:
    https://yandex.ru/support/partnermarket/elements/promo-gift.html
    """
    def __init__(
        self,
        id: str,
        name: str,
        pictures: List[str] = None,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.pictures = pictures

    def create_dict(self, **kwargs) -> dict:
        return dict(id=self.id, name=self.name, pictures=self.pictures)

    def create_xml(self, **kwargs) -> "abstract.XMLElement":
        gift_el = abstract.XMLElement("gift", {"id": self.id})
        name_el = abstract.XMLSubElement(gift_el, "name")
        name_el.text = self.name

        # Add pictures
        if self.pictures:
            for url in self.pictures:
                p_el = abstract.XMLSubElement(gift_el, "picture")
                p_el.text = url

        return gift_el

    @staticmethod
    def from_xml(gift_el: abstract.XMLElement) -> "Gift":
        kwargs = {"pictures": []}

        # Parse element
        for el in gift_el:
            if el.tag == "name":
                kwargs["name"] = el.text
            elif el.tag == "picture":
                kwargs["pictures"].append(el.text)

        return Gift(id=gift_el.attrib.get("id"), **kwargs)
