from __future__ import annotations

import logging
import requests
import urllib.parse
import xmltodict

from enum import Enum
from pyzctrl import exceptions
from types import SimpleNamespace

DEFAULT_TIMEOUT = 10
_LOGGER = logging.getLogger(__name__)

class ZControlDevice(SimpleNamespace):
    """Support for fetching the status of ZControl® devices."""

    def __init__(
        self,
        host: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.host = host
        self.timeout = timeout
        self._process_attrs(_DeviceAttributes()) # set all attributes to None

    def update(self) -> None:
        """Fetch ZControl® device status."""
        status = self._fetch_resource('status.xml')
        dict = xmltodict.parse(status).get('response')
        self._process_attrs(_DeviceAttributes(dict))

    def _fetch_resource(self, resource: str) -> str:
        try:
            url = urllib.parse.urljoin(self.host, resource)
            _LOGGER.debug("Fetching %s", url)

            response = requests.get(url, timeout = self.timeout)
            response.raise_for_status()

            _LOGGER.debug("Successfully fetched %s: %s", url, response.text)
            return response.text

        except requests.exceptions.Timeout as ex:
            _LOGGER.error("Timed out while fetching %s", url)
            raise exceptions.ResourceFetchTimeoutError(self.host, resource) from ex

        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Failed to fetch resource %s; %s", url, ex)
            raise exceptions.ResourceFetchError(self.host, resource) from ex

    def _process_attrs(self, attrs: _DeviceAttributes) -> None:
        """Process device attributes."""


class AquanotFit508(ZControlDevice):
    """Support for fetching the status of Aquanot® Fit 508 devices."""

    class _Alarm(Enum):
        """Enum containing known AquanotFit® 508 Alarms"""

        PRIMARY_POWER_MISSING = 1 << 0
        BATTERY_MISSING = 1 << 1
        LOW_BATTERY_VOLTAGE = 1 << 2
        BATTERY_POLARITY = 1 << 3
        OPERATIONAL_FLOAT = 1 << 4
        HIGH_WATER_FLOAT = 1 << 5
        OPERATIONAL_FLOAT_MALFUNCTION = 1 << 6
        PUMP_LOW_CURRENT = 1 << 7
        PUMP_CYCLED = 1 << 8
        PUMP_LOCKED_ROTOR_CURRENT = 1 << 9
        HIGH_WATER_FLOAT_MISSING = 1 << 10
        BAD_BATTERY = 1 << 11
        OPERATIONAL_FLOAT_MISSING = 1 << 12
        PUMP_NO_CURRENT = 1 << 14

    def _process_attrs(self, attrs: _DeviceAttributes) -> None:
        self.device_id = attrs.get('deviceid')
        self.firmware_version = attrs.get('firm')
        self.system_uptime = attrs.get_float('nt', 0.1)
        self.is_battery_charging = attrs.get_bool('chargestate')
        self.battery_voltage = attrs.get_float('batteryv', 0.01)
        self.battery_current = attrs.get_float('chargei', 0.01)
        self.dc_pump_current = attrs.get_float('motori', 0.1)
        self.dc_pump_runtime = attrs.get_float('mrt', 0.1)
        self.is_dc_pump_running = attrs.get_bool('pump')
        self.is_dc_pump_in_airlock = attrs.get_bool('airllogic')
        self.is_primary_pump_missing = attrs.get_bool('prmissing')
        self.is_operational_float_active = attrs.get_bool('of')
        self.operational_float_activation_count = attrs.get_int('ofc')
        self.operational_float_never_present = attrs.get_bool('opnevpres')
        self.is_high_water_float_active = attrs.get_bool('hiwaterfloat')
        self.high_water_float_activation_count = attrs.get_int('hi')
        self.high_water_float_never_present = attrs.get_bool('hinevpres')
        self.is_self_test_running = attrs.get_bool_from_bitmask('action', 2)
        self.alarms = {a.name.lower(): attrs.get_bool_from_bitmask('alarms', a.value) for a in self._Alarm}

    def perform_self_test(self) -> None:
        """Performs self test."""
        self._fetch_resource('selftest.cgi')

    def silence_alarms(self) -> None:
        """Silences all alarms."""
        self._fetch_resource('silence.cgi')

    def acknowledge_faults(self) -> None:
        """Acknowledges all faults and resets the device."""
        self._fetch_resource('ackfaults.cgi')


class _DeviceAttributes(dict[str, str]):

    def get_bool(self, key: str) -> bool | None:
        val = self.get(key)
        if val == None:
            return None
        return val.lower() in ['1', 'true', 't', 'yes', 'y']

    def get_bool_from_bitmask(self, key: str, bitmask: int) -> bool | None:
        val = self.get_int(key)
        if val == None:
            return None
        return (val & bitmask) == bitmask

    def get_float(self, key: str, multiplier: float = 1) -> float | None:
        val = self.get(key)
        if val == None:
            return None
        try:
            return float(val) * multiplier
        except ValueError as ex:
            _LOGGER.error('Failed to convert %s to float', val)
            return None

    def get_int(self, key: str) -> float | None:
        val = self.get(key)
        if val == None:
            return None
        try:
            return int(val)
        except ValueError as ex:
            _LOGGER.error('Failed to convert %s to int', val)
            return None
