import serial
import time

from lora_e22 import LoRaE22, Configuration, print_configuration
from lora_e22_operation_constant import ResponseStatusCode

from lora_e22_constants import FixedTransmission, RssiEnableByte

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/serial0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, aux_pin=18, m0_pin=22, m1_pin=27)
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

configuration_to_set = Configuration('400T22S')
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}", ResponseStatusCode.get_description(code))
print_configuration(confSetted)
print("Waiting for messages...")
while True:
    if lora.available() > 0:
        # If the sender not set RSSI
        # code, value = lora.receive_message()
        # If the sender set RSSI
        code, value, rssi = lora.receive_message(rssi=True)
        print('RSSI: ', rssi)

        print(ResponseStatusCode.get_description(code))

        print(value)
        time.sleep(2)
