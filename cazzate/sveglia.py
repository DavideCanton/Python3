import ctypes
import os
import time

myDll = ctypes.cdll.LoadLibrary(os.path.join("lib", "Dialog.dll"))


def show_dialog(message, title="Python Dialog"):
    myDll.ShowDialog(message.encode(), title.encode())


message = input("Messaggio>")
wait_time = int(input("Tempo>"))
time.sleep(wait_time)
show_dialog(message)
