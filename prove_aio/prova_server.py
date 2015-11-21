import asyncio


class MyProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Data:", data)
        self.transport.write(data)


def main():
    loop = asyncio.get_event_loop()
    coro = loop.create_server(MyProtocol, "localhost", 8000, reuse_address=True)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main()
