from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET


XMLElement = ET.Element
XMLSubElement = ET.SubElement


class BaseModel(ABC):
    @abstractmethod
    def create_dict(self, **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_xml(self, **kwargs) -> XMLElement:
        raise NotImplementedError

    @property
    def clean_dict(self) -> dict:
        return dict(**{k: v for k, v in self.create_dict().items() if v})

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        el = self.create_xml()
        if root_el is not None:
            root_el.append(el)
        return el

    def to_dict(self, clean: bool = False) -> dict:
        return self.clean_dict if clean else self.create_dict()
