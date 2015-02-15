from tkinter.tix import Tk
from tkinter.ttk import Label, Entry, Button, Combobox
import sys
from tkinter.messagebox import showerror
from tkinter import StringVar
from tkinter.constants import S, E, N, W, CENTER, FALSE, DISABLED
try:
    from wmi import WMI
except ImportError:
    pass
import re
from subprocess import Popen, PIPE, call, check_output
from collections import defaultdict
from functools import partial, wraps


class IPError(Exception):
    def __init__(self, msg):
        super(IPError, self).__init__(msg)


class IPManager:
    def setStatic(self, ip, gateway, mask="/24"):
        raise NotImplementedError

    def setDynamic(self):
        raise NotImplementedError

    def getData(self):
        raise NotImplementedError

    def _split(self, l, n):
        it = iter(l)
        while True:
            try:
                yield "".join([next(it) for _ in range(n)])
            except StopIteration:
                break

    def getIFList(self):
        return None

    def _expand(self, mask):
        i = int(mask[1:])
        s = "1" * i + "0" * (32 - i)
        b2 = partial(int, base=2)
        return ".".join(str(b2(x)) for x in self._split(s, 8))


class IPManagerWin(IPManager):
    query = ("select * from "
            "Win32_NetworkAdapterConfiguration where IPEnabled=TRUE")

    def __init__(self):
        wmi = WMI()
        net_adapter = wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        if not net_adapter:
            raise IPError("Adapter not found")
        self.ni = net_adapter[0]
        self.wmi = wmi

    def setStatic(self, ip, gateway, mask="/24"):
        if mask[0] == "/":
            mask = self._expand(mask)
        v, *_ = self.ni.EnableStatic(IPAddress=[ip],
                                     SubnetMask=[mask])
        if v != 0:
            raise IPError("Errore in EnableStatic: {}".format(v))
        v, *_ = self.ni.SetGateways(DefaultIPGateway=[gateway])
        if v != 0:
            raise IPError("Errore in SetGateways: {}".format(v))

    def setDynamic(self):
        v, *_ = self.ni.EnableDHCP()
        if v != 0:
            raise IPError("Errore in EnableDHCP: {}".format(v))

    def getData(self):
        res = self.wmi.query(IPManagerWin.query)
        dev = res[0]
        return (dev.IPAddress[0], dev.IPSubnet[0],
                dev.DefaultIPGateway[0], dev.DHCPEnabled)


class InterfacesFileManager:
    def __init__(self):
        self.d = self._load()

    def _load(self):
        d = defaultdict(list)
        current = None
        with open("/etc/network/interfaces") as f:
            for line in f:
                line = line.strip()
                if line.startswith("iface"):
                    current = line.split()[1]
                    if "loopback" in line:
                        current = None
                        continue
                    if "dhcp" in line:
                        ip, mask = self._parseIFCONFIG(current)
                        gw = self._getGateway()
                        d[current] = [ip, mask, gw, "dhcp"]
                        current = None
                elif line.startswith("address"):
                    d[current].append(line.split()[1])
                elif line.startswith("netmask"):
                    d[current].append(line.split()[1])
                elif line.startswith("gateway"):
                    d[current].append(line.split()[1])
                if current and len(d[current]) == 3:
                    d[current].append("static")
                    current = None
        return d

    def setStatic(self, iface, ip, mask, gw):
        self.d[iface] = [ip, mask, gw, "static"]
        self._write()

    def setDynamic(self, iface):
        self.d[iface] = ["dhcp"]
        self._write()

    def getData(self, iface):
        return self.d[iface]

    def _write(self):
        with open("/etc/network/interfaces", "w") as f:
            f.write("auto lo\niface lo inet loopback\n\n")
            for k, v in self.d.items():
                f.write("auto {}\n".format(k))
                if len(v) == 1 or v[-1] == "dhcp":
                    f.write("iface {} inet dhcp\n\n".format(k))
                else:
                    f.write("iface {} inet static\n".format(k))
                    f.write("address {}\n".format(v[0]))
                    f.write("netmask {}\n".format(v[1]))
                    f.write("gateway {}\n\n".format(v[2]))
        call("/etc/init.d/networking restart", shell=True)
        self.d = self._load()

    def _parseIFCONFIG(self, ifname):
        s = Popen("ifconfig {}".format(ifname), shell=True,
                  stdout=PIPE, stderr=PIPE)
        o, e = s.communicate()
        if e:
            raise IPError("Error in ifconfig {}".format(e))
        o = o.decode()
        m = re.findall("\d+\.\d+\.\d+\.\d+", o)
        return m[0], m[2]

    def _getGateway(self):
        o = check_output("route", shell=True)       
        try:
            s = [l for l in o.decode().split("\n")
                 if l.startswith("default")][0]
            return s.strip().split()[1]
        except IndexError:
            return ""


