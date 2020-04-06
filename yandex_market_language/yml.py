from xml.dom import minidom
from xml.etree import ElementTree as ET

from yandex_market_language.models import Feed


class YML:
    """
    Main class for feed parse and conversion.
    """
    def __init__(self, file_or_path):
        self._file_or_path = file_or_path

    @staticmethod
    def prettify_el(el: "ET.Element") -> "ET.Element":
        """
        Return a pretty-printed XML string for the Element.
        """
        raw = ET.tostring(el, "utf-8")
        parsed = minidom.parseString(raw)
        prettified = parsed.toprettyxml(indent="\t")
        return ET.fromstring(prettified)

    def parse(self) -> "Feed":
        """
        Parses an XML feed file to the Feed model.
        """
        tree = ET.parse(self._file_or_path)
        root = tree.getroot()
        return Feed.from_xml(root)

    def convert(self, feed: "Feed", pretty: bool = True):
        """
        Converts Feed model to XML file.
        """
        feed_el = feed.to_xml()
        if pretty:
            feed_el = self.prettify_el(feed_el)
        tree = ET.ElementTree(feed_el)
        tree.write(self._file_or_path, encoding="utf-8")


def parse(file_or_path):
    return YML(file_or_path).parse()


def convert(file_or_path, feed: "Feed", pretty: bool = True):
    YML(file_or_path).convert(feed, pretty)
