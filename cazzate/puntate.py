# ! /usr/bin/python3

from urllib.request import urlopen
import re
import sys

try:
    import winreg
except ImportError:
    print("Warning: winreg non disponibile (feature NEW non disponibile)",
          file=sys.stderr)
    winreg = None

USE_WINREG = False
base_url = "http://www.piratestreaming.com/serietv/"

chuck = {"url": "chuck.html",
         "start": "Quinta Stagione Ita",
         "end": "<div"}
bbt = {"url": "The-Big-Bang-Theory.html",
       "start": "Quinta Stagione",
       "end": "Quinta Stagione"}


def find(start, end, url, serie):
    s = urlopen(base_url + url).read().decode(errors="ignore")
    start_i = s.find(start)
    end_i = s.find(end, start_i + 1) + len(end)
    return set([match.group(0) for match in
                re.finditer(r"{}x\d+".format(serie), s[start_i:end_i])])


def get_len(set_puntate, name):
    new = ""
    puntate = len(set_puntate)
    if winreg and USE_WINREG:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r'Software\KamiPuntate', 0,
                                 winreg.KEY_ALL_ACCESS)
            val, _ = winreg.QueryValueEx(key, name)
        except WindowsError:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                   r'Software\KamiPuntate')
            val = 0
        if val != puntate:
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, puntate)
            new = " NEW"
    return puntate, new


# print("Chuck: {} puntate{}"
# .format(*get_len(find(serie=5, **chuck), "Chuck")))
l = get_len(find(serie=5, **bbt), "The Big Bang Theory")
print("The Big Bang Theory: {} puntate{}".format(*l))
