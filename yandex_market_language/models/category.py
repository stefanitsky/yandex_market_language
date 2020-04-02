from .abstract import AbstractModel, XMLElement


class Category(AbstractModel):
    """
    Category model for shop.

    Docs:
    https://yandex.ru/support/partnermarket/elements/categories.html
    """
    def __init__(self, category_id, name, parent_id=None):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id

    def create_dict(self, **kwargs) -> dict:
        return dict(
            id=self.category_id, name=self.name, parent_id=self.parent_id
        )

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"id": self.category_id}

        if self.parent_id:
            attribs["parentId"] = self.parent_id

        el = XMLElement("category", attribs)
        el.text = self.name
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Category":
        return Category(
            category_id=el.attrib["id"],
            name=el.text,
            parent_id=el.attrib.get("parentId")
        )
