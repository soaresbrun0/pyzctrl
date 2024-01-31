"""Basic support for ZControl® devices equipped with pumps."""

from dataclasses import dataclass
from enum import StrEnum

from .basic import ZControlDevice


@dataclass
class ZControlPumpDevice(ZControlDevice):
    """Defines a generic ZControl® device with pumps."""

    @dataclass(init = True)
    class Pump:
        """Defines a ZControl® device pump."""

        class Type(StrEnum):
            """Defines pump types."""
        
            DC = "DC"

        type: Type | None = None
        """The pump's type."""

        current: float | None = None
        """The pump's current in amps."""

        is_running: bool | None = None
        """Whether or not the pump is running."""

        runtime: float | None = None
        """The pump's total runtime, in seconds."""

        airlock_detected: bool | None = None
        """Whether or not the pump has detected an airlock."""

    pumps: [Pump] = None
    """The device's pumps."""
