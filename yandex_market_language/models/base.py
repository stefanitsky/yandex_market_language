from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Union
from xml.etree import ElementTree as ET

from yandex_market_language.exceptions import ValidationError

XMLElement = ET.Element
XMLSubElement = ET.SubElement


class BaseModel(ABC):
    @abstractmethod
    def create_dict(self, **kwargs) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_xml(self, **kwargs) -> XMLElement:
        raise NotImplementedError

    @property
    def clean_dict(self) -> dict:
        return dict(**{k: v for k, v in self.create_dict().items() if v})

    @staticmethod
    def _is_valid_int(
        value,
        attr: str,
        allow_none: bool = False,
        convert_to_str: bool = True
    ) -> Optional[Union[int, str]]:
        try:
            value = int(value)
            return str(value) if convert_to_str else value
        except (TypeError, ValueError):
            if value is None and allow_none:
                return None
            raise ValidationError("{a} must be a valid int".format(a=attr))

    @staticmethod
    def _is_valid_bool(
        value,
        attr: str,
        allow_none: bool = False
    ) -> Optional[str]:
        if value in ["true", "false"]:
            return value
        elif value is True:
            return "true"
        elif value is False:
            return "false"
        elif value is None and allow_none:
            return None
        else:
            raise ValidationError(
                "The {attr} parameter should be boolean. "
                "Got {t} instead.".format(attr=attr, t=type(value))
            )

    @staticmethod
    def _is_valid_float(
        value,
        attr: str,
        allow_none: bool = False,
        convert_to_str: bool = True
    ) -> Optional[Union[float, str]]:
        try:
            float(value)
            return str(value) if convert_to_str else value
        except (TypeError, ValueError):
            if value is None and allow_none:
                return None
            raise ValidationError("{a} must be a valid float".format(a=attr))

    @staticmethod
    def _str_to_bool(value) -> Optional[bool]:
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            return None

    @staticmethod
    def _is_valid_datetime(
        dt,
        dt_format,
        attr: str,
        allow_none: bool = False,
    ) -> Optional[Union[datetime, str]]:
        if isinstance(dt, datetime):
            return dt.strftime(dt_format)
        elif isinstance(dt, str):
            try:
                datetime.strptime(dt, dt_format)
            except ValueError as e:
                raise ValidationError(e)
            return dt
        elif dt is None and allow_none:
            return None
        else:
            raise ValidationError(
                "{a} must be a valid datetime".format(a=attr)
            )

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        el = self.create_xml()
        if root_el is not None:
            root_el.append(el)
        return el

    def to_dict(self, clean: bool = False) -> dict:
        return self.clean_dict if clean else self.create_dict()

    @staticmethod
    def from_xml(el: XMLElement) -> "BaseModel":
        raise NotImplementedError
