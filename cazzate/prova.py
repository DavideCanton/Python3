import time
import win32com.client
import random


client = win32com.client.Dispatch("WScript.Shell")
time.sleep(5)
wl = "sifsaifh", "ijfdsuohgsdk", "hkdhskg", "fhjdkjhf", "difjsdog"
for _ in range(15):
    for c in random.choice(wl):
        client.SendKeys(c)
    client.SendKeys("{enter}")
    time.sleep(1)

