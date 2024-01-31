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
        device = AquanotFit508(MockDeviceConnection({
            "status.xml": read_file('valid_status.xml')
        }))
        device.update()
        self.assertEqual(device.device_id, "test_device")
        self.assertEqual(device.firmware_version, "1.40")
        self.assertEqual(device.system_uptime, 920172.1)
        self.assertEqual(device.is_on_battery_power, False)
        self.assertEqual(device.is_self_test_running, False)

        self.assertEqual(len(device.pumps), 1)
        pump: ZControlPumpDevice.Pump = device.pumps[0]
        self.assertEqual(pump.type, ZControlPumpDevice.Pump.Type.DC)
        self.assertEqual(pump.current, 0)
        self.assertEqual(pump.is_running, False)
        self.assertEqual(pump.runtime, 78.8)
        self.assertEqual(pump.airlock_detected, False)

        self.assertEqual(len(device.floats), 2)
        operational_float: ZControlFloatDevice.Float = device.floats[0]
        self.assertEqual(operational_float.type, ZControlFloatDevice.Float.Type.OPERATIONAL)
        self.assertEqual(operational_float.is_active, False)
        self.assertEqual(operational_float.activation_count, 2)
        self.assertEqual(operational_float.is_malfunctioning, False)
        self.assertEqual(operational_float.is_missing, False)
        self.assertEqual(operational_float.never_present, False)
        
        high_water_float: ZControlFloatDevice.Float = device.floats[1]
        self.assertEqual(high_water_float.type, ZControlFloatDevice.Float.Type.HIGH_WATER)
        self.assertEqual(operational_float.is_active, False)
        self.assertEqual(operational_float.activation_count, 2)
        self.assertEqual(operational_float.is_malfunctioning, False)
        self.assertEqual(operational_float.is_missing, False)
        self.assertEqual(operational_float.never_present, False)

        self.assertEqual(len(device.batteries), 1)
        battery: ZControlBatteryDevice.Battery = device.batteries[0]
        self.assertEqual(battery.voltage, 12.85)
        self.assertEqual(battery.current, 0)
        self.assertEqual(battery.is_charging, False)
        self.assertEqual(battery.is_low, False)
        self.assertEqual(battery.is_missing, False)
        self.assertEqual(battery.is_bad, False)


if __name__ == "__main__":
    unittest.main()
