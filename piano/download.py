from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


address = "http://www.febat.com/Musica/Musica_frequenze_musicali.html"
val = urlopen(address).read().decode()

pattern = re.compile(".*([A-G]#?\d+).*?(\d+) Hz.*", re.DOTALL)
val = re.sub("</TR>\s*<TD>", "</TR><TR><TD>", val)
print(val)

with open("piano.txt", "wt") as f:
    for n in BeautifulSoup(val).find_all("tr"):
        t = re.findall(pattern, str(n))
        if t:
            t = t[0]
            f.write("{};{}\n".format(t[0], t[1]))
