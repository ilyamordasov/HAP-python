import pygatt
import sensors.sensorbase as sensorbase
from binascii import hexlify

YOUR_DEVICE_ADDRESS = "E5:FB:01:09:F7:B4"
ADDRESS_TYPE = pygatt.BLEAddressType.random

adapter = pygatt.GATTToolBackend()
index = 0

class G201S(sensorbase.SensorBase):
    def __init__(self):
        super(G201S, self).__init__(update_callback = self._update_sensor_data)

    
    def handle_data(handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        print("Received data: %s" % hexlify(value))

    
    def write_handle(self, device, handle, value, increment=True):
        global index
        # if handle == 0x000e:
        #     val = [0x55, bytes(index), value, 0xAA]
        # else:
        #     val = [bytes(index), value]
        
        # device.char_write_handle(handle, val, True)
        # if increment: index += 1
        
        device.char_write_handle(0x000e, bytearray([0x55, 0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43, 0xAA]))
        device.char_write_handle(0x000c, bytearray([0x01, 0x00]))
        device.char_write_handle(0x000e, bytearray([0x55, 0x01, 0x01, 0xAA]))
        device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x03, 0xAA]))
        print(val)

    def turn_on(self):
        try:
            adapter.start()
            device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
            #device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=self.handle_data)

            # self.write_handle(device, 0x000e, bytearray([0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43]), False)
            # self.write_handle(device, 0x000c, bytearray([0x01, 0x00]))
            # self.write_handle(device, 0x000e, bytearray([0x01]))
            # self.write_handle(device, 0x000e, bytearray([0x03]))
            device.char_write_handle(0x000e, bytearray([0x55, 0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43, 0xAA]))
            device.char_write_handle(0x000c, bytearray([0x01, 0x00]))
            device.char_write_handle(0x000e, bytearray([0x55, 0x01, 0x01, 0xAA]))
            device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x03, 0xAA]))

        finally:
            adapter.stop()

    def turn_off(self):
        try:
            adapter.start()
            device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
            #device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=self.handle_data)

            # self.write_handle(device, 0x000e, bytearray([0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43]), False)
            # self.write_handle(device, 0x000c, bytearray([0x01, 0x00]))
            # self.write_handle(device, 0x000e, bytearray([0x01]))
            # self.write_handle(device, 0x000e, bytearray([0x04]))
            
            device.char_write_handle(0x000e, bytearray([0x55, 0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43, 0xAA]))
            device.char_write_handle(0x000c, bytearray([0x01, 0x00]))
            device.char_write_handle(0x000e, bytearray([0x55, 0x01, 0x01, 0xAA]))
            device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x04, 0xAA]))

        finally:
            adapter.stop()        

    def set_temperature(self, value):
        print("set temperature {}".format(value))
        # try:
        #     adapter.start()
        #     device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
        #     device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data)

        #     write_handle(0x000e, bytearray([0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43]), False)
        #     write_handle(0x000c, bytearray([0x01, 0x00]))
        #     write_handle(0x000e, bytearray([0x01]))
        #     write_handle(0x000e, bytearray([0x06]))

        # finally:
        #     adapter.stop() 

    def _update_sensor_data(self):
        print("update")

if __name__ == '__main__':
    sensor = G201S(self)
