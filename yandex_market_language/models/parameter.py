from .abstract import AbstractModel, XMLElement

from yandex_market_language.exceptions import ValidationError


class Parameter(AbstractModel):
    """
    Model of offer characteristics and parameters.

    Docs:
    https://yandex.ru/support/partnermarket/elements/param.html
    """
    def __init__(self, name: str, value: str, unit: str = None):
        self.name = name
        self.value = value
        self.unit = unit

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, v):
        try:
            self._value = str(v)
        except (TypeError, ValueError):
            raise ValidationError("value must be a string")

    def create_dict(self, **kwargs) -> dict:
        return dict(name=self.name, value=self.value, unit=self.unit)

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"name": self.name}
        if self.unit:
            attribs["unit"] = self.unit
        el = XMLElement("param", attribs)
        el.text = self.value
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Parameter":
        return Parameter(value=el.text, **el.attrib)
