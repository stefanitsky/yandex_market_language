from .base import BaseModel, XMLElement

from yandex_market_language.exceptions import ValidationError


class Dimensions(BaseModel):
    def __init__(self, length, wight, height):
        self.length = length
        self.width = wight
        self.height = height

    @staticmethod
    def _value_is_float(value, a) -> str:
        try:
            float(value)
            return str(value)
        except (TypeError, ValueError):
            raise ValidationError("{a} must be a valid float".format(a=a))

    @property
    def length(self) -> float:
        return float(self._length)

    @length.setter
    def length(self, value):
        self._length = self._value_is_float(value, "length")

    @property
    def width(self) -> float:
        return float(self._width)

    @width.setter
    def width(self, value):
        self._width = self._value_is_float(value, "width")

    @property
    def height(self) -> float:
        return float(self._height)

    @height.setter
    def height(self, value):
        self._height = self._value_is_float(value, "height")

    def create_dict(self, **kwargs) -> dict:
        return dict(length=self.length, width=self.width, height=self.height)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("dimensions")
        el.text = "/".join([self._length, self._width, self._height])
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Dimensions":
        return Dimensions(*el.text.split("/"))
