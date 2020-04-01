from xml.etree import ElementTree as ET

from yandex_market_language.models import Feed


class YMLParser:
    def __init__(self, file_or_path):
        self._file_or_path = file_or_path

    def parse(self) -> Feed:
        tree = ET.parse(self._file_or_path)
        root = tree.getroot()
        return Feed.from_xml(root)
