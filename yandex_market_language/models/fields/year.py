from typing import Optional


class YearField:
    _year = None

    @property
    def year(self) -> Optional[int]:
        return int(self._year) if self._year else None

    @year.setter
    def year(self, value):
        self._year = self._is_valid_int(value, "year", True)
