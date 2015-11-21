import asyncio


class MyProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(b"Ciao!")

    def data_received(self, data):
        print(data.decode())
        self.transport.close()

    def connection_lost(self, exc):
        self.loop.stop()


def main():
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: MyProtocol(loop), "localhost", 8000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
