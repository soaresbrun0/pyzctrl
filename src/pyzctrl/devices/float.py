"""Basic support for ZControl® devices equipped with floats."""

from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self

from .basic import ZControlDevice


@dataclass
class ZControlFloatDevice(ZControlDevice):
    """Defines a generic ZControl® device equipped with floats."""

    @dataclass(init = True)
    class Float:
        """Defines a ZControl® device float."""

        class Type(StrEnum):
            """Defines the type of the float."""

            OPERATIONAL = auto()
            HIGH_WATER = auto()

        class State(StrEnum):
            """Defines the state of a float."""

            ACTIVE = auto()
            INACTIVE = auto()
            MALFUNCTIONING = auto()
            MISSING = auto()
            NEVER_PRESENT = auto()

            @classmethod
            def from_attributes(
                cls,
                active: bool | None = None,
                malfunctioning: bool | None = None,
                missing: bool | None = None,
                never_present: bool | None = None,
            ) -> Self | None:
                """Returns a state based on the given attributes."""
                if never_present is True:
                    return cls.NEVER_PRESENT
                if missing is True:
                    return cls.MISSING
                if malfunctioning is True:
                    return cls.MALFUNCTIONING
                if active is True:
                    return cls.ACTIVE
                if active is False:
                    return cls.INACTIVE
                return None

        type: Type | None = None
        """The float's type."""

        state: State | None = None
        """The float's state."""

        activation_count: int | None = None
        """The float's total activation count."""

    floats: [Float] = None
    """The device's floats."""
