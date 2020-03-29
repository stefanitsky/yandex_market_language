from .base import BaseModel, XMLElement

from yandex_market_language.exceptions import ValidationError


class Price(BaseModel):
    def __init__(self, value, is_starting: bool = False):
        self.value = value
        self.is_starting = is_starting

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
