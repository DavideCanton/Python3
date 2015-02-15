# coding=utf-8
__author__ = 'davide'

from collections import Counter, OrderedDict
from decimal import Decimal as D
from decimal import getcontext
from itertools import zip_longest


class Arit:
    def __init__(self, p):
        self.p = p
        self.a = D()
        self.b = D("1")
        self.aD = D()
        self.bD = D("1")

    def feed_encode(self, ch):
        diff = self.b - self.a
        bk = self.a
        for k in p:
            ak = bk
            bk = bk + self.p[k] * diff
            if k == ch:
                self.a, self.b = ak, bk
                break
        return self.a, self.b

    def decode(self, n):
        bk = self.aD
        diff = self.bD - self.aD
        for k in self.p:
            ak = bk
            bk = ak + self.p[k] * diff
            if ak <= n < bk:
                if k == "\0":
                    raise StopIteration
                yield k
                self.aD, self.bD = ak, bk
                break


def computeP(s):
    s += "\0"
    l = D(len(s))
    c = Counter(s)
    p = {k: D(v) / l for k, v in c.items()}
    return p


def getN(a, b):
    sa, sb = map(str, (a, b))
    flag = False
    l = ["0", "."]
    i = 0
    for i, t in enumerate(zip_longest(sa[2:], sb[2:], fillvalue="0")):
        ia, ib = map(int, t)
        l.append(str(ia))
        if flag:
            break
        if ia != ib:
            flag = True
    d = D("".join(l))
    d += D("." + "0" * i + "1")
    return d

if __name__ == "__main__":
    getcontext().prec = 10
    s = "Soffermati sull’arida sponda volti i guardi al varcato Ticino, "\
        "tutti assorti nel novo destino, certi in cor dell’antica virtù, han giurato: "\
        "non fia che quest’onda scorra più tra due rive straniere; non fia loco ove sorgan "\
        "barriere tra l’Italia e l’Italia, mai più! L’han giurato: altri forti a quel giuro "\
        "rispondean da fraterne contrade, affilando nell’ombra le spade che or levate scintillano "\
        "al sol. Già le destre hanno strette le destre; già le sacre parole son porte; o compagni "\
        "sul letto di morte, o fratelli su libero suol. Chi potrà della gemina Dora, della Bormida "\
        "al Tanaro sposa, del Ticino e dell’Orba selvosa scerner l’onde confuse nel Po; chi stornargli "\
        "del rapido Mella e dell’Oglio le miste correnti, chi ritorgliergli i mille torrenti che la "\
        "foce dell’Adda versò, quello ancora una gente risorta potrà scindere in volghi spregiati, "\
        " e a ritroso degli anni e dei fati, risospingerla ai prischi dolor; una gente che libera "\
        "tutta o fia serva tra l’Alpe ed il mare; una d’arme, di lingua, d’altare, di memorie, di "\
        "sangue e di cor. Con quel volto sfidato e dimesso, con quel guardo atterrato ed incerto con "\
        "che stassi un mendico sofferto per mercede nel suolo stranier, star doveva in sua terra il "\
        "Lombardo: l’altrui voglia era legge per lui; il suo fato un segreto d’altrui; la sua parte "\
        "servire e tacer. O stranieri, nel proprio retaggio torna Italia e il suo suolo riprende; o "\
        "stranieri, strappate le tende da una terra che madre non v’è. Non vedete che tutta si scote, "\
        "dal Cenisio alla balza di Scilla? non sentite che infida vacilla sotto il peso de’ barbari piè?"

    #s = "abcabd"
    p = computeP(s)
    ar = Arit(p)

    for ch in s:
        a, b = ar.feed_encode(ch)
    a, b = ar.feed_encode("\0")

    print("[{}, {}[".format(a, b))
    n = getN(a, b)
    print(n)

    l = list(ar.decode(n))
    print(s)
    print("".join(l))