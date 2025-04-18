import asyncio
import json

def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False

async def gateway_task(lora_rx_queue, mqtt_publish_queue):
    while True:
        data = await lora_rx_queue.get()
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        if is_valid_json(data):
            await mqtt_publish_queue.put(data)
        await asyncio.sleep(0.1)
