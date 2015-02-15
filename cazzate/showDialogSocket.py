from ctypes import cdll
import os.path
from socket import *

myDll = cdll.LoadLibrary(os.path.join("lib", "Dialog.dll"))
s = socket()
s.bind(("", 8000))
s.listen(1)
while True:
    ch, addr = s.accept()
    myDll.ShowDialog("Got connection from {}".format(addr), "Info")
    ch.send("Ciaooo")
    ch.close()
