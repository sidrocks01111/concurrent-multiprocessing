import asyncio
import time


async def async_sleep(x):
    print('Before Sleep', x)
    n = max(2, x)
    for i in range(1, n):
        yield i
        await asyncio.sleep(i)
    print('After SLeep', x)
    
    
async def print_hello():
    print('Hello')


async def main():
    start = time.time()
    # task = asyncio.create_task(async_sleep(2))
    # await async_sleep(3)
    # await print_hello()
    # await task
    # try:
    #     await asyncio.gather(asyncio.wait_for(async_sleep(4), 5), async_sleep(2), print_hello())
    # except asyncio.TimeoutError:
    #     print('Timeout error')
    # this doesnt run the loop concurrently but this just gives control back to event loop to run other coorutines
    async for k in async_sleep(5):
        print(k)
    print('total time', time.time() - start)
if __name__ == "__main__":
    asyncio.run(main())