from urllib.request import urlopen
import os.path as path
import os

directory = "img"

if not path.exists(directory):
    os.mkdir(directory)

addr = ("http://www.zona111.it/il_mio_blog/"
        "wp-content/gallery/carte_napoletane/")
name_template = "{}-{}.jpg"
for i in range(1, 11):
    for seed in ("bastoni", "spade", "coppe", "denari"):
        name = name_template.format(i, seed)
        pagina = urlopen(addr + name).read()
        print("Sto salvando {}".format(name))
        dest = "c_{}{}.jpg".format(i, seed[0])
        with open(path.join(directory, dest), "wb") as f:
            f.write(pagina)
