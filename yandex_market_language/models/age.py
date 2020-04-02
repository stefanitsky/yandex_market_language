from .abstract import AbstractModel, XMLElement

from yandex_market_language.exceptions import ValidationError


UNIT_CHOICES = ("year", "month")
YEAR_CHOICES = [y for y in range(0, 19, 6)]
MONTH_CHOICES = [m for m in range(0, 13)]


class Age(AbstractModel):
    """
    Age category of the offer.
    """
    def __init__(self, unit: str, value):
        self.unit = unit
        self.value = value

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, value):
        if value and value not in UNIT_CHOICES:
            raise ValidationError("unit must be a valid choice: {c}".format(
                c=", ".join(UNIT_CHOICES)
            ))
        self._unit = value

    @property
    def value(self) -> int:
        return int(self._value)

    @value.setter
    def value(self, v):
        try:
            v = int(v)

            # Check valid choices for specified unit
            not_valid, choices = False, None
            if self.unit == "year":
                if v not in YEAR_CHOICES:
                    not_valid, choices = True, YEAR_CHOICES
            else:
                if v not in MONTH_CHOICES:
                    not_valid, choices = True, MONTH_CHOICES

            # Raise ValidationError if choice is not valid
            if not_valid:
                raise ValidationError(
                    "value for unit 'year' must be a valid choice: "
                    "{c}".format(c=", ".join(str(c) for c in choices))
                )

            self._value = str(v)
        except (TypeError, ValueError):
            raise ValidationError("value must be a valid int")

    def create_dict(self, **kwargs) -> dict:
        return dict(unit=self.unit, value=self.value)

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {}
        if self._unit:
            attribs["unit"] = self._unit
        el = XMLElement("age", attribs)
        el.text = self._value
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Age":
        return Age(unit=el.attrib.get("unit"), value=el.text)
