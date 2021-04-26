import asyncio


class PingIP:
    def __init__(self, ip_list):
        self.ip_list = ip_list

    @staticmethod
    async def _ping(ip):
        reply = await asyncio.create_subprocess_shell(
            f"ping -c 3 -n {ip}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await reply.communicate()
        ip_is_reachable = reply.returncode == 0
        return ip, ip_is_reachable

    async def scan(self):
        ping_ok = []
        ping_not_ok = []
        coroutines = [self._ping(ip) for ip in self.ip_list]
        result = await asyncio.gather(*coroutines)
        for ip, status in result:
            if status:
                ping_ok.append(ip)
            else:
                ping_not_ok.append(ip)
        return ping_ok, ping_not_ok


if __name__ == "__main__":
    ip_list = ["192.168.100.1", "192.168.100.2", "192.168.100.3", "192.168.100.11"]
    scanner = PingIP(ip_list)
    results = asyncio.run(scanner.scan())
    print(results)
