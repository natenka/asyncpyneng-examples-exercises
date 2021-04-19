import asyncio
from datetime import datetime
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException
from async_timeout import timeout
import yaml

from ex06_async_iterator_telnet_ssh import CheckConnection, scan


class CheckConnectionPing(CheckConnection):
    def __init__(self, device_list):
        self.device_list = device_list
        self._current_device = 0

    async def _scan_device(self, device):
        reply = await asyncio.create_subprocess_shell(
            f"ping -c 3 -n {device}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await reply.communicate()
        output = (stdout + stderr).decode("utf-8")

        if reply.returncode == 0:
            return True, output
        else:
            return False, output


async def scan(devices, protocol):
    protocol_class_map = {
        "ssh": CheckConnection,
        "telnet": CheckConnection,
        "icmp": CheckConnectionPing,
    }
    ConnectionClass = protocol_class_map.get(protocol.lower())
    if ConnectionClass:
        check = ConnectionClass(devices)
        async for status, msg in check:
            if status:
                print(f"{datetime.now()} {protocol}. Подключение успешно: {msg}")
            else:
                print(f"{datetime.now()} {protocol}. Не удалось подключиться: {msg}")
    else:
        raise ValueError(f"Для протокола {protocol} нет соответствующего класса")


async def main():
    with open("devices_asyncssh.yaml") as f:
        devices_ssh = yaml.safe_load(f)
    with open("devices_asynctelnet.yaml") as f:
        devices_telnet = yaml.safe_load(f)
    ip_list = ["192.168.100.1", "8.8.8.8", "10.1.1.1"]
    await asyncio.gather(scan(devices_ssh, "SSH"), scan(devices_telnet, "Telnet"), scan(ip_list, "ICMP"))


if __name__ == "__main__":
    asyncio.run(main())
