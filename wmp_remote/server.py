__author__ = 'Davide'

import win32api
import win32con
import socket

# stop not defined
VK_MEDIA_STOP = 0xB2


class RemoteController:
    def play_pause(self):
        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 34)

    def stop(self):
        win32api.keybd_event(VK_MEDIA_STOP, 34)

    def next(self):
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 34)

    def prev(self):
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 34)

    def vol_up(self):
        win32api.keybd_event(win32con.VK_VOLUME_UP, 34)

    def vol_down(self):
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 34)

    def vol_mute(self):
        win32api.keybd_event(win32con.VK_VOLUME_MUTE, 34)


class Handler:
    def __init__(self):
        self.controller = RemoteController()

    def dispatch(self, msg):
        if msg == b"p":
            self.controller.play_pause()
        elif msg == b"n":
            self.controller.next()
        elif msg == b"s":
            self.controller.stop()
        elif msg == b"v":
            self.controller.prev()
        elif msg == b"+":
            self.controller.vol_up()
        elif msg == b"-":
            self.controller.vol_down()
        elif msg == b"m":
            self.controller.vol_mute()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    handler = Handler()

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    while True:
        data, addr = server.recvfrom(256)
        print(data, addr)
        handler.dispatch(data)
