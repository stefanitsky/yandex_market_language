from .abstract import AbstractModel, XMLElement

from yandex_market_language.exceptions import ValidationError


CONDITION_CHOICES = ("likenew", "used")


class Condition(AbstractModel):
    """
    Condition model.
    Used for used goods and goods discounted due to deficiencies.

    Docs:
    https://yandex.ru/support/partnermarket/elements/condition.html
    """
    def __init__(self, condition_type: str, reason: str):
        self.condition_type = condition_type
        self.reason = reason

    @property
    def condition_type(self) -> str:
        return self._condition_type

    @condition_type.setter
    def condition_type(self, value):
        if value not in CONDITION_CHOICES:
            raise ValidationError(
                "condition_type attribute must be a value from a list: "
                "{list}".format(list=", ".join(CONDITION_CHOICES))
            )
        self._condition_type = value

    def create_dict(self, **kwargs) -> dict:
        return dict(condition_type=self.condition_type, reason=self.reason)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("condition", {"type": self.condition_type})
        reason_el = XMLElement("reason")
        reason_el.text = self.reason
        el.append(reason_el)
        return el

    @staticmethod
    def from_xml(el: XMLElement) -> "Condition":
        return Condition(condition_type=el.attrib["type"], reason=el[0].text)
