# -*- coding: utf-8 -*-

import pygatt
from binascii import hexlify, unhexlify
import time
import sys, struct

print(sys.argv[1])

YOUR_DEVICE_ADDRESS = "E5:FB:01:09:F7:B4"
ADDRESS_TYPE = pygatt.BLEAddressType.random

adapter = pygatt.GATTToolBackend()
index = 0
cur_temp = 0

def handle_data(handle, value):
    """
    handle -- integer, characteristic read handle the data was received on
    value -- bytearray, the data returned in the notification
    """
    print("Received data: %s" % hexlify(value))

def get_temperature():
	global index
	device.char_write_handle(0x000e, bytearray([0x55, index, 0x06, 0xAA]), True)
	value = device.char_read("6e400003-b5a3-f393-e0a9-e50e24dcca9e")
	value = hexlify(value)
	value = value[16:18]
	index += 1
	return int(value, 16)
	print('{}°C'.format(value))

try:
	adapter.start()
	device = adapter.connect(YOUR_DEVICE_ADDRESS, address_type=ADDRESS_TYPE)
	time.sleep(1)
	device.subscribe("6e400003-b5a3-f393-e0a9-e50e24dcca9e", callback=handle_data)
	device.char_write_handle(0x000e, bytearray([0x55, 0x00, 0xFF, 0xDF, 0x24, 0x0E, 0xC6, 0x94, 0xD1, 0x97, 0x43, 0xAA]), True)
	device.char_write_handle(0x000c, bytearray([0x01, 0x00]), True)
	device.char_write_handle(0x000e, bytearray([0x55, 0x01, 0x01, 0xAA]), True)

	if str(sys.argv[1]) == "start":	
		device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x03, 0xAA]), True)

	elif str(sys.argv[1]) == "stop":
		device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x04, 0xAA]), True)

	elif str(sys.argv[1]) == "get":
		device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x06, 0xAA]), True)
		value = device.char_read("6e400003-b5a3-f393-e0a9-e50e24dcca9e")
		value = hexlify(value)
		value = value[16:18]
		value = int(value, 16)
		print('{}°C'.format(value))

	elif str(sys.argv[1]) == "set":
		print(sys.argv[2])
		#device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x05, 0x00, 0x00, int(sys.argv[2]), 0x00, 0xAA]), True)
		device.char_write_handle(0x000e, bytearray([0x55, 0x02, 0x52, 0x00, 0xAA]), True)
		device.char_write_handle(0x000e, bytearray([0x55, 0x03, 0x35, int(sys.argv[2]), 0xAA]), True)
		index = 4
		if get_temperature() < int(sys.argv[2]):
			device.char_write_handle(0x000e, bytearray([0x55, index, 0x03, 0xAA]), True)
			while True:
				if int(sys.argv[2]) == get_temperature():
					device.char_write_handle(0x000e, bytearray([0x55, index, 0x04, 0xAA]), True)
					break
		else:
			print('{}°C'.format(get_temperature()))
		#device.char_write_handle(0x000e, bytearray([0x55, 0x03, 0x05, 0x00, 0x00, int(sys.argv[2]), 0x00, 0xAA]), True)

finally:
	adapter.stop()