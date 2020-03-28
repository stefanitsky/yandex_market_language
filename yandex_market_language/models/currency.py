from .base import BaseModel, XMLElement, XMLSubElement

from yandex_market_language.exceptions import ValidationError


CURRENCY_CHOICES = ("RUR", "RUB", "UAH", "BYN", "KZT", "USD", "EUR")
RATE_CHOICES = ("CBRF", "NBU", "NBK", "CB")


class CurrencyChoicesValidationError(ValidationError):
    def __str__(self):
        formatted_choices = ", ".join(CURRENCY_CHOICES)
        return f"Price data is accepted only in: {formatted_choices}"


class Currency(BaseModel):
    def __init__(self, currency, rate, plus):
        self.currency = currency
        self.rate = rate
        self.plus = plus

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, value):
        if value not in CURRENCY_CHOICES:
            raise CurrencyChoicesValidationError
        self._currency = value

    @property
    def rate(self) -> str:
        return self._rate

    @rate.setter
    def rate(self, value):
        if value not in RATE_CHOICES:
            try:
                float(value)
            except (TypeError, ValueError):
                raise ValidationError(
                    "The rate parameter can have the following values: "
                    f"number (int or float), {', '.join(RATE_CHOICES)}"
                )

        self._rate = str(value)

    @property
    def plus(self) -> str:
        return self._plus

    @plus.setter
    def plus(self, value):
        try:
            int(value)
            self._plus = str(value)
        except (TypeError, ValueError):
            raise ValidationError("The plus parameter only can be int.")

    def to_dict(self) -> dict:
        return dict(id=self.currency, rate=self.rate, plus=self.plus)

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        if root_el is not None:
            return XMLSubElement(root_el, "currency", self.to_dict())
        else:
            return XMLElement("currency", self.to_dict())
