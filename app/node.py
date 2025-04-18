import json
import asyncio
async def node_task(uart_rx_queue, lora_tx_queue):
    while True:
        await asyncio.sleep(0.01)
        uart_rx_data = await uart_rx_queue.get()
        # need some processing ?
        print(f"{uart_rx_data}")
        try:
            data_part = uart_rx_data[13:]
            final_data = json.dumps(json.loads(data_part))
            print(f"Parse json sucess {final_data}")
            await lora_tx_queue.put(final_data)
        except:
            continue