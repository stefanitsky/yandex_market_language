=====
Usage
=====

To use Yandex Market Language (YML) for Python in a project::

    from yandex_market_language import parse, convert


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


Parser / Converter
------------------

You can parse XML files into ready-to-use Feed model instance with parser::

    >>> from yandex_market_language import parse, convert
    >>> feed = parse("tests/fixtures/valid_feed.xml")
    >>> feed
    <yandex_market_language.models.feed.Feed object at 0x10d99fdf0>
    >>> feed.to_dict()
    {
        'shop': {
            'name': 'ZS',
            'company': 'ZoneSmart',
            'url': 'https://zonesmart.ru',
            ...
            'offers': [
                'type': None,
                'vendor': 'Brother',
                'vendor_code': 'ABC1234'
                ...
            ]
            ...
        }
    }

And convert Feed model instances into XML files::

    >>> convert("converted_from_feed_model.xml", feed)
    >>> feed = parse("converted_from_feed_model.xml")
    >>> feed
    <yandex_market_language.models.feed.Feed object at 0x10d8bdee0>
    >>> feed.to_xml()
    <Element 'yml_catalog' at 0x000002121B634E00>
    >>> from xml.etree import ElementTree as ET
    >>> ET.tostring(feed.to_xml())
    b'<yml_catalog date="2019-11-01 17:22">
        <shop>
            <name>ZS</name>
            <company>ZoneSmart</company>
            <url>https://zonesmart.ru</url>
            ...
            <offers>
                <offer>
                    <name>...</name>
                    <vendor>...</name>
                    <vendorCode>...</vendorCode>
                </offer>
                ...
            </offers>
            ...
        </shop>
    </yml_catalog>

