# -*- coding: utf-8 -*-

import pygatt
import sensors.sensorbase as sensorbase
from binascii import hexlify
import time

YOUR_DEVICE_ADDRESS = "E5:FB:01:09:F7:B4"
ADDRESS_TYPE = pygatt.BLEAddressType.random

adapter = pygatt.GATTToolBackend()
index = 0
cur_temp = 0

class G201S(sensorbase.SensorBase):
    def __init__(self):
        super(G201S, self).__init__(update_callback = self._update_sensor_data)
    
    def write_handle(self, device, handle, value, increment=True):
        global index
        val = []
        if handle == 0x000e:
            val.append(0x55)
            val.append(index)
            for i in value:
                val.append(i)
            val.append(0xAA)
        else:
            for i in value:
                val.append(i)
        
        val = bytearray(val)
        device.char_write_handle(handle, val, True)
        if increment: index += 1

    def turn_on(self):
        global index
        index = 0
        try:
            adapter.start()
            device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
            self.write_handle(device, 0x000e, [0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43], False)
            self.write_handle(device, 0x000c, [0x01, 0x00])
            self.write_handle(device, 0x000e, [0x01])
            self.write_handle(device, 0x000e, [0x05, 0x00, 0x00, int(hex(100), 16), 0x00])
            self.write_handle(device, 0x000e, [0x03])

        finally:
            adapter.stop()

    def turn_off(self):
        global index
        index = 0
        try:
            adapter.start()
            device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
            self.write_handle(device, 0x000e, [0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43], False)
            self.write_handle(device, 0x000c, [0x01, 0x00])
            self.write_handle(device, 0x000e, [0x01])
            self.write_handle(device, 0x000e, [0x04])
            cur_temp = self.get_temperature()
            print("Tried to switch off, returned {}".format(cur_temp))

        finally:
            adapter.stop()        

    def set_temperature(self, value):
        global index
        index = 0
        print("set temperature {}".format(value))
        # try:
        #     adapter.start()
        #     device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
        #     self.write_handle(device, 0x000e, [0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43], False)
        #     self.write_handle(device, 0x000c, [0x01, 0x00])
        #     self.write_handle(device, 0x000e, [0x01])
        #     self.write_handle(device, 0x000e, [0x05, 0x00, 0x00, int(hex(value), 16), 0x00])
        #     self.write_handle(device, 0x000e, [0x03])
        #     self.get_temperature()

        # finally:
        #     adapter.stop()
        if self.get_temperature() < value:
            self.turn_on()
            while True:
                if self.get_temperature() == value:
                    self.turn_off()
                    break
        else:
            print('{}°C'.format(self.get_temperature()))

    def get_temperature(self):
        global index
        index = 0
        try:
            adapter.start()
            device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
            self.write_handle(device, 0x000e, [0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43], False)
            self.write_handle(device, 0x000c, [0x01, 0x00])
            self.write_handle(device, 0x000e, [0x01])
            self.write_handle(device, 0x000e, [0x06])
            print("get temperature")
            value = device.char_read("6e400003-b5a3-f393-e0a9-e50e24dcca9e")
            value = hexlify(value)
            value = value[16:18]
            cur_temp = int(value, 16)
            print("Current temperature of kettle is {}".format(cur_temp))
            return cur_temp
        finally:
            adapter.stop()

    def _update_sensor_data(self):
        print("update")
        return cur_temp

if __name__ == '__main__':
    sensor = G201S(self)
