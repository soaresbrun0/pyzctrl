"""Basic support for ZControl® devices equipped with batteries."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .basic import ZControlDevice


@dataclass
class ZControlBatteryDevice(ZControlDevice):
    """Defines a generic ZControl® device equipped with batteries."""

    @dataclass(init = True)
    class Battery:
        """Defines a battery."""

        class Type(str, Enum):
            """Defines the battery types."""

            BACKUP = "Backup"

        voltage: Optional[float] = None
        """The battery's voltage in volts."""

        current: Optional[float] = None
        """The battery's current in amps."""

        is_charging: Optional[bool] = None
        """Whether or not the battery is charging."""

        is_low: Optional[bool] = None
        """Whether or not the battery is low."""

        is_missing: Optional[bool] = None
        """Whether or not the battery is missing."""

        is_bad: Optional[bool] = None
        """Whether or not the battery is bad."""

    batteries: dict[Battery.Type: Battery] = None
    """The device's batteries by type."""

    is_primary_power_missing: Optional[bool] = None
    """Whether or not the device's primary power source is missing."""
