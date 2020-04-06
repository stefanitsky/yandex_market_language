from tests import cases, factories
from yandex_market_language import models


class PromoTest(cases.ModelTestCase):
    def test_to_dict(self):
        p = factories.Promo()
        d = p.to_dict()
        expected_dict = dict(
            promo_id=p.promo_id,
            promo_type=p.promo_type,
            start_date=p.start_date,
            end_date=p.end_date,
            description=p.description,
            url=p.url,
            purchase=p.purchase.to_dict(),
            promo_gifts=[pg.to_dict() for pg in p.promo_gifts],
        )
        self.assertEqual(d, expected_dict)

    def test_to_xml(self):
        p = factories.Promo()
        el = p.to_xml()

        attribs = {"id": p.promo_id, "type": p.promo_type}
        expected_el = cases.ET.Element("promo", attribs)
        for tag, attr in models.Promo.MAPPING.items():
            el_ = cases.ET.SubElement(expected_el, tag)
            el_.text = getattr(p, attr)

        # Add purchase
        p.purchase.to_xml(expected_el)

        # Add promo gifts
        promo_gifts_el = cases.ET.SubElement(expected_el, "promo-gifts")
        for pg in p.promo_gifts:
            pg.to_xml(promo_gifts_el)

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        p = factories.Promo()
        el = p.to_xml()
        parsed_p = models.Promo.from_xml(el)
        self.assertEqual(p.to_dict(), parsed_p.to_dict())


class PurchaseTest(cases.ModelTestCase):
    def test_to_dict(self):
        p = factories.Purchase()
        d = p.to_dict()
        expected_d = dict(
            required_quantity=p.required_quantity,
            products=[p.to_dict() for p in p.products]
        )
        self.assertEqual(d, expected_d)

    def test_to_xml(self):
        p = factories.Purchase()
        el = p.to_xml()

        expected_el = cases.ET.Element("purchase")

        q_el = cases.ET.SubElement(expected_el, "required-quantity")
        q_el.text = p.required_quantity

        # Add products el
        for _ in p.products:
            _.to_xml(expected_el)

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        p = factories.Purchase()
        el = p.to_xml()
        parsed_p = models.Purchase.from_xml(el)
        self.assertEqual(p.to_dict(), parsed_p.to_dict())


class ProductTest(cases.ModelTestCase):
    def test_to_dict(self):
        p = factories.Product()
        d = p.to_dict()
        expected_d = dict(offer_id=p.offer_id, category_id=p.category_id)
        self.assertEqual(d, expected_d)

    def test_to_xml(self):
        p = factories.Product()
        el = p.to_xml()

        attribs = {"offer-id": p.offer_id, "category-id": p.category_id}
        expected_el = cases.ET.Element("product", attribs)

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        p = factories.Product()
        el = p.to_xml()
        parsed_p = models.Product.from_xml(el)
        self.assertEqual(p.to_dict(), parsed_p.to_dict())


class PromoGiftTest(cases.ModelTestCase):
    def test_to_dict(self):
        pg = factories.PromoGift()
        d = pg.to_dict()
        expected_d = dict(gift_id=pg.gift_id, offer_id=pg.offer_id)
        self.assertEqual(d, expected_d)

    def test_to_xml(self):
        pg = factories.PromoGift()
        el = pg.to_xml()

        attribs = {}
        if pg.offer_id:
            attribs["offer-id"] = pg.offer_id
        elif pg.gift_id:
            attribs["gift-id"] = pg.gift_id
        expected_el = cases.ET.Element("promo-gift", attribs)

        self.assertElementsEquals(el, expected_el)

    def test_from_xml(self):
        pg = factories.PromoGift()
        el = pg.to_xml()
        parsed_pg = models.PromoGift.from_xml(el)
        self.assertEqual(pg.to_dict(), parsed_pg.to_dict())
