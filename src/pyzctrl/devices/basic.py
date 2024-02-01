"""Basic support for ZControl® devices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Optional

import xmltodict

from ..utils import AttributeMap
from .connection import ZControlDeviceConnection


@dataclass
class ZControlDevice:
    """Defines a generic ZControl® device."""

    MANUFACTURER: ClassVar[Optional[str]] = "Zoeller Pump Company"
    MODEL: ClassVar[Optional[str]] = None

    connection: ZControlDeviceConnection
    """The device connection."""

    device_id: Optional[str] = None
    """The device's unique identifier (e.g. serial number)."""

    serial_number: Optional[str] = None
    """The device's serial number."""

    firmware_version: Optional[str] = None
    """The device's firmware version."""

    system_uptime: Optional[float] = None
    """The time in seconds since the device was booted."""

    is_self_test_running: Optional[bool] = None
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
