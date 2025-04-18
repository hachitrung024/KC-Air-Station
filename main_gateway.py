import asyncio
from app.lora_handler import init_lora, lora_receiver, lora_sender
from app.gateway import gateway_task
from app.mqtt_publisher import mqtt_publisher, init_mqtt

async def main():
    lora_rx_queue = asyncio.Queue()
    lora_tx_queue = asyncio.Queue()
    # uart_rx_queue = asyncio.Queue()
    mqtt_publish_queue = asyncio.Queue()
    init_lora()
    init_mqtt()
    await asyncio.gather(
        # uart_receiver(uart_rx_queue),
        lora_sender(lora_tx_queue),
        lora_receiver(lora_rx_queue),
        gateway_task(lora_rx_queue, mqtt_publish_queue),
        mqtt_publisher(mqtt_publish_queue)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
