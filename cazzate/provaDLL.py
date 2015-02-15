from ctypes import cdll
from functools import partial
import os.path

myDll = cdll.LoadLibrary(os.path.join("lib", "Dialog.dll"))
message, title = map(str.encode, [input("Messaggio>"), input("Titolo>")])
myDll.ShowDialog(message, title)
