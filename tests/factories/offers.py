from typing import List
from unittest import mock

from yandex_market_language.models import Parameter
from yandex_market_language.models.offers import (
    EXPIRY_FORMAT,
    DATE_FORMAT,
    AbstractOffer,
    SimplifiedOffer,
    ArbitraryOffer,
    AbstractBookOffer,
    BookOffer,
    AudioBookOffer,
    MusicVideoOffer,
    MedicineOffer,
    EventTicketOffer,
    AlcoholOffer,
)
from yandex_market_language.models.currency import CURRENCY_CHOICES
from faker import Faker

from .price import PriceFactory
from .option import OptionFactory
from .parameter import ParameterFactory
from .condition import ConditionFactory
from .dimensions import DimensionsFactory
from .age import AgeFactory


fake = Faker()


class AbstractOfferFactory:

    __cls__ = AbstractOffer

    def __init__(
        self,
        vendor=fake.pystr(),
        vendor_code=fake.pystr(),
        offer_id=str(fake.pyint()),
        bid=str(fake.pyint()),
        url=fake.url(),
        price=PriceFactory(),
        supplier=str(fake.pyint()),
        old_price=str(fake.pyint()),
        enable_auto_discounts=fake.pybool(),
        currency=fake.random_element(CURRENCY_CHOICES),
        category_id=str(fake.pyint()),
        pictures=None,
        delivery=None,
        pickup=None,
        delivery_options=None,
        pickup_options=None,
        store=fake.random_element([True, False, None]),
        description=fake.text(),
        sales_notes=fake.text(),
        min_quantity=fake.pyint(),
        manufacturer_warranty=fake.pybool(),
        country_of_origin=fake.random_element(["Австралия", "Австрия"]),
        adult=fake.pybool(),
        barcodes=None,
        parameters=None,
        condition=ConditionFactory(),
        credit_template_id=fake.pystr(),
        expiry=fake.date(EXPIRY_FORMAT),
        weight=fake.pyfloat(),
        dimensions=DimensionsFactory(),
        downloadable=fake.pybool(),
        available=fake.random_element([True, False, None]),
        age=AgeFactory(),
        group_id=fake.pyint(),
    ):
        if pictures is None:
            pictures = [fake.url() for _ in range(3)]
        if delivery_options is None:
            delivery_options = [OptionFactory() for _ in range(3)]
        if pickup_options is None:
            pickup_options = [OptionFactory() for _ in range(3)]
        if barcodes is None:
            barcodes = [fake.pystr() for _ in range(3)]
        if parameters is None:
            parameters = [ParameterFactory() for _ in range(3)]

        self.vendor = vendor
        self.vendor_code = vendor_code
        self.offer_id = offer_id
        self.bid = bid
        self.url = url
        self.price = price
        self.old_price = old_price
        self.enable_auto_discounts = enable_auto_discounts
        self.currency = currency
        self.category_id = category_id
        self.pictures = pictures
        self.supplier = supplier
        self.delivery = delivery
        self.pickup = pickup
        self.delivery_options = delivery_options
        self.pickup_options = pickup_options
        self.store = store
        self.description = description
        self.sales_notes = sales_notes
        self.min_quantity = min_quantity
        self.manufacturer_warranty = manufacturer_warranty
        self.country_of_origin = country_of_origin
        self.adult = adult
        self.barcodes = barcodes
        self.parameters = parameters
        self.condition = condition
        self.credit_template_id = credit_template_id
        self.expiry = expiry
        self.weight = weight
        self.dimensions = dimensions
        self.downloadable = downloadable
        self.available = available
        self.age = age
        self.group_id = group_id

    def get_values(self, **kwargs) -> dict:
        return dict(
            vendor=self.vendor,
            vendor_code=self.vendor_code,
            offer_id=self.offer_id,
            bid=self.bid,
            url=self.url,
            price=self.price,
            old_price=self.old_price,
            enable_auto_discounts=self.enable_auto_discounts,
            currency=self.currency,
            category_id=self.category_id,
            pictures=self.pictures,
            supplier=self.supplier,
            delivery=self.delivery,
            pickup=self.pickup,
            delivery_options=self.delivery_options,
            pickup_options=self.pickup_options,
            store=self.store,
            description=self.description,
            sales_notes=self.sales_notes,
            min_quantity=self.min_quantity,
            manufacturer_warranty=self.manufacturer_warranty,
            country_of_origin=self.country_of_origin,
            adult=self.adult,
            barcodes=self.barcodes,
            parameters=self.parameters,
            condition=self.condition,
            credit_template_id=self.credit_template_id,
            expiry=self.expiry,
            weight=self.weight,
            dimensions=self.dimensions,
            downloadable=self.downloadable,
            available=self.available,
            age=self.age,
            group_id=self.group_id,
            **kwargs,
        )

    @mock.patch.multiple(AbstractOffer, __abstractmethods__=set())
    def create(self, **kwargs) -> "__cls__":
        return self.__cls__(**self.get_values(**kwargs))


