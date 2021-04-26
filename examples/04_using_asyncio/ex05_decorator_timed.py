import asyncio
from datetime import datetime
from functools import wraps
import yaml
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException


def timecode(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = await function(*args, **kwargs)
        print(">>> Функция выполнялась:", datetime.now() - start_time)
        return result

    return wrapper


@timecode
async def send_show(device, command):
    try:
        async with AsyncScrapli(**device) as conn:
            result = await conn.send_command(command)
            await asyncio.sleep(2)
            return result.result
    except ScrapliException as error:
        print(error, device["host"])


if __name__ == "__main__":
    with open("devices_async.yaml") as f:
        devices = yaml.safe_load(f)
        r1 = devices[0]
    result = asyncio.run(send_show(r1, "sh clock"))
    print(result)
