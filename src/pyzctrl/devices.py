"""Support for fetching the status of ZControl® devices."""
from __future__ import annotations

import logging
import requests
import urllib.parse
import xmltodict

from enum import Enum

DEFAULT_TIMEOUT = 10
_LOGGER = logging.getLogger(__name__)

class ZControlDevice:

    def __init__(
        self,
        host: str,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.host = host
        self.timeout = timeout
        self._attrs: dict[str, str] | None = None

    def _get_resource(self, resource: str) -> str:
        try:
            _LOGGER.debug("Fetching '%s'", resource)
            url = urllib.parse.urljoin(self.host, resource)
            response = requests.get(url, timeout = self.timeout)
            response.raise_for_status()

            _LOGGER.debug("Successfully fetched '%s': %s", response.text)
            return response.text

        except requests.exceptions.Timeout:
            _LOGGER.error("Timed out while fetching '%s'", resource)
            raise

        except requests.exceptions.RequestException as ex:
            _LOGGER.error("Failed to fetch resource %s", resource, ex)
            raise

    def update(self) -> None:
        """Fetch ZControl® device status."""
        status = self._get_resource('status.xml')
        self._attrs = xmltodict.parse(status).get('response')

    def _get_str_attr(self, key: str) -> str | None:
        if self._attrs == None:
            self.update()
        return self._attrs.get(key) if self._attrs != None else None

    def _get_bool_attr(self, key: str) -> bool | None:
        str = self._get_str_attr(key)
        if str == None:
            return None
        return str.lower() in ['1', 'true', 't', 'yes', 'y']

    def _get_float_attr(self, key: str, multiplier: float = 1) -> float | None:
        str = self._get_str_attr(key)
        if str == None:
            return None
        try:
            return float(str) * multiplier
        except ValueError as ex:
            _LOGGER.error('Failed to convert %s to float', str)
            return None

    def _get_int_attr(self, key: str) -> float | None:
        str = self._get_str_attr(key)
        if str == None:
            return None
        try:
            return int(str)
        except ValueError as ex:
            _LOGGER.error('Failed to convert %s to int', str)
            return None

    @property
    def device_id(self) -> str | None:
        """The device identifier."""
        return self._get_str_attr('deviceid')

    @property
    def firmware_version(self) -> str | None:
        """The firmware version."""
        return self._get_str_attr('firm')

    @property
    def system_uptime(self) -> float | None:
        """The system uptime (s)."""
        return self._get_float_attr('nt', 0.1)


class AquanotFit508(ZControlDevice):

    @property
    def is_battery_charging(self) -> bool | None:
        """Whether or not the battery is charging."""
        return self._get_bool_attr('chargestate')

    @property
    def battery_voltage(self) -> float | None:
        """The battery voltage (V)."""
        return self._get_float_attr('batteryv', 0.01)

    @property
    def battery_current(self) -> float | None:
        """The battery current (A)."""
        return self._get_float_attr('chargei', 0.01)

    @property
    def dc_pump_current(self) -> float | None:
        """The DC pump current (A)."""
        return self._get_float_attr('motori', 0.1)

    @property
    def dc_pump_runtime(self) -> float | None:
        """The DC pump runtime (s)."""
        return self._get_float_attr('mrt', 0.1)

    @property
    def is_dc_pump_running(self) -> bool | None:
        """Whether or not the DC pump is running."""
        return self._get_bool_attr('pump')

    @property
    def is_dc_pump_in_airlock(self) -> bool | None:
        """Whether or not the DC pump is in airlock."""
        return self._get_bool_attr('airllogic')

    @property
    def is_primary_pump_missing(self) -> bool | None:
        """Whether or not the primary pump is missing."""
        return self._get_bool_attr('prmissing')

    @property
    def is_operational_float_active(self) -> bool | None:
        """Whether or not the operational float is active."""
        return self._get_bool_attr('of')

    @property
    def operational_float_activation_count(self) -> int | None:
        """The total number of times the operational float was activated."""
        return self._get_int_attr('ofc')

    @property
    def operational_float_never_present(self) -> bool | None:
        """Whether or not the operational float was never present."""
        return self._get_bool_attr('opnevpres')

    @property
    def is_high_water_float_active(self) -> bool | None:
        """Whether or not the high water float is active."""
        return self._get_bool_attr('hiwaterfloat')

    @property
    def high_water_float_activation_count(self) -> int | None:
        """The total number of times the high water float was activated."""
        return self._get_int_attr('hi')

    @property
    def high_water_float_never_present(self) -> bool | None:
        """Whether or not the high water float was never present."""
        return self._get_bool_attr('hinevpres')

    @property
    def is_self_test_running(self) -> bool | None:
        """Whether or not the system is performing a self-test."""
        action = self._get_int_attr('action')
        if action == None:
            return None
        return (action & 2) != 0

    def perform_self_test(self): None
        """Performs a self-test."""
        self._get_resource('selftest.cgi')

    """Alarms"""
    class Alarm(Enum):

        primary_power_missing = 1 << 0
        battery_missing = 1 << 1
        low_battery_voltage = 1 << 2
        battery_polarity = 1 << 3
        operational_float = 1 << 4
        high_water_float = 1 << 5
        operational_float_malfunction = 1 << 6
        pump_low_current = 1 << 7
        pump_cycled = 1 << 8
        pump_locked_rotor_current = 1 << 9
        high_water_float_missing = 1 << 10
        bad_battery = 1 << 11
        operational_float_missing = 1 << 12
        pump_no_current = 1 << 14

    def is_alarm_active(self, alarm: Alarm) -> bool | None:
        alarms = self._get_int_attr('alarms')
        if alarms == None:
            return None
        return (alarms & alarm.value) == alarm.value

    @property
    def has_active_alarms(self) -> bool | None:
        alarms = self._get_int_attr('alarms')
        if alarms == None:
            return None
        return alarms != 0

    def silence_alarms(): None
        self._get_resource('silence.cgi')

    def acknowledge_faults(): None
        self._get_resource('ackfaults.cgi')
