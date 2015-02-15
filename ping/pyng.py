__author__ = "davide"

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

# Python module for pinging hosts


class ICMPPacket:
    """Class that represents an ICMP struct_packet"""

    __slots__ = "_data", "_checksum", "_type"

    def __init__(self, packetType=ICMP_ECHO_RESPONSE, data=""):
        """Initialize the struct_packet
        @param packetType: tuple
        """
        self.packetType = packetType
        self.data = data
        self._checksum = -1

    @property
    def packetType(self):
        """16 bits that represent the struct_packet type, code"""
        return self._type

    @packetType.setter
    def packetType(self, packet_type):
        if len(packet_type) != 2:
            raise ValueError("type must be a 2-element tuple")
        if any(not 0 <= val < (1 << 8) for val in packet_type):
            raise ValueError("Packet type not valid")
        self._type = packet_type

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


class Pinger:
    """Class useful for pinging remote hosts"""
    DEFAULT_TIMEOUT = 5

    def __init__(self, timeout=DEFAULT_TIMEOUT):
        """Initalize the Pinger with the timeout specified"""
        self.socket = None
        self.timeout = timeout
        self.id_dict = defaultdict(int)

    def ping(self, dest_address, data=None):
        """Sends to dest a ping packet with data specified"""
        if not self.socket:
            self.close()

        dest_address = str(dest_address)
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
    tmax, tmin, tmean, total, received = -1, sys.maxsize, 0, 0, 0

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

            received += 1
            tmean = ((received - 1) * tmean + t) / received
            signal(SIGINT, handler)

            if i != args.tries - 1:
                time.sleep(1)

        except socket.timeout:
            print("Host is not reachable")
        except KeyboardInterrupt:
            break

    print("***** RESULTS *****")
    if received != 0:
        stats = "Max time: {:1.2f} ms, Min time: {:1.2f} ms, Avg time: {:1.2f} ms"
        print(stats.format(tmax, tmin, tmean))

    stats = "Sent packets: {}\tReceived: {}\tLost: {}"
    print(stats.format(total, received, total - received))

    print("Packet Lost: {:1.0f}%".format((total - received) / total * 100))


if __name__ == '__main__':
    main()
