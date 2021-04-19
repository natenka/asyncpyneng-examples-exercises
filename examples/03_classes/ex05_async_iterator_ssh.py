import asyncio
from datetime import datetime
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException
import yaml


class CheckConnection:
    def __init__(self, device_list):
        self.device_list = device_list
        self._current_device = 0

    async def _scan_device(self, device):
        ip = device["host"]
        try:
            async with AsyncScrapli(**device) as conn:
                prompt = await conn.get_prompt()
            return True, prompt
        except (ScrapliException, asyncio.exceptions.TimeoutError) as error:
            return False, f"{error} {ip}"

    async def __anext__(self):
        if self._current_device >= len(self.device_list):
            raise StopAsyncIteration
        device_params = self.device_list[self._current_device]
        scan_results = await self._scan_device(device_params)
        self._current_device += 1
        return scan_results

    def __aiter__(self):
        return self


async def ssh_scan(devices):
    check = CheckConnection(devices)
    async for status, msg in check:
        if status:
            print(f"{datetime.now()} SSH. Подключение успешно: {msg}")
        else:
            print(f"{datetime.now()} SSH. Не удалось подключиться: {msg}")


if __name__ == "__main__":
    with open("devices_asyncssh.yaml") as f:
        devices = yaml.safe_load(f)
    asyncio.run(ssh_scan(devices))

