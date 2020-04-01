# from xml.dom import minidom
from xml.etree import ElementTree as ET

from yandex_market_language.models import Feed


class YMLParser:
    def __init__(self, file_or_path):
        self._file_or_path = file_or_path

    # @staticmethod
    # def prettify(el: ET.Element) -> str:
    #     """
    #     Return a pretty-printed XML string for the Element.
    #     """
    #     raw = ET.tostring(el, "utf-8")
    #     parsed = minidom.parseString(raw)
    #     return parsed.toprettyxml(indent="\t")

    def parse(self) -> Feed:
        tree = ET.parse(self._file_or_path)
        root = tree.getroot()
        return Feed.from_xml(root)
