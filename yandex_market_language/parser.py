from xml.etree import ElementTree as ET

from yandex_market_language.models import Feed


class YMLParser:
    def __init__(self, file_or_path):
        self._file_or_path = file_or_path
        self._tree = ET.parse(file_or_path)

    def parse(self) -> Feed:
        return Feed.from_xml(self._tree.getroot())
