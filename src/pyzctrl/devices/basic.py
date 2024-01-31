"""Basic support for ZControl® devices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

import xmltodict

from ..utils import AttributeMap
from .connection import ZControlDeviceConnection


@dataclass
class ZControlDevice:
    """Defines a generic ZControl® device."""

    MANUFACTURER: ClassVar[str | None] = "Zoeller Pump Company"
    MODEL: ClassVar[str | None] = None

    connection: ZControlDeviceConnection
    """The device connection."""

    device_id: str | None = None
    """The device's unique identifier (e.g. serial number)."""

    serial_number: str | None = None
    """The device's serial number."""

    firmware_version: str | None = None
    """The device's firmware version."""

    system_uptime: float | None = None
    """The time in seconds since the device was booted."""

    is_self_test_running: bool | None = None
    """Whether or not the device is currently performing a self-test."""

    def __init__(self, connection: ZControlDeviceConnection) -> None:
        self.connection = connection

    def update(self) -> None:
        """Fetch ZControl® device status."""
        status = self.connection.fetch_resource("status.xml")
        attrs = AttributeMap(xmltodict.parse(status).get("response"))
        self._process_attrs(attrs)

    def _process_attrs(self, attrs: AttributeMap) -> None:
        """Process device attributes."""
