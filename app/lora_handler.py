import asyncio
import serial
from lora_e22 import LoRaE22, print_configuration, Configuration
from lora_e22_constants import OperatingFrequency, FixedTransmission, TransmissionPower, \
    AirDataRate, UARTParity, UARTBaudRate, RssiAmbientNoiseEnable, SubPacketSetting, WorPeriod, \
    LbtEnableByte, RssiEnableByte, TransmissionPower22, WorTransceiverControl, RepeaterModeEnableByte
from lora_e22_operation_constant import ResponseStatusCode
from utils.config import get_lora_config, get_target_config
lora_cfg = get_lora_config()
target_cfg = get_target_config()

loraSerial = serial.Serial(
    lora_cfg.get("device", "/dev/serial0"),
    baudrate=int(lora_cfg.get("baudrate", 9600))
)
lora = LoRaE22(
    lora_cfg.get("model", "400T22S"),
    loraSerial,
    aux_pin=int(lora_cfg.get("aux_pin")),
    m0_pin=int(lora_cfg.get("m0_pin")),
    m1_pin=int(lora_cfg.get("m1_pin"))
)
lora_lock = asyncio.Lock()

async def lora_receiver(lora_rx_queue):
    while True:
        async with lora_lock:
            if lora.available() > 0:
                code, value, rssi = lora.receive_message(rssi=True)
                print('RSSI: ', rssi)
                print(ResponseStatusCode.get_description(code))
                await lora_rx_queue.put(value)
                await asyncio.sleep(2)
        await asyncio.sleep(0.1)

async def lora_sender(lora_tx_queue):
    target_add_h = int(target_cfg.get("add_h","0xff"), 16)
    target_add_l = int(target_cfg.get("add_l","0xff"), 16)
    target_chan= int(target_cfg.get("chan", 23))
    while True:
        msg = await lora_tx_queue.get()
        async with lora_lock:
            code = lora.send_fixed_message(target_add_h, target_add_l, target_chan, msg)
            print("Send message: {}", ResponseStatusCode.get_description(code))
        await asyncio.sleep(0.1)

def init_lora():
    code = lora.begin()
    print(f"Initialization: {ResponseStatusCode.get_description(code)}")

    config_model = lora_cfg.get("config_model", "400T22S")
    configuration_to_set = Configuration(config_model)
    configuration_to_set.ADDH = int(lora_cfg.get("add_h", "0x00"), 16 )
    configuration_to_set.ADDL = int(lora_cfg.get("add_l", "0x00"), 16 )
    configuration_to_set.CHAN = int(lora_cfg.get("chan", 23))

    configuration_to_set.NETID = int(lora_cfg.get("net_id", 0))

    configuration_to_set.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_100_96
    configuration_to_set.SPED.uartParity = UARTParity.MODE_00_8N1
    configuration_to_set.SPED.uartBaudRate = UARTBaudRate.BPS_9600

    configuration_to_set.OPTION.subPacketSetting = SubPacketSetting.SPS_240_00
    configuration_to_set.OPTION.transmissionPower = TransmissionPower22.POWER_22
    configuration_to_set.OPTION.RSSIAmbientNoise = RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_ENABLED

    configuration_to_set.TRANSMISSION_MODE.WORTransceiverControl = WorTransceiverControl.WOR_TRANSMITTER
    configuration_to_set.TRANSMISSION_MODE.enableLBT = LbtEnableByte.LBT_DISABLED
    configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
    configuration_to_set.TRANSMISSION_MODE.enableRepeater = RepeaterModeEnableByte.REPEATER_DISABLED
    configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
    configuration_to_set.TRANSMISSION_MODE.WORPeriod = WorPeriod.WOR_1500_010

    configuration_to_set.CRYPT.CRYPT_H = int(lora_cfg.get("crypt_h", "0x00"), 16)
    configuration_to_set.CRYPT.CRYPT_L = int(lora_cfg.get("crypt_l", "0x00"), 16)
    code, confSetted = lora.set_configuration(configuration_to_set)
    print(f"Set configuration: {ResponseStatusCode.get_description(code)}")
    print_configuration(confSetted)
