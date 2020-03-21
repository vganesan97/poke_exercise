import requests
import json
import csv
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


executor = ThreadPoolExecutor(max_workers=18)
loop = asyncio.get_event_loop()

async def make_requests():
    futures = [loop.run_in_executor(executor, requests.get, "https://pokeapi.co/api/v2/ability/technician") for _ in range(18)]
    responses = await asyncio.gather(*futures)
    return responses
    
x = loop.run_until_complete(make_requests())
print(x)
data = x[0].json()

list = [3,4,5,6,7]
list.remove(4)
print(list)