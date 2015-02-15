__author__ = 'Kami'

from Levenshtein import *

ALBUM = """Dark Chest of Wonders
Wish I Had an Angel
Nemo
Planet Hell
Creek Mary's Blood
The Siren
Dead Gardens
Romanticide
Ghost Love Score
Kuolema Tekee Taiteilijan
Higher Than Hope""".split("\n")


def dist(s1, s2):
    m = max(len(s1), len(s2))
    return distance(s1, s2) / m


if __name__ == "__main__":
    ts = ["{:>02} - {}".format(*t) for t in enumerate(ALBUM, start=1)]

    c = {}
    for s1 in ts:
        d = [(s, ratio(s.lower(), s1.lower())) for s in ALBUM]
        d.sort(key=lambda t: -t[1])
        c[s1] = d[0]

    n = 0
    for k, v in c.items():
        i = k.rindex("-")
        if k[i + 2:] == v[0]:
            n += 1
        else:
            print("NO:", '"{}"'.format(k), "matched to", '"{}"'.format(v[0]))
    print("Precisione:", n / len(c))
