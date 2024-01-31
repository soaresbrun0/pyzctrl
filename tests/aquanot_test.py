"""Aquanot® test cases"""

import unittest

from src.pyzctrl.devices.aquanot import AquanotFit508
from src.pyzctrl.devices.battery import ZControlBatteryDevice
from src.pyzctrl.devices.float import ZControlFloatDevice
from src.pyzctrl.devices.pump import ZControlPumpDevice
from tests.utils import MockDeviceConnection, read_file


class AquanotFit508Tests(unittest.TestCase):
    """Test cases for the Aquanot® Fit 508 device."""

    def test_valid_status(self):
        """Tests parsing of a valid status.xml file."""
        device = AquanotFit508(
            MockDeviceConnection({"status.xml": read_file("valid_status.xml")})
        )
        device.update()
        self.assertEqual(device.device_id, "test_device")
        self.assertEqual(device.firmware_version, "1.40")
        self.assertEqual(device.system_uptime, 920172.1)
        self.assertEqual(device.is_self_test_running, False)

        # ZControlBatteryDevice
        self.assertEqual(device.is_primary_power_missing, False)
        backup_battery = device.batteries[
            ZControlBatteryDevice.Battery.Type.BACKUP
        ]
        self.assertEqual(backup_battery.voltage, 12.85)
        self.assertEqual(backup_battery.current, 0)
        self.assertEqual(backup_battery.is_charging, False)
        self.assertEqual(backup_battery.is_low, False)
        self.assertEqual(backup_battery.is_missing, False)
        self.assertEqual(backup_battery.is_bad, False)

        # ZControlFloatDevice
        operational_float: ZControlFloatDevice.Float = device.floats[
            ZControlFloatDevice.Float.Type.OPERATIONAL
        ]
        self.assertEqual(operational_float.is_active, False)
        self.assertEqual(operational_float.activation_count, 2)
        self.assertEqual(operational_float.is_malfunctioning, False)
        self.assertEqual(operational_float.is_missing, False)
        self.assertEqual(operational_float.never_present, False)

        high_water_float: ZControlFloatDevice.Float = device.floats[
            ZControlFloatDevice.Float.Type.HIGH_WATER
        ]
        self.assertEqual(high_water_float.is_active, False)
        self.assertEqual(high_water_float.activation_count, 0)
        self.assertEqual(high_water_float.is_malfunctioning, None)
        self.assertEqual(high_water_float.is_missing, False)
        self.assertEqual(high_water_float.never_present, False)

        # ZControlPumpDevice
        dc_pump = device.pumps[ZControlPumpDevice.Pump.Type.DC]
        self.assertEqual(dc_pump.current, 0)
        self.assertEqual(dc_pump.is_running, False)
        self.assertEqual(dc_pump.runtime, 78.8)
        self.assertEqual(dc_pump.airlock_detected, False)


if __name__ == "__main__":
    unittest.main()
