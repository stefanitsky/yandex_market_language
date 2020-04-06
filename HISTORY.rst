=======
History
=======

0.6.0 (2020-04-06)
------------------
* Added all missed models: Gifts & Promos.
* Added cbid warning message on set (field is deprecated).
* Added creation of an XML file from the Feed model.

0.5.0 (2020-04-02)
------------------
* Added missed offers of types: audiobook, artist.title, medicine, event-ticket & alco.
* Some fixes for fields.

0.4.0 (2020-04-01)
------------------
* Added xml parsing for all models, except: Gifts, Promos and another types of offers like audiobooks, medicine etc.
* Fixed fields parsing for datetime fields & fields that can be None.
* Added new field for offer: supplier.

0.3.0 (2020-03-30)
------------------

* All missing fields and models were added for the BaseOffer.
* SimplifiedOffer is now fully supported for xml / dict.
* Custom exception classes removed and replaced with ValidationError.

0.2.0 (2020-03-29)
------------------

* Added models for xml to dict and backward support: Category, Currency, Feed, Option (delivery / pickup), Price.
* Added basic models implementation (WIP): Shop, Offers.
* Added basic validation support (WIP, will be improved after finishing of models).

0.1.0 (2020-03-28)
------------------

* First release on PyPI.
