import pygatt
from binascii import hexlify

YOUR_DEVICE_ADDRESS = "E5:FB:01:09:F7:B4"
ADDRESS_TYPE = pygatt.BLEAddressType.random

adapter = pygatt.GATTToolBackend()

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))
"""
def write_handle(handle, value):
	val = [0x55, i, value]
	device.char_write_handle(handle, val, True)
"""
try:
    adapter.start()
    device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
    device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data)

    device.char_write_handle(0x000e, bytearray([0x55, 0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43, 0xAA]), True)

    device.char_write_handle(0x000c, bytearray([0x01, 0x00]), True)

    device.char_write_handle(0x000e, bytearray([0x55, 0x01, 0x01, 0xAA]), True)
    device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x03, 0xAA]), True)
    device.char_write_handle(0x000e, bytearray([0x55, 0x03, 0x06, 0xAA]), True)

finally:
    adapter.stop()
