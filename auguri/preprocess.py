import re
from collections import namedtuple
from datetime import datetime

name_regex = re.compile(r"(?P<name>.+?) ha scritto sul tuo diario")
data_regex = re.compile(r"(?P<giorno>.+?) alle ore (?P<ore>\d+\.\d+)")


Data = namedtuple("Data", "name, date, text")


def process(path):
    l = []
    with open(path) as f:
        while True:
            name = f.readline().strip()
            if not name:
                break
            name = name_regex.search(name).group("name")
            data = f.readline().strip()
            m_data = data_regex.search(data)
            g = int(m_data.group("giorno")[0])
            h = m_data.group("ore")
            h, m = map(int, h.split("."))
            d = datetime(2012, 12, g, h, m)

            text = f.readline().strip()
            f.readline()
            l.append(Data(name=name, date=d, text=text))
    return l


if __name__ == '__main__':
    l = process("auguri.txt")
    with open("auguri2.txt", "w") as f:
        for d in l:
            t = d.name, str(d.date), d.text
            f.write(";".join(t) + "\n")
