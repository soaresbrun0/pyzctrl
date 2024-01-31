"""Support for Aquanot® devices."""

from dataclasses import dataclass
from enum import IntEnum, IntFlag, StrEnum

from .battery import ZControlBatteryDevice
from .float import ZControlFloatDevice
from .pump import ZControlPumpDevice
from ..utils import AttributeMap


MANUFACTURER = "Zoeller Pump Company"
MODEL = "Aquanot® Fit 508"


@dataclass
class AquanotFit508(ZControlBatteryDevice, ZControlFloatDevice, ZControlPumpDevice):
    """Support for fetching the status of Aquanot® Fit 508 devices."""

    def _process_attrs(self, attrs: AttributeMap) -> None:
        # ZControlDevice
        self.device_id = attrs.get(self._Attribute.DEVICE_ID)
        self.serial_number = self.device_id
        self.manufacturer = MANUFACTURER
        self.model = MODEL
        self.firmware_version = attrs.get(self._Attribute.FIRMWARE_VERSION)
        self.system_uptime = attrs.get_float(self._Attribute.SYSTEM_UPTIME, 0.1)
        self.is_self_test_running = attrs.get_bool_from_bitmask(
            self._Attribute.ACTION, self._Action.SELF_TEST_RUNNING
        )

        # ZControlBatteryDevice
        self.batteries = {
            self.Battery.Type.BACKUP: self.Battery(
                voltage = attrs.get_float(self._Attribute.BATTERY_VOLTAGE, 0.01),
                current = attrs.get_float(self._Attribute.BATTERY_CURRENT, 0.01),
                is_charging = attrs.get_bool(self._Attribute.BATTERY_IS_CHARGING),
                is_low = attrs.get_bool_from_bitmask(
                    self._Attribute.ALARMS, self._Alarm.LOW_BATTERY_VOLTAGE
                ),
                is_missing = attrs.get_bool_from_bitmask(
                    self._Attribute.ALARMS, self._Alarm.BATTERY_MISSING
                ),
                is_bad = attrs.get_bool_from_bitmask(
                    self._Attribute.ALARMS, self._Alarm.BATTERY_BAD
                ),
            ),
        }
        self.is_primary_power_missing = attrs.get_bool_from_bitmask(
            self._Attribute.ALARMS, self._Alarm.PRIMARY_POWER_MISSING
        )
        
        # ZControlFloatDevice
        self.floats = {
            self.Float.Type.OPERATIONAL: self.Float(
                is_active = attrs.get_bool(self._Attribute.OPERATIONAL_FLOAT_IS_ACTIVE),
                activation_count = attrs.get_int(
                    self._Attribute.OPERATIONAL_FLOAT_ACTIVATION_COUNT
                ),
                is_malfunctioning = attrs.get_bool_from_bitmask(
                    self._Attribute.ALARMS, self._Alarm.OPERATIONAL_FLOAT_MALFUNCTION
                ),
                is_missing = attrs.get_bool_from_bitmask(
                    self._Attribute.ALARMS, self._Alarm.OPERATIONAL_FLOAT_MISSING
                ),
                never_present = attrs.get_bool(self._Attribute.OPERATIONAL_FLOAT_NEVER_PRESENT),
            ),
            self.Float.Type.HIGH_WATER: self.Float(
                is_active = attrs.get_bool(self._Attribute.HIGH_WATER_FLOAT_IS_ACTIVE),
                activation_count = attrs.get_int(self._Attribute.HIGH_WATER_FLOAT_ACTIVATION_COUNT),
                is_missing = attrs.get_bool_from_bitmask(
                    self._Attribute.ALARMS, self._Alarm.HIGH_WATER_FLOAT_MISSING
                ),
                never_present = attrs.get_bool(self._Attribute.HIGH_WATER_FLOAT_NEVER_PRESENT),
            ),
        }

        # ZControlPumpDevice
        self.pumps = {
            self.Pump.Type.DC: self.Pump(
                current = attrs.get_float(self._Attribute.DC_PUMP_CURRENT, 0.1),
                runtime = attrs.get_float(self._Attribute.DC_PUMP_RUNTIME, 0.1),
                is_running = attrs.get_bool(self._Attribute.DC_PUMP_IS_RUNNING),
                airlock_detected = attrs.get_bool(self._Attribute.DC_PUMP_AIRLOCK_DETECTED),
            ),
        }

    def perform_self_test(self) -> None:
        """Performs self test."""
        self.connection.fetch_resource("selftest.cgi")

    def silence_alarms(self) -> None:
        """Silences all alarms."""
        self.connection.fetch_resource("silence.cgi")

    def acknowledge_faults(self) -> None:
        """Acknowledges all faults and resets the device."""
        self.connection.fetch_resource("ackfaults.cgi")

    class _Attribute(StrEnum):

        DEVICE_ID = "deviceid"
        FIRMWARE_VERSION = "firm"
        SYSTEM_UPTIME = "nt"

        DC_PUMP_CURRENT = "motori"
        DC_PUMP_RUNTIME = "mrt"
        DC_PUMP_IS_RUNNING = "pump"
        DC_PUMP_AIRLOCK_DETECTED = "airllogic"

        OPERATIONAL_FLOAT_IS_ACTIVE = "of"
        OPERATIONAL_FLOAT_ACTIVATION_COUNT = "ofc"
        OPERATIONAL_FLOAT_NEVER_PRESENT = "opnevpres"

        HIGH_WATER_FLOAT_IS_ACTIVE = "hiwaterfloat"
        HIGH_WATER_FLOAT_ACTIVATION_COUNT = "hi"
        HIGH_WATER_FLOAT_NEVER_PRESENT = "hinevpres"

        BATTERY_VOLTAGE = "batteryv"
        BATTERY_CURRENT = "chargei"
        BATTERY_IS_CHARGING = "chargestate"

        ACTION = "action"
        ALARMS = "alarms"

    class _Action(IntEnum):

        DC_PUMP_RUNNING = 1
        SELF_TEST_RUNNING = 2

    class _Alarm(IntFlag):

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
        BATTERY_BAD = 1 << 11
        OPERATIONAL_FLOAT_MISSING = 1 << 12
        PUMP_NO_CURRENT = 1 << 14
