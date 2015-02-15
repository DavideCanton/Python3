__author__ = 'davide'

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
           b"\xc0\x0c\0\x01\0\x01\0\0\0\xde\0\x04\xc0\xa8\x01\x21"]
    return b"".join(buf)


class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        tid, name = getData(data)
        resp = getResp(tid, name)
        socket.sendto(resp, self.client_address)
        self.server.shutdown()

if __name__ == "__main__":
    HOST, PORT = "", 53
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()