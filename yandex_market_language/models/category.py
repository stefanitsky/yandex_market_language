from .abstract import AbstractModel, XMLElement


class Category(AbstractModel):
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
        el.attrib["category_id"] = el.attrib.pop("id")
        el.attrib["parent_id"] = el.attrib.pop("parentId", None)
        return Category(name=el.text, **el.attrib)
