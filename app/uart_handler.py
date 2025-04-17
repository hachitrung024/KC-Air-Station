import asyncio
import serial

def setup_serial():
    return serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=0)

async def uart_task(queue):
    ser = setup_serial()

    while True:
        data = ser.readline()
        if data:
            decoded = data.decode().strip()
            await queue.put(decoded)
        await asyncio.sleep(0.01)
