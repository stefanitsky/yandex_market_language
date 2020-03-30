from typing import Optional

from .base import BaseModel, XMLElement

from yandex_market_language.exceptions import ValidationError


CURRENCY_CHOICES = ("RUR", "RUB", "UAH", "BYN", "KZT", "USD", "EUR")
RATE_CHOICES = ("CBRF", "NBU", "NBK", "CB")


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
            raise ValidationError(
                "Price data is accepted only in: (formatted_choices)".format(
                    formatted_choices=", ".join(CURRENCY_CHOICES)
                )
            )
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
                    (
                        "The rate parameter can have the following values: "
                        "number (int or float), (rate_choices)".format(
                            rate_choices=', '.join(RATE_CHOICES)
                        )
                    )
                )

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

    def create_dict(self, **kwargs) -> dict:
        return dict(id=self.currency, rate=self.rate, plus=self.plus)

    def create_xml(self, **kwargs) -> XMLElement:
        el = XMLElement("currency", self.clean_dict)
        return el
