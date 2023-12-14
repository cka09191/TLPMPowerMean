"""
PowerMeterManager
author : Gyeongjun Chae (ck09137@gmail.com)
"""

from ctypes import c_uint32, byref, create_string_buffer, c_int, c_char_p, c_bool, c_double
import numpy as np
from TLPM import TLPM
import time


class Powermeter:
    def __init__(self):
        self.tlPM = TLPM()
        self.device_count = c_uint32()
        self.tlPM.findRsrc(byref(self.device_count))
        print("Devices found:", self.device_count.value)
        self.resource_name = create_string_buffer(1024)

    def __enter__(self):
        if self.device_count.value > 0:
            self.tlPM.getRsrcName(c_int(0), self.resource_name)
            print("Connecting to:", c_char_p(self.resource_name.raw).value)
            self.tlPM.open(self.resource_name, c_bool(True), c_bool(True))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.tlPM.close()

    def _set_wavelength(self, wavelength):
        self.tlPM.setWavelength(wavelength=c_double(wavelength))

    def _measure_power(self):
        power = c_double()
        self.tlPM.measPower(byref(power))
        return power.value

    def mean(self, second: float = 2, reps: int = 10, wavelength: float = 780) -> float:
        """
        Measure the power multiple times over a total time duration, with an intentional delay between each measurement.
    
        :param second: Total time duration for all measurements.
        :param reps: Number of measurements to take.
        :param wavelength: Wavelength to set for the measurements.
        :return: The mean of the power measurements.
        """
        self._set_wavelength(wavelength)
        power_measurements = []
        for _ in range(reps):
            power_measurements.append(self._measure_power())
            time.sleep(second / reps)
        return np.mean(power_measurements)


    def measure(self, wavelength=780):
        """
        Measure the power.
    
        :param wavelength: Wavelength to set for the measurement.
        :return: The power measurement
        """
        self._set_wavelength(wavelength)
        return self._measure_power()
