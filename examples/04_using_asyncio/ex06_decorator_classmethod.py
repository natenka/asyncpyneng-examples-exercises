from pprint import pprint
import asyncio
import asyncssh


class ConnectAsyncSSH:

    @classmethod
    async def connect(cls, host, username, password, enable_password, connection_timeout=5):
        self = cls()

        self.host = host
        self.username = username
        self.password = password
        self.enable_password = enable_password
        self.connection_timeout = connection_timeout
        self._ssh = await asyncio.wait_for(
            asyncssh.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                encryption_algs="+aes128-cbc,aes256-cbc",
            ),
            timeout=self.connection_timeout,
        )
        self.writer, self.reader, _ = await self._ssh.open_session(
            term_type="Dumb", term_size=(200, 24)
        )
        await self.reader.readuntil(">")
        self.writer.write("enable\n")
        await self.reader.readuntil("Password")
        self.writer.write(f"{self.enable_password}\n")
        await self.reader.readuntil("#")
        self.writer.write("terminal length 0\n")
        await self.reader.readuntil("#")
        return self

    async def get_prompt(self):
        self.writer.write("\n")
        output = await self.reader.readuntil("#")
        return output


async def main():
    r1 = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "enable_password": "cisco",
    }
    ssh = await ConnectAsyncSSH.connect(**r1)
    print(await ssh.get_prompt())


if __name__ == "__main__":
    asyncio.run(main())
