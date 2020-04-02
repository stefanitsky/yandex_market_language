from typing import Optional

from .abstract import AbstractModel, XMLElement


class Price(AbstractModel):
    """
    Actual offer price model.
    """
    def __init__(self, value, is_starting=False):
        self.value = value
        self.is_starting = is_starting

    @property
    def is_starting(self) -> Optional[bool]:
        return self._str_to_bool(self._is_starting)

    @is_starting.setter
    def is_starting(self, value):
        self._is_starting = self._is_valid_bool(value, "is_starting", True)

    @property
    def value(self) -> float:
        return float(self._value)

    @value.setter
    def value(self, v):
        self._value = self._is_valid_float(v, "price")

    def create_dict(self, **kwargs) -> dict:
        return dict(value=self.value, is_starting=self.is_starting)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("price")

        if self.is_starting:
            el.attrib["from"] = "true"

        el.text = self._value
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "AbstractModel":
        return Price(el.text, el.attrib.get("from", False))