class IPManagerLinux(IPManager):
    def __init__(self, iname):
        self.ifname = iname
        self.fm = InterfacesFileManager()

    def getIFList(self):
        s = check_output("netstat -i", shell=True).decode().split('\n')
        l = [x.split()[0] for x in s if x][2:]
        l.remove("lo")
        return l

    def setStatic(self, ip, gateway, mask="/24"):
        if mask[0] == "/":
            mask = self._expand(mask)
        try:
            self.fm.setStatic(self.ifname, ip, mask, gateway)
        except Exception as e:
            raise IPError("Errore: {}".format(e))

    def setDynamic(self):
        try:
            self.fm.setDynamic(self.ifname)
        except Exception as e:
            raise IPError("Errore: {}".format(e))

    def getData(self):
        t = self.fm.getData(self.ifname)
        return t[0], t[1], t[2], (t[3] == "dhcp")

    def setIFName(self, iname):
        self.ifname = iname


class Show_error_in_messagebox:
    def __init__(self, exctypes, aft_raise=False):
        self.exctypes = exctypes
        self.aft_raise = aft_raise

    def __call__(self, func):
        @wraps(func)
        def wrapper(*a, **k):
            try:
                ret = func(*a, **k)
            except Exception as e:
                if type(e) in self.exctypes:
                    showerror("Errore", str(e))
                    if self.aft_raise:
                        raise e
                    else:
                        return
                else:
                    raise e
            return ret
        return wrapper


class GUI(Tk):
    @Show_error_in_messagebox([IPError], aft_raise=True)
    def __init__(self, master=None):
        super(GUI, self).__init__(master)
        self.title("IP Manager")
        self.resizable(FALSE, FALSE)
        self.ip = StringVar()
        self.mask = StringVar()
        self.gateway = StringVar()
        self.val = StringVar()
        Label(self, text="IP:", anchor=E).grid(row=0, column=0)
        Entry(self, textvar=self.ip).grid(row=0, column=1)
        Label(self, text="Mask:", anchor=E).grid(row=1, column=0)
        Entry(self, textvar=self.mask).grid(row=1, column=1)
        Label(self, text="Gateway:", anchor=E).grid(row=2, column=0)
        Entry(self, textvar=self.gateway).grid(row=2, column=1)
        Label(self, text="IFace:", anchor=E).grid(row=3, column=0)
        box = Combobox(self, textvariable=self.val, state='readonly')
        box.grid(row=3, column=1)
        box.bind("<<ComboboxSelected>>", self.change)
        bs = Button(self, text="IP Statico", command=self.ip_static)
        bs.grid(row=4, column=0, sticky=N + W + S + E)
        bd = Button(self, text="IP Dinamico", command=self.ip_dynamic)
        bd.grid(row=4, column=1, sticky=N + W + S + E)
        bu = Button(self, text="Aggiorna", command=self._fillData)
        bu.grid(row=5, column=0, columnspan=2, sticky=N + W + S + E)
        self._setupOS(box)
        l = self.ipm.getIFList()
        box['values'] = l if l is not None else []
        self.status = Label(self, anchor=CENTER)
        self.status.grid(row=6, column=0, columnspan=2, sticky=N + W + S + E)
        self._fillData()

    def change(self, *e):
        self.ipm.setIFName(self.val.get())

    def _fillData(self):
        ip, mask, gateway, dynamic = self.ipm.getData()
        self.ip.set(ip)
        self.mask.set(mask)
        self.gateway.set(gateway)
        if dynamic:
            self.status.configure(text="IP Dinamico")
        else:
            self.status.configure(text="IP Statico")

    def _setupOS(self, box):
        if sys.platform.startswith("win32"):
            self.ipm = IPManagerWin()
            box.config(state=DISABLED)
        else:
            self.ipm =  IPManagerLinux("eth0")

    @Show_error_in_messagebox([IPError])
    def ip_static(self):
        ip = self.ip.get()
        mask = self.mask.get()
        gateway = self.gateway.get()
        if ip and mask and gateway:
            self.ipm.setStatic(ip, gateway, mask)
            self.status.configure(text="IP Statico")
            self._fillData()

    @Show_error_in_messagebox([IPError])
    def ip_dynamic(self):
        self.ipm.setDynamic()
        self.status.configure(text="IP Dinamico")
        self._fillData()


if __name__ == '__main__':
    GUI().mainloop()
