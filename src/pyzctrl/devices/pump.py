"""Basic support for ZControl® devices equipped with pumps."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .basic import ZControlDevice


@dataclass
class ZControlPumpDevice(ZControlDevice):
    """Defines a generic ZControl® device with pumps."""

    @dataclass(init = True)
    class Pump:
        """Defines a ZControl® device pump."""

        class Type(str, Enum):
            """Defines pump types."""
        
            DC = "DC"

        current: Optional[float] = None
        """The pump's current in amps."""

        is_running: Optional[bool] = None
        """Whether or not the pump is running."""

        runtime: Optional[float] = None
        """The pump's total runtime, in seconds."""

        airlock_detected: Optional[bool] = None
        """Whether or not the pump has detected an airlock."""

    pumps: dict[Pump.Type: Pump] = None
    """The device's pumps by type."""
