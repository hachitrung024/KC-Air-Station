import json
async def node_task(uart_rx_queue, lora_tx_queue):
    while True:
        uart_rx_data = await uart_rx_queue.get()
        # need some processing ?
        print(f"Receive from core 2 : {uart_rx_data}")
        try:
            data_part = uart_rx_data[13:]
            final_data = json.loads(data_part)
            print(f"Parse json sucess {final_data}")
            await lora_tx_queue.put(final_data) # directly foward
        except:
            continue