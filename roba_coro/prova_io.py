from socket import SOCK_STREAM, AF_INET, socket
from roba_coro.syscalls import NewTask, ReadWait, WriteWait
from roba_coro.utils import Scheduler

__author__ = 'Davide'


def handle_client(client, addr):
    print("Connection from", addr)
    while True:
        yield ReadWait(client)
        data = client.recv(1 << 16)
        if not data:
            break
        yield WriteWait(client)
        client.send(data)
    client.close()
    print("Client closed")
    yield


def server(port):
    print("Start server on port", port)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(5)
    while True:
        yield ReadWait(sock)
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))


if __name__ == "__main__":
    sched = Scheduler()
    sched.new(server(45000))
    sched.new(server(46000))
    sched.mainloop()