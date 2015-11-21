import re
import collections
import datetime

name_regex = re.compile(r"(?P<name>.+?) ha scritto sul tuo diario")
data_regex = re.compile(r"(?P<giorno>.+?) alle ore (?P<ore>\d+\.\d+)")

Data = collections.namedtuple("Data", "name, date, text")


def process(path):
    data_list = []
    with open(path) as open_file:
        for line in iter(open_file, ""):
            name = line.strip()
            name = name_regex.search(name).group("name")
            data = open_file.readline().strip()
            m_data = data_regex.search(data)
            g = int(m_data.group("giorno")[0])
            h = m_data.group("ore")
            h, m = map(int, h.split("."))
            d = datetime.datetime(2012, 12, g, h, m)

            text = open_file.readline().strip()
            open_file.readline()
            data_list.append(Data(name=name, date=d, text=text))
    return data_list


if __name__ == '__main__':
    l = process("auguri.txt")
    with open("auguri2.txt", "w") as f:
        for d in l:
            t = d.name, str(d.date), d.text
            f.write(";".join(t) + "\n")
