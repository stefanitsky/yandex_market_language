from .base import BaseModel, XMLElement


class Category(BaseModel):
    def __init__(self, category_id, name, parent_id=None):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id

    def create_dict(self, **kwargs) -> dict:
        return dict(
            id=self.category_id, name=self.name, parent_id=self.parent_id
        )

    def create_xml(self, **kwargs) -> XMLElement:
        d = self.clean_dict
        name = d.pop("name")
        el = XMLElement("category", d)
        el.text = name
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Category":
        return Category("1234", "test")
