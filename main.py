import asyncio
from app.uart_handler import uart_receiver
from app.lora_handler import init_lora, lora_receiver, lora_sender
from app.node import node_task
async def main():
    # lora_rx_queue = asyncio.Queue()
    lora_tx_queue = asyncio.Queue()
    uart_rx_queue = asyncio.Queue()
    await asyncio.gather(
        uart_receiver(uart_rx_queue),
        lora_sender(lora_tx_queue),
        # lora_receiver(lora_rx_queue),
        node_task(uart_rx_queue, lora_tx_queue)
    )
if __name__ == "__main__":
    init_lora()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
