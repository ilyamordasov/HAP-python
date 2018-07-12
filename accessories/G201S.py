# An Accessory for a Smart Kettle.
from sensors.g201s import G201S as sensor
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_SENSOR

class G201S(Accessory):

	category = CATEGORY_SENSOR

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		serv_kettle = self.add_preload_service('SmartKettle')
		g201s = sensor()
		g201s.set_temperature(4)
		self.g201s = g201s

		self.char_on = serv_kettle.configure_char('On', setter_callback=self.turn_on)
		self.char_set = serv_kettle.configure_char('TargetTemperature', setter_callback=self.set_temperature)
		self.char_get = serv_kettle.configure_char('CurrentTemperature', setter_callback=self.get_temperature)
		#self.char_get = serv_kettle.get_characteristic('CurrentTemperature')

	def turn_on(self, value):
		if value:
			#print("Чайник включен")
			self.g201s.turn_on();
		else:
			#print("Чайник выключен")
			self.g201s.turn_off();

	def set_temperature(self, value):
		self.char_set.set_value(value);
		self.g201s.set_temperature(value)
		print(value)

	def get_temperature(self, value):
		val = self.g201s.get_temperature(value)
		print("Температура чайник {}°C".format(val))

	def turn_off(self, value):
		super().stop()
		print(">> Чайник выключен {}".format(value))