class SimplifiedOfferFactory(AbstractOfferFactory):

    __cls__ = SimplifiedOffer

    def __init__(self, name=fake.pystr(), **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def get_values(self) -> dict:
        return super().get_values(name=self.name)


class ArbitraryOfferFactory(AbstractOfferFactory):

    __cls__ = ArbitraryOffer

    def __init__(
        self,
        model=fake.pystr(),
        vendor=fake.pystr(),
        type_prefix=fake.pystr(),
        **kwargs
    ):
        super().__init__(vendor=vendor, **kwargs)
        self.model = model
        self.type_prefix = type_prefix

    def get_values(self, **kwargs) -> dict:
        return super().get_values(
            model=self.model,
            type_prefix=self.type_prefix
        )


class AbstractBookOfferFactory(AbstractOfferFactory):

    __cls__ = AbstractBookOffer

    def __init__(
        self,
        name=fake.pystr(),
        publisher=fake.pystr(),
        age=AgeFactory(),
        isbn=fake.pystr(),
        author=fake.name(),
        series=fake.text(),
        year=fake.year(),
        volume=fake.pyint(),
        part=fake.pyint(),
        language=fake.pystr(),
        table_of_contents=fake.text(),
        **kwargs
    ):
        super().__init__(age=age, **kwargs)
        self.name = name
        self.publisher = publisher
        self.isbn = isbn
        self.author = author
        self.series = series
        self.year = year
        self.volume = volume
        self.part = part
        self.language = language
        self.table_of_contents = table_of_contents

    def get_values(self, **kwargs) -> dict:
        return super().get_values(
            name=self.name,
            publisher=self.publisher,
            isbn=self.isbn,
            author=self.author,
            series=self.series,
            year=self.year,
            volume=self.volume,
            part=self.part,
            language=self.language,
            table_of_contents=self.table_of_contents,
            **kwargs
        )

    @mock.patch.multiple(AbstractBookOffer, __abstractmethods__=set())
    def create(self, **kwargs) -> "__cls__":
        return self.__cls__(**self.get_values(**kwargs))


class BookOfferFactory(AbstractBookOfferFactory):

    __cls__ = BookOffer

    def __init__(
        self,
        binding=fake.pystr(),
        page_extent=fake.pyint(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.binding = binding
        self.page_extent = page_extent

    def get_values(self, **kwargs) -> dict:
        return super().get_values(
            binding=self.binding,
            page_extent=self.page_extent,
        )


class AudioBookOfferFactory(AbstractBookOfferFactory):

    __cls__ = AudioBookOffer

    def __init__(
        self,
        performed_by=fake.name(),
        performance_type=fake.random_element(["радиоспектакль", "начитано"]),
        storage=fake.random_element(["CD", "касета", "flash"]),
        audio_format=fake.random_element(["mp3", "wav"]),
        recording_length=fake.random_element(["22:08", "13:37"]),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.performed_by = performed_by
        self.performance_type = performance_type
        self.storage = storage
        self.audio_format = audio_format
        self.recording_length = recording_length

    def get_values(self, **kwargs) -> dict:
        return super().get_values(
            performed_by=self.performed_by,
            performance_type=self.performance_type,
            storage=self.storage,
            audio_format=self.audio_format,
            recording_length=self.recording_length,
            **kwargs
        )


class MusicVideoOfferFactory(AbstractOfferFactory):

    __cls__ = MusicVideoOffer

    def __init__(
        self,
        artist: str = fake.name(),
        title: str = fake.words(),
        year: str = fake.year(),
        media: str = fake.pystr(),
        starring: str = fake.name(),
        director: str = fake.name(),
        original_name: str = fake.name(),
        country: str = fake.pystr(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.artist = artist
        self.title = title
        self.year = year
        self.media = media
        self.starring = starring
        self.director = director
        self.original_name = original_name
        self.country = country

    def get_values(self, **kwargs) -> dict:
        return super().get_values(
            artist=self.artist,
            title=self.title,
            year=self.year,
            media=self.media,
            starring=self.starring,
            director=self.director,
            original_name=self.original_name,
            country=self.country,
            **kwargs
        )


class MedicineOfferFactory(AbstractOfferFactory):

    __cls__ = MedicineOffer

    def __init__(self, name: str = fake.pystr(), **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def get_values(self, **kwargs) -> dict:
        return super().get_values(name=self.name)


class EventTicketOfferFactory(AbstractOfferFactory):

    __cls__ = EventTicketOffer

    def __init__(
        self,
        name=fake.name(),
        place=fake.pystr(),
        date=fake.date(DATE_FORMAT),
        hall=fake.pystr(),
        hall_part=fake.pystr(),
        is_premiere=fake.pybool(),
        is_kids=fake.pybool(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.place = place
        self.date = date
        self.hall = hall
        self.hall_part = hall_part
        self.is_premiere = is_premiere
        self.is_kids = is_kids

    def get_values(self, **kwargs) -> dict:
        return super().get_values(
            name=self.name,
            place=self.place,
            date=self.date,
            hall=self.hall,
            hall_part=self.hall_part,
            is_premiere=self.is_premiere,
            is_kids=self.is_kids,
        )


class AlcoholOfferFactory(AbstractOfferFactory):

    __cls__ = AlcoholOffer

    def __init__(
        self,
        name: str = fake.pystr(),
        vendor: str = fake.pystr(),
        barcodes: List[str] = None,
        parameters: List[Parameter] = None,
        **kwargs
    ):
        if barcodes is None:
            barcodes = [fake.pystr() for _ in range(3)]
        if parameters is None:
            parameters = [ParameterFactory() for _ in range(3)]

        super().__init__(
            vendor=vendor,
            barcodes=barcodes,
            parameters=parameters,
            **kwargs
        )
        self.name = name

    def get_values(self, **kwargs) -> dict:
        return super().get_values(name=self.name)
