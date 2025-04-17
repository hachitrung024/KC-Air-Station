async def node_task(uart_rx_queue, lora_tx_queue):
    while True:
        uart_rx_data = await uart_rx_queue.get()
        # need some processing ?
        print(uart_rx_data)
        await lora_tx_queue.put(uart_rx_data) # directly foward