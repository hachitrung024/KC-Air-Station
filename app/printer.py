async def print_task(queue):
    while True:
        data = await queue.get()
        print(f"[ACM0]: {data}")