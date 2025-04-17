import asyncio
import serial
from utils.config import get_uart_config

def setup_serial():
    uart_cfg = get_uart_config()
    return serial.Serial(
        uart_cfg.get("port", "/dev/ttyACM0"),
        baudrate=int(uart_cfg.get("baudrate", 9600)),
        timeout=float(uart_cfg.get("timeout", 0))
    )

async def uart_receiver(uart_rx_queue):
    ser = setup_serial()

    while True:
        data = ser.readline()
        if data:
            decoded = data.decode().strip()
            await uart_rx_queue.put(decoded)
        await asyncio.sleep(0.01)
