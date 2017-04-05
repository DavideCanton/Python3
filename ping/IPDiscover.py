from ping.pyng import Pinger
import socket
import sys
import ipaddress


class MockPinger:
    def __init__(self, *args, **kwargs):
        pass

    def ping(self, *args, **kwargs):
        pass

    def pong(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    if len(sys.argv) > 2:
        exit("Uso: {} <timeout in ms>".format(sys.argv[0]))

    timeout = 1 if len(sys.argv) < 2 else float(sys.argv[1]) / 1000
    pinger = Pinger(timeout)
    result = {}

    net_ip = ipaddress.IPv4Network("192.168.1.0/24")

    for ip in net_ip:
        print("Pinging", ip, end=' ')
        sys.stdout.flush()
        pinger.ping(ip, data=b"a")

        try:
            pinger.pong()
        except socket.timeout:
            print("-> not found")
        else:
            try:
                addresses = socket.gethostbyaddr(str_ip)[:2]
                addresses[1].append(addresses[0])
                result[ip] = addresses[1]
                print("->", addresses[1])
            except socket.herror:
                result[ip] = [str(ip)]
                print("->", ip)

    for k, v in sorted(result.items()):
        print("{}\t=>\t{}".format(k, " ".join(v)))
