from pprint import pprint
import asyncio

import yaml
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException


async def send_show(device, command):
    print(f">>> connect {device['host']}")
    try:
        async with AsyncScrapli(**device) as conn:
            result = await conn.send_command(command)
            return result.result
    except ScrapliException as error:
        print(error, device["host"])


async def send_command_to_devices(devices, commands):
    tasks = [asyncio.create_task(send_show(device, commands)) for device in devices]
    result = [await task for task in tasks]
    return result


if __name__ == "__main__":
    with open("devices_async.yaml") as f:
        devices = yaml.safe_load(f)
    result = asyncio.run(send_command_to_devices(devices, "sh clock"))
    pprint(result, width=120)
