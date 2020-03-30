from typing import Optional

from yandex_market_language.exceptions import ValidationError


ENABLE_AUTO_DISCOUNTS_CHOICES = ("yes", "true", "1", "no", "false", "0")


class EnableAutoDiscountField:
    _enable_auto_discounts = None

    @property
    def enable_auto_discounts(self) -> Optional[bool]:
        if self._enable_auto_discounts:
            if self._enable_auto_discounts in ["yes", "true", "1"]:
                return True
            elif self._enable_auto_discounts in ["no", "false", "0"]:
                return False
        return None

    @enable_auto_discounts.setter
    def enable_auto_discounts(self, value):
        if value in ["yes", "true", "1", "no", "false", "0"]:
            self._enable_auto_discounts = value
        elif value is True:
            self._enable_auto_discounts = "true"
        elif value is False:
            self._enable_auto_discounts = "false"
        elif value is None:
            self._enable_auto_discounts = value
        else:
            raise ValidationError(
                (
                    "enable_auto_discounts should be True, False "
                    "or str from available values: {values}".format(
                        values=", ".join(ENABLE_AUTO_DISCOUNTS_CHOICES)
                    )
                )
            )
