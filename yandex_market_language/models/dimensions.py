from .abstract import AbstractModel, XMLElement


class Dimensions(AbstractModel):
    """
    Offer dimensions model (length, width, height) in the package in
    centimeters.
    """
    def __init__(self, length, wight, height):
        self.length = length
        self.width = wight
        self.height = height

    @property
    def length(self) -> float:
        return float(self._length)

    @length.setter
    def length(self, value):
        self._length = self._is_valid_float(value, "length")

    @property
    def width(self) -> float:
        return float(self._width)

    @width.setter
    def width(self, value):
        self._width = self._is_valid_float(value, "width")

    @property
    def height(self) -> float:
        return float(self._height)

    @height.setter
    def height(self, value):
        self._height = self._is_valid_float(value, "height")

    def create_dict(self, **kwargs) -> dict:
        return dict(length=self.length, width=self.width, height=self.height)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("dimensions")
        el.text = "/".join([self._length, self._width, self._height])
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Dimensions":
        return Dimensions(*el.text.split("/"))
