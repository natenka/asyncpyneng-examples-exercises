import asyncio
from pprint import pprint
from scrapli import AsyncScrapli
from scrapli.exceptions import ScrapliException


class CheckSSH:
    def __init__(self, device_list, common_ssh_params):
        self.device_list = device_list
        self.common_ssh_params = common_ssh_params

    async def scan(self):
        results = {"success": {}, "fail": {}}
        for ip in self.device_list:
            self.common_ssh_params["host"] = ip
            try:
                async with AsyncScrapli(**self.common_ssh_params) as conn:
                    prompt = await conn.get_prompt()
                    results["success"][ip] = prompt
            except ScrapliException as error:
                results["fail"][ip] = error
        return results


async def main():
    params = {
        "auth_username": "cisco",
        "auth_password": "cisco",
        "auth_secondary": "cisco",
        "auth_strict_key": False,
        "timeout_socket": 5,  # timeout for establishing socket/initial connection in seconds
        "timeout_transport": 10,  # timeout for ssh|telnet transport in seconds
        "platform": "cisco_iosxe",
        "transport": "asyncssh",
    }

    devices = ["192.168.100.1", "192.168.100.2", "192.168.100.3", "192.168.100.15"]
    check = CheckSSH(devices, params)
    results = await check.scan()
    pprint(results)


if __name__ == "__main__":
    asyncio.run(main())
