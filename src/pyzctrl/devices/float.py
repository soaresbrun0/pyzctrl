"""Basic support for ZControl® devices equipped with floats."""

from dataclasses import dataclass
from enum import StrEnum

from .basic import ZControlDevice


@dataclass
class ZControlFloatDevice(ZControlDevice):
    """Defines a generic ZControl® device equipped with floats."""

    @dataclass(init = True)
    class Float:
        """Defines a ZControl® device float."""

        class Type(StrEnum):
            """Defines the float types."""

            OPERATIONAL = "Operational"
            HIGH_WATER = "High Water"

        is_active: bool | None = None
        """Whether or not the float is active."""

        activation_count: int | None = None
        """The float's total activation count."""

        is_malfunctioning: bool | None = None
        """Whether or not the float is malfunctioning."""

        is_missing: bool | None = None
        """Whether or not the float is missing."""

        never_present: bool | None = None
        """Whether or not the float was never present."""

    floats: dict[Float.Type: Float] = None
    """The device's floats by type."""
