from typing import Optional

from .base import BaseModel, XMLElement

from yandex_market_language.exceptions import ValidationError


CURRENCY_CHOICES = ("RUR", "RUB", "UAH", "BYN", "KZT", "USD", "EUR")
RATE_CHOICES = ("CBRF", "NBU", "NBK", "CB")


class CurrencyChoicesValidationError(ValidationError):
    def __str__(self):
        return "Price data is accepted only in: (formatted_choices)".format(
            formatted_choices=", ".join(CURRENCY_CHOICES)
        )


class RateValidationError(ValidationError):
    def __str__(self):
        return (
            "The rate parameter can have the following values: "
            "number (int or float), (rate_choices)".format(
                rate_choices=', '.join(RATE_CHOICES)
            )
        )


class Currency(BaseModel):
    def __init__(self, currency, rate, plus=None):
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
                raise RateValidationError

        self._rate = str(value)

    @property
    def plus(self) -> Optional[str]:
        return self._plus

    @plus.setter
    def plus(self, value):
        try:
            if value:
                int(value)
                value = str(value)
            self._plus = value
        except (TypeError, ValueError):
            raise ValidationError("The plus parameter only can be int.")

    def to_dict(self, *, clean: bool = False) -> dict:
        d = dict(id=self.currency, rate=self.rate, plus=self.plus)
        return super()._clean_dict(d) if clean else d

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        attribs = self.to_dict(clean=True)
        el = XMLElement("currency", attribs)
        return super()._to_xml(el, root_el)
