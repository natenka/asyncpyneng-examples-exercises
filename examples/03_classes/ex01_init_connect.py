from pprint import pprint
import asyncio
import asyncssh


class ConnectAsyncSSH:
    def __init__(self, host, username, password, enable_password, connection_timeout=5):
        self.host = host
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.connection_timeout = connection_timeout

    async def connect(self):
        self.ssh = await asyncio.wait_for(
            asyncssh.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                encryption_algs="+aes128-cbc,aes256-cbc",
            ),
            timeout=self.connection_timeout,
        )
        self.writer, self.reader, _ = await self.ssh.open_session(
            term_type="Dumb", term_size=(200, 24)
        )
        await reader.readuntil(">")
        self.writer.write("enable\n")
        await reader.readuntil("Password")
        self.writer.write(f"{self.enable_password}\n")
        await reader.readuntil("#")
        self.writer.write("terminal length 0\n")
        await reader.readuntil("#")


async def main():
    r1 = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "enable_password": "cisco",
    }
    ssh = ConnectAsyncSSH(**r1)
    await ssh.connect()


if __name__ == "__main__":
    asyncio.run(main())
