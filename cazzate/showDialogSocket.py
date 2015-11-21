import ctypes
import os.path
import socket

myDll = ctypes.cdll.LoadLibrary(os.path.join("lib", "Dialog.dll"))
s = socket.socket()
s.bind(("", 8000))
s.listen(1)
while True:
    ch, addr = s.accept()
    myDll.ShowDialog("Got connection from {}".format(addr), "Info")
    ch.send("Ciaooo")
    ch.close()
