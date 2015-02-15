import sys
from ping.pyng import Pinger
from multiprocessing import Process
import time
import socket


class PingerThread(Process):
    def __init__(self, address):
        super(PingerThread, self).__init__()
        self.daemon = True
        self.address = address
        self.more = True

    def run(self):
        p = Pinger()
        while self.more:
            p.ping(self.address)
            # p.pong()
            time.sleep(1)

    def stop(self):
        self.more = False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Missing argument")
    dest_address = sys.argv[1]
    try:
        dest_address = socket.gethostbyname(dest_address)
    except socket.gaierror:
        sys.exit("{} not valid".format(dest_address))
    number = 5 if len(sys.argv) < 3 else int(sys.argv[2])
    proc_list = []
    for i in range(number):
        print("Spawned {} ping thread".format(i))
        try:
            p = PingerThread(dest_address)
            proc_list.append(p)
            p.start()
        except Exception:
            break
    input("Premere invio per terminare...")
    for p in proc_list:
        p.terminate()
