from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Union
from xml.etree import ElementTree as ET

from yandex_market_language.exceptions import ValidationError


XMLElement = ET.Element
XMLSubElement = ET.SubElement


class AbstractModel(ABC):
    """
    Abstract model for creating child models.
    """
    @abstractmethod
    def create_dict(self, **kwargs) -> dict:
        """
        Must be inherited by each child class.
        Describes the logic for creating a dictionary with data from a model.
        """
        raise NotImplementedError

    @abstractmethod
    def create_xml(self, **kwargs) -> XMLElement:
        """
        Must be inherited by each child class.
        Describes the logic for creating a xml with data from a model.
        """
        raise NotImplementedError

    @staticmethod
    def from_xml(el: XMLElement) -> "AbstractModel":
        """
        Must be inherited by each child class.
        Describes the logic for creating a model from an xml element.
        """
        raise NotImplementedError

    def to_xml(self, root_el: XMLElement = None) -> XMLElement:
        """
        Calls the inherited method to create the element and appends it to the
        parent, if it was set.
        """
        el = self.create_xml()
        if root_el is not None:
            root_el.append(el)
        return el

    def to_dict(self, clean: bool = False) -> dict:
        """
        Calls the inherited method to create the dictionary and returns a
        clean dictionary if the parameter was set.
        """
        return self.clean_dict if clean else self.create_dict()

    @property
    def clean_dict(self) -> dict:
        """
        A helper property to get clean dictionary with data.
        """
        return dict(**{k: v for k, v in self.create_dict().items() if v})

    @staticmethod
    def _is_valid_int(
        value,
        attr: str,
        allow_none: bool = False,
        convert_to_str: bool = True
    ) -> Optional[Union[int, str]]:
        """
        A helper method for checking if a value is a valid number and returning
        a value if the check succeeds or raising an error.
        """
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
        """
        A helper method for checking if a value is a valid bool and returning
        a value if the check succeeds or raising an error.
        """
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
        """
        A helper method for checking if a value is a valid float and returning
        a value if the check succeeds or raising an error.
        """
        try:
            float(value)
            return str(value) if convert_to_str else value
        except (TypeError, ValueError):
            if value is None and allow_none:
                return None
            raise ValidationError("{a} must be a valid float".format(a=attr))

    @staticmethod
    def _str_to_bool(value: str) -> Optional[bool]:
        """
        Returns a boolean converted from a string or None.
        """
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
        """
        A helper method for checking if a value is a valid datetime and
        returning a value if the check succeeds or raising an error.
        """
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
