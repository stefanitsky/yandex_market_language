from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET


XMLElement = ET.Element
XMLSubElement = ET.SubElement


class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        raise NotImplementedError

    @staticmethod
    def _clean_dict(d: dict) -> dict:
        return dict(**{k: v for k, v in d.items() if v})
