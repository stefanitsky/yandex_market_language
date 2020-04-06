import typing as t
from yandex_market_language import models
from yandex_market_language.models.abstract import XMLElement, XMLSubElement


class Promo(models.AbstractModel):
    """
    Docs: https://yandex.ru/support/partnermarket/elements/promo-gift.html
    """

    MAPPING = {
        "start-date": "start_date",
        "end-date": "end_date",
        "description": "description",
        "url": "url",
    }

    def __init__(
        self,
        promo_id: str,
        promo_type: str,
        purchase: "Purchase",
        promo_gifts: t.List["PromoGift"],
        start_date=None,
        end_date=None,
        description=None,
        url=None,
    ):
        self.promo_id = promo_id
        self.promo_type = promo_type
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.url = url
        self.purchase = purchase
        self.promo_gifts = promo_gifts

    def create_dict(self, **kwargs) -> dict:
        return dict(
            promo_id=self.promo_id,
            promo_type=self.promo_type,
            start_date=self.start_date,
            end_date=self.end_date,
            description=self.description,
            url=self.url,
            purchase=self.purchase.to_dict(),
            promo_gifts=[pg.to_dict() for pg in self.promo_gifts],
        )

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {"id": self.promo_id, "type": self.promo_type}
        promo_el = XMLElement("promo", attribs)

        for tag, attr in self.MAPPING.items():
            v = getattr(self, attr)
            if v:
                el = XMLSubElement(promo_el, tag)
                el.text = v

        # Add purchase el
        self.purchase.to_xml(promo_el)

        # Add promo gifts
        promo_gifts_el = XMLSubElement(promo_el, "promo-gifts")
        for pg in self.promo_gifts:
            pg.to_xml(promo_gifts_el)

        return promo_el

    @classmethod
    def from_xml(cls, promo_el: XMLElement) -> "Promo":
        kwargs = dict(
            promo_id=promo_el.attrib.get("id"),
            promo_type=promo_el.attrib.get("type"),
            promo_gifts=[]
        )

        for el in promo_el:
            if el.tag in cls.MAPPING:
                kwargs[cls.MAPPING[el.tag]] = el.text
            elif el.tag == "purchase":
                kwargs["purchase"] = Purchase.from_xml(el)
            elif el.tag == "promo-gifts":
                for pg_el in el:
                    kwargs["promo_gifts"].append(PromoGift.from_xml(pg_el))

        return Promo(**kwargs)


class Purchase(models.AbstractModel):
    """
    Docs: https://yandex.ru/support/partnermarket/elements/promo-gift.html
    """
    def __init__(self, products: t.List["Product"], required_quantity="1"):
        self.required_quantity = required_quantity
        self.products = products

    def create_dict(self, **kwargs) -> dict:
        return dict(
            required_quantity=self.required_quantity,
            products=[p.to_dict() for p in self.products]
        )

    def create_xml(self, **kwargs) -> XMLElement:
        purchase_el = XMLElement("purchase")

        # Add required quantity el
        required_quantity_el = XMLSubElement(purchase_el, "required-quantity")
        required_quantity_el.text = self.required_quantity

        # Add products el
        for p in self.products:
            p.to_xml(purchase_el)

        return purchase_el

    @staticmethod
    def from_xml(purchase_el: XMLElement) -> "Purchase":
        kwargs = {"products": []}

        for el in purchase_el:
            if el.tag == "required-quantity":
                kwargs["required_quantity"] = el.text
            elif el.tag == "product":
                kwargs["products"].append(Product.from_xml(el))

        return Purchase(**kwargs)


class Product(models.AbstractModel):
    """
    Docs: https://yandex.ru/support/partnermarket/elements/promo-gift.html
    """
    def __init__(self, offer_id: str = None, category_id: str = None):
        self.offer_id = offer_id
        self.category_id = category_id

    def create_dict(self, **kwargs) -> dict:
        return dict(
            offer_id=self.offer_id,
            category_id=self.category_id,
        )

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {}
        if self.offer_id:
            attribs["offer-id"] = self.offer_id
        if self.category_id:
            attribs["category-id"] = self.category_id
        return XMLElement("product", attribs)

    @staticmethod
    def from_xml(product_el: XMLElement) -> "Product":
        return Product(
            offer_id=product_el.attrib.get("offer-id"),
            category_id=product_el.attrib.get("category-id")
        )


class PromoGift(models.AbstractModel):
    """
    Docs:
    https://yandex.ru/support/partnermarket/elements/promo-gift.html
    """
    def __init__(self, offer_id: str = None, gift_id: str = None):
        self.offer_id = offer_id
        self.gift_id = gift_id

    def create_dict(self, **kwargs) -> dict:
        return dict(offer_id=self.offer_id, gift_id=self.gift_id)

    def create_xml(self, **kwargs) -> XMLElement:
        attribs = {}
        if self.offer_id:
            attribs["offer-id"] = self.offer_id
        elif self.gift_id:
            attribs["gift-id"] = self.gift_id
        return XMLElement("promo-gift", attribs)

    @staticmethod
    def from_xml(el: XMLElement) -> "PromoGift":
        return PromoGift(
            offer_id=el.attrib.get("offer-id"),
            gift_id=el.attrib.get("gift-id")
        )
