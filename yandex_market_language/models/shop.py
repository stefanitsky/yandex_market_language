from .base import BaseModel, XMLElement, XMLSubElement

from yandex_market_language.exceptions import ValidationError


class Shop(BaseModel):
    def __init__(
        self,
        name: str,
        company: str,
        url: str,
        platform: str = None,
        version: str = None,
        agency: str = None,
        email: str = None,
    ):
        self.name = name
        self.company = company
        self.url = url
        self.platform = platform
        self.version = version
        self.agency = agency
        self.email = email

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        if len(value) > 512:
            raise ValidationError("The maximum url length is 512 characters.")
        self._url = value

    def to_dict(self) -> dict:
        return dict(
            name=self.name,
            company=self.company,
            url=self.url,
            platform=self.platform,
            version=self.version,
            agency=self.agency,
            email=self.email,
        )

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        if root_el is not None:
            shop_el = XMLSubElement(root_el, "shop")
        else:
            shop_el = XMLElement("shop")

        # Add simple elements
        for tag in (
            "name",
            "company",
            "url",
            "platform",
            "version",
            "agency",
            "email",
        ):
            el = XMLSubElement(shop_el, tag)
            el.text = getattr(self, tag)

        return shop_el
