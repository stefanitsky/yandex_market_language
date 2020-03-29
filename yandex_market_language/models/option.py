from .base import BaseModel, XMLElement


class Option(BaseModel):
    def __init__(self, cost, days, order_before=None):
        self.cost = cost
        self.days = days
        self.order_before = order_before

    def create_dict(self, **kwargs) -> dict:
        return dict(
            cost=self.cost, days=self.days, order_before=self.order_before
        )

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("option", attrib=self.clean_dict)
        return el
