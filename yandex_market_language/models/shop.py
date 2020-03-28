from .base import BaseModel, XMLElement, XMLSubElement


class Shop(BaseModel):
    def __init__(self, name: str):
        self.name = name

    def to_dict(self) -> dict:
        return dict(name=self.name)

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        if root_el is not None:
            shop_el = XMLSubElement(root_el, "shop")
        else:
            shop_el = XMLElement("shop")
        XMLSubElement(shop_el, "name", text=self.name)
        return shop_el
