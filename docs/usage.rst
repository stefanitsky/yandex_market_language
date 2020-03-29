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
    >>> {'id': '1', 'name': 'Shoes', 'parent_id': None}

Or XML element::

    >>> el = category.to_xml()
    >>> el
    <Element 'category' at 0x10ecda900>
    >>> from xml.etree import ElementTree as ET
    >>> ET.tostring(el)
    b'<category id="1">Shoes</category>'
