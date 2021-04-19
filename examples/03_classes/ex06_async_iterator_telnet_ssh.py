import asyncio
from datetime import datetime
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException
from async_timeout import timeout
import yaml


class CheckConnection:
    def __init__(self, device_list):
        self.device_list = device_list
        self._current_device = 0

    async def _scan_device(self, device):
        ip = device["host"]
        try:
            async with timeout(5):  # для asynctelnet
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


async def scan(devices, protocol):
    check = CheckConnection(devices)
    async for status, msg in check:
        if status:
            print(f"{datetime.now()} {protocol}. Подключение успешно: {msg}")
        else:
            print(f"{datetime.now()} {protocol}. Не удалось подключиться: {msg}")


async def main():
    with open("devices_asyncssh.yaml") as f:
        devices_ssh = yaml.safe_load(f)
    with open("devices_asynctelnet.yaml") as f:
        devices_telnet = yaml.safe_load(f)
    await asyncio.gather(scan(devices_ssh, "SSH"), scan(devices_telnet, "Telnet"))


if __name__ == "__main__":
    asyncio.run(main())
