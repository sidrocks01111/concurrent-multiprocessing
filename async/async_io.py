import asyncio
import time
import requests
import aiohttp


async def get_url_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main():
    urls = [
        'https://en.wikipedia.org/wiki/Music_genre',
        'https://en.wikipedia.org/wiki/Main_Page',
        'https://en.wikipedia.org/wiki/Cross_Road_Blues',
        'https://en.wikipedia.org/wiki/Robert_Johnson',
        'https://en.wikipedia.org/wiki/Blues'

    ]

    start_time = time.time()
    for url in urls:
        requests.get(url)

    end_time = time.time()

    print('requests took', end_time - start_time)
    
    start_t = time.time()
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_url_response(url)))
    
    await asyncio.gather(*tasks)
    end_t = time.time()
    print('Aync req took', end_t - start_t)

if __name__ == "__main__":
    asyncio.run(main())
