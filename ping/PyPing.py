import struct
import socket
import argparse
import sys
from datetime import datetime
import time
from collections import defaultdict
from signal import signal, SIGINT, SIG_IGN

ICMP_ECHO_REQUEST = 8, 0
ICMP_ECHO_RESPONSE = 0, 0

__all__ = ["ICMPPacket", "Pinger",
           "ICMP_ECHO_REQUEST", "ICMP_ECHO_RESPONSE"]


class ICMPPacket(object):
    """Class that represents an ICMP struct_packet"""

    def __init__(self, packetType=ICMP_ECHO_RESPONSE, data=""):
        """Initialize the struct_packet"""
        self.packetType = packetType
        self.data = data
        self._checksum = -1

    @property
    def packetType(self):
        """16 bits that represent the struct_packet type, code"""
        return self._type

    @packetType.setter
    def packetType(self, type):
        if len(type) != 2:
            raise ValueError("type must be a 2-element tuple")
        for val in type:
            if val < 0 or val >= (1 << 8):
                raise ValueError("Packet type not valid: {}".format(val))
        self._type = type

    @property
    def data(self):
        """Packet content"""
        return self._data

    @data.setter
    def data(self, data=b""):
        self._data = data or b""

    def compute_checksum(self):
        # checksum set to zero
        header = bytes([self._type[0], self._type[1], 0, 0])
        struct_packet = header + self._data
        length = len(struct_packet)
        if length % 2:
            odd = struct_packet[-1] << 8
            struct_packet = struct_packet[:-1]
        else:
            odd = 0
        format_len = len(struct_packet) // 2
        blocks = struct.unpack("!{}H".format(format_len), struct_packet)
        checksum = sum(blocks)
        checksum += odd
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum += checksum >> 16
        self._checksum = ~checksum & 0xFFFF

    @property
    def checksum(self):
        """Packet checksum"""
        return self._checksum

    @property
    def computedChecksum(self):
        """Computed checksum"""
        return self._checksum >= 0

    def __str__(self):
        return ("ICMPPacket[type={}, data={}, checksum={}]"
                .format(self._type, self._data[4:], self._checksum))

    def encodePacket(self):
        """Returns the struct_packet encoded in a string"""
        if not self.computedChecksum:
            self.compute_checksum()
        return struct.pack("!BBH{}s".format(len(self._data)),
                           self._type[0], self._type[1],
                           self._checksum, self._data)

    @staticmethod
    def buildPacket(raw):
        """Builds an ICMPPacket from the string raw
           (received from a pong), returns (IP Header (raw), ICMP Packet)"""
        ihl = (raw[0] & 0x0F) << 2
        ip_header, raw_packet = raw[:ihl], raw[ihl:]
        format_len = len(raw_packet) - 4
        unpacked = struct.unpack("!BBH{}s".format(format_len), raw_packet)
        packet = ICMPPacket(unpacked[:2], unpacked[3])
        packet._checksum = unpacked[2]
        return ip_header, packet


class Pinger(object):
    """Class useful for pinging remote hosts"""
    DEFAULT_TIMEOUT = 5

    def __init__(self, timeout=Pinger.DEFAULT_TIMEOUT):
        """Initalize the Pinger with the timeout specified"""
        self.socket = None
        self.timeout = timeout
        self.id_dict = defaultdict(int)

    def ping(self, dest_address, data=None):
        """Sends to dest a ping packet with data specified"""
        if not self.socket:
            self.close()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                    socket.getprotobyname("icmp"))
        self.socket.connect((dest_address, 0))
        self.socket.settimeout(self.timeout)

        packet = ICMPPacket(packetType=ICMP_ECHO_REQUEST)
        idpacket = struct.pack("!I", self.id_dict[dest_address])
        packet.data = idpacket + (data or b"")

        self.id_dict[dest_address] += 1

        packet_struct = packet.encodePacket()
        self.socket.send(packet_struct)

    def pong(self):
        """Returns the response of remote host"""
        if not self.socket:
            raise socket.error("Socket closed")
        return ICMPPacket.buildPacket(self.socket.recv((1 << 16) - 1))

    def close(self):
        """Closes the Pinger"""
        if self.socket:
            self.socket.close()
            self.socket = None

    def __del__(self):
        """Closes the Pinger"""
        self.close()


def main():
    def parseArgs():
        handler = argparse.ArgumentParser(description="Pinger")

        handler.add_argument('-r', '--remote_host', help="Destination",
                             default="localhost", dest="dest")

        handler.add_argument('-d', '--data', help="Dati", default="",
                             dest="data")

        handler.add_argument('-t', '--tries', help="Numero di ping",
                             default=sys.maxsize, dest="tries", type=int)

        return handler.parse_args()

    args = parseArgs()
    try:
        ip = socket.gethostbyname(args.dest)
    except socket.gaierror:
        sys.exit("{} not found".format(args.dest))
    print("Pinging", args.dest, "(" + ip + ")")
    pinger = Pinger()
    tmax = -1
    tmin = sys.maxsize
    tsum = 0
    tnumber = 0
    total = 0

    for i in range(args.tries):
        total += 1
        try:
            pinger.ping(args.dest, args.data.encode())
            t = datetime.now()
            pinger.pong()
            t = (datetime.now() - t).microseconds / 1000.
            print("Got ping from {} in {:1.2f} ms".format(args.dest, t))

            handler = signal(SIGINT, SIG_IGN)
            tmax, tmin = max(tmax, t), min(tmin, t)

            tsum += t
            tnumber += 1
            signal(SIGINT, handler)

            if i != args.tries - 1:
                time.sleep(1)

        except socket.timeout:
            print("Host is not reachable")
        except KeyboardInterrupt:
            break

    print("***** RESULTS *****")
    if tnumber != 0:
        print("Max time: {:1.2f} ms, "
              "Min time: {:1.2f} ms, "
              "Avg time: {:1.2f} ms"\
        .format(tmax, tmin, tsum / tnumber))
    else:
        print("Statistiche non disponibili")

    print("Pacchetti trasmessi: {}\tRicevuti: {}\tPersi: {}"\
    .format(total, tnumber, total - tnumber))

    print("Persi {:1.0f}%".format((total - tnumber) / total * 100))

if __name__ == '__main__':
    main()
