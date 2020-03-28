from abc import ABC, abstractmethod
from xml.etree import ElementTree as ET


XMLElement = ET.Element
XMLSubElement = ET.SubElement


class BaseModel(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        pass
