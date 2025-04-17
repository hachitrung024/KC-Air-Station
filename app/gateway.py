async def gateway_task(lora_rx_queue):
    while True:
        lora_rx_data = await lora_rx_queue.get()
        # need some processing ?
        print(lora_rx_data)
        # await lora_tx_queue.put(uart_rx_data) # directly foward