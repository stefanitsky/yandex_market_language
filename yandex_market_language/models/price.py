from typing import Optional

from .abstract import AbstractModel, XMLElement

from yandex_market_language.exceptions import ValidationError


class Price(AbstractModel):
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
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        try:
            float(v)
            self._value = str(v)
        except (TypeError, ValueError):
            raise ValidationError("price can be int or float type")

    def create_dict(self, **kwargs) -> dict:
        return dict(value=self.value, is_starting=self.is_starting)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("price")
        if self.is_starting:
            el.attrib["from"] = "true"
        el.text = self.value
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "AbstractModel":
        return Price(el.text, el.attrib.get("from", False))
