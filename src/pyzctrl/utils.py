"""General utilities to support ZControl® devices."""

from enum import IntFlag, StrEnum
import logging

_LOGGER = logging.getLogger(__name__)

class AttributeMap(dict[str, str]):
    """Defines a map of key/value pairs representing attributes."""

    def get(self, attr: str | StrEnum) -> str | None:
        """Returns the string value for the given attribute."""
        if isinstance(attr, str):
            return super().get(attr)
        if isinstance(attr, StrEnum):
            return super().get(attr.value)
        return None

    def get_bool(self, attr: str | StrEnum) -> bool | None:
        """Returns the bool value for the given attribute."""
        val = self.get(attr)
        if val is None:
            return None
        return val.lower() in ["1", "true", "t", "yes", "y"]

    def get_bool_from_bitmask(self, attr: str, bitmask: int | IntFlag) -> bool | None:
        """Returns the bool value for the given bitmask attribute."""
        val = self.get_int(attr)
        if val is None:
            return None
        if isinstance(bitmask, IntFlag):
            bitmask = bitmask.value
        return (val & bitmask) == bitmask

    def get_int(self, attr: str) -> int | None:
        """Returns the int value for the given attribute."""
        val = self.get(attr)
        if val is None:
            return None
        try:
            return int(val)
        except ValueError:
            _LOGGER.error("Failed to convert attribute %s (%s) to int.", attr, val)
            return None

    def get_float(self, attr: str, multiplier: float = 1, precision: int = 2) -> float | None:
        """Returns the float value for the given attribute."""
        val = self.get(attr)
        if val is None:
            return None
        try:
            return round(float(val) * multiplier, precision)
        except ValueError:
            _LOGGER.error("Failed to convert attribute %s (%s) to float.", attr, val)
            return None
