from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
from multiprocessing.pool import ThreadPool
from scipy.odr.__odrpack import odr_stop


def down(addr, name, address, directory):
    print("Downloading {}...".format(name))
    if addr[0] != "/":
        pagina = urlopen(addr).read()
    else:
        pagina = urlopen(address + addr).read()

    print("Sto salvando {}...".format(name))
    try:
        with open(os.path.join(directory, name), "wb") as f:
            f.write(pagina)
    except OSError:
        pass

if __name__ == '__main__':
    address = "http://foto.panorama.it/"
    directory = "img"
    t = ThreadPool(5)

    if address[-1] != "/":
        address += "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    content = urlopen(address).read()

    for link in BeautifulSoup(content).find_all("img"):
        addr = link["src"]
        name = addr.split("/")[-1]
        args = (addr, name, address, directory)
        t.apply_async(down, args=args)

    t.close()
    t.join()
