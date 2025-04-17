import asyncio
from utils.config import get_mode
from app.uart_handler import uart_receiver
from app.lora_handler import init_lora, lora_receiver, lora_sender
from app.node import node_task
async def main():
    lora_rx_queue = asyncio.Queue()
    lora_tx_queue = asyncio.Queue()
    uart_rx_queue = asyncio.Queue()
    mode = get_mode()

    if mode == "node":        
        await asyncio.gather(
            uart_receiver(uart_rx_queue),
            lora_sender(lora_tx_queue),
            # lora_receiver(lora_rx_queue),
            node_task(uart_rx_queue, lora_tx_queue)
        )

    elif mode == "gateway":
        await asyncio.gather(
            # mqtt_task(lora_rx_queue),  # có thể thêm sau
            # lora_receiver(lora_rx_queue),
            # lora_sender(lora_tx_queue),
        )
    else:
        print(f"Can't recognize mode: {mode}")

if __name__ == "__main__":
    mode = get_mode()
    if mode in ["node", "gateway"]:
        init_lora()
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Stopped")
    else:
        print(f"Invalid mode: {mode}")
