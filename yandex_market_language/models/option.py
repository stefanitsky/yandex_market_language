from .abstract import AbstractModel, XMLElement


class Option(AbstractModel):
    """
    Option model for both the delivery option and the pickup option.

    Docs:
    https://yandex.ru/support/partnermarket/elements/delivery-options.html
    https://yandex.ru/support/partnermarket/elements/pickup-options.html
    """
    def __init__(self, cost, days, order_before=None):
        self.cost = cost
        self.days = days
        self.order_before = order_before

    def create_dict(self, **kwargs) -> dict:
        return dict(
            cost=self.cost, days=self.days, order_before=self.order_before
        )

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"cost": self.cost, "days": self.days}
        if self.order_before:
            attribs["order-before"] = self.order_before
        el = XMLElement("option", attrib=attribs)
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Option":
        el.attrib["order_before"] = el.attrib.pop("order-before", None)
        return Option(**el.attrib)
