import asyncio
import serial
from lora_e22 import LoRaE22, Configuration, print_configuration
from lora_e22_operation_constant import ResponseStatusCode
from lora_e22_constants import RssiEnableByte
from utils.config import get_lora_config

# Đọc config
lora_cfg = get_lora_config()

# Khởi tạo lora + lock
loraSerial = serial.Serial(
    lora_cfg.get("device", "/dev/serial0"),
    baudrate=int(lora_cfg.get("baudrate", 9600))
)
lora = LoRaE22(
    lora_cfg.get("model", "400T22D"),
    loraSerial,
    aux_pin=int(lora_cfg.get("aux_pin")),
    m0_pin=int(lora_cfg.get("m0_pin")),
    m1_pin=int(lora_cfg.get("m1_pin"))
)
lora_lock = asyncio.Lock()

def init_lora():
    code = lora.begin()
    print(f"Initialization: {ResponseStatusCode.get_description(code)}")

    config_model = lora_cfg.get("config_model", "400T22S")
    configuration_to_set = Configuration(config_model)
    configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

    code, confSetted = lora.set_configuration(configuration_to_set)
    print(f"Set configuration: {ResponseStatusCode.get_description(code)}")
    print_configuration(confSetted)


async def lora_receiver(lora_rx_queue):
    while True:
        async with lora_lock:
            if lora.available() > 0:
                code, value, rssi = lora.receive_message(rssi=True)
                print('RSSI: ', rssi)
                print(ResponseStatusCode.get_description(code))
                await lora_rx_queue.put(value)
                await asyncio.sleep(2)
        await asyncio.sleep(0.01)

async def lora_sender(lora_tx_queue):
    while True:
        msg = await lora_tx_queue.get()
        async with lora_lock:
            code = lora.send_transparent_message(msg)
            print("Send message: {}", ResponseStatusCode.get_description(code))
        await asyncio.sleep(0.01)
