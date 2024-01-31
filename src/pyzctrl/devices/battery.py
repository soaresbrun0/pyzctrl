"""Basic support for ZControl® devices equipped with batteries."""

from dataclasses import dataclass
from .basic import ZControlDevice


@dataclass
class ZControlBatteryDevice(ZControlDevice):
    """Defines a generic ZControl® device equipped with batteries."""

    @dataclass(init = True)
    class Battery:
        """Defines a battery."""

        voltage: float | None = None
        """The battery's voltage in volts."""

        current: float | None = None
        """The battery's current in amps."""

        is_charging: bool | None = None
        """Whether or not the battery is charging."""

        is_low: bool | None = None
        """Whether or not the battery is low."""

        is_missing: bool | None = None
        """Whether or not the battery is missing."""

        is_bad: bool | None = None
        """Whether or not the battery is bad."""

    batteries: [Battery] = None
    """The device's batteries."""

    is_on_battery_power: bool | None = None
    """Whether or not the device is currently being powered by a battery."""
