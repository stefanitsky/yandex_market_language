from unittest import TestCase

from yandex_market_language.exceptions import ValidationError
from yandex_market_language.models.fields.enable_auto_discounts import (
    EnableAutoDiscountField,
    ENABLE_AUTO_DISCOUNTS_CHOICES,
)


class EnableAutoDiscountsFieldTestCase(TestCase):
    def test_enable_auto_discounts_validation_error(self):
        msg = (
            "enable_auto_discounts should be True, False or str from available"
            " values: {values}".format(
                values=", ".join(ENABLE_AUTO_DISCOUNTS_CHOICES)
            )
        )
        with self.assertRaises(ValidationError) as e:
            f = EnableAutoDiscountField()
            f.enable_auto_discounts = "err"
            self.assertEqual(str(e), msg)

    def test_enable_auto_discounts_property(self):
        f = EnableAutoDiscountField()

        for v in ["yes", "true", "1"]:
            f.enable_auto_discounts = v
            self.assertEqual(f.enable_auto_discounts, True)

        for v in ["no", "false", "0"]:
            f.enable_auto_discounts = v
            self.assertEqual(f.enable_auto_discounts, False)

        f.enable_auto_discounts = None
        self.assertEqual(f.enable_auto_discounts, None)

        f.enable_auto_discounts = True
        self.assertEqual(f.enable_auto_discounts, True)

        f.enable_auto_discounts = False
        self.assertEqual(f.enable_auto_discounts, False)
