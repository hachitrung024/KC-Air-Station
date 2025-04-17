import asyncio
from uart_handler import uart_task
from printer import print_task

async def main():
    queue = asyncio.Queue()
    
    await asyncio.gather(
        uart_task(queue),
        print_task(queue)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
