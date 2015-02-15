__author__ = 'davide'

import socket
import socketserver

def getData(data):
    tid = data[:2]
    name = data[12:]
    l = []
    last = -1
    for c in name:
        if last < 0:
            if c == 0:
                break
            last = c
            l.append([])
        else:
            l[-1].append(chr(c))
            last -= 1
        if last == 0:
            last = -1
    s = ".".join("".join(x) for x in l)
    #print(s)
    return tid, name


def getResp(tid, name):
    buf = [tid, b"\x81\x80\0\x01\0\x01\0\0\0\0", name,
           b"\xc0\x0c\0\x01\0\x01\0\0\0\xde\0\x04"]
    return b"".join(buf)


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("glennhk.altervista.org", 80))
        s.send(b"GET / HTTP/1.0")
        data = s.recv(10000)
        self.request.sendall(data)

if __name__ == "__main__":
    HOST, PORT = "", 80
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()