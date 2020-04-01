=====
Usage
=====

To use Yandex Market Language (YML) for Python in a project::

    import yandex_market_language


Models
--------

You can create models manually::

    >>> from yandex_market_language import models
    >>> category = models.Category(category_id="1", name="Shoes")

And then transform them into a dictionary::

    >>> d = category.to_dict()
    >>> d
    {'id': '1', 'name': 'Shoes', 'parent_id': None}

Or XML element::

    >>> el = category.to_xml()
    >>> el
    <Element 'category' at 0x10ecda900>
    >>> from xml.etree import ElementTree as ET
    >>> ET.tostring(el)
    b'<category id="1">Shoes</category>'


Parser
--------

You can parse XML files into ready-to-use Feed model instance with parser::

    >>> from yandex_market_language import parser
    >>> p = parser.YMLParser("./tests/fixtures/valid_feed.xml")
    >>> feed = p.parse()
    >>> feed
    <yandex_market_language.models.feed.Feed object at 0x107724370>
    >>> feed.to_dict()
