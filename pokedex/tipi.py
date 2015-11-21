__author__ = 'davide'

import operator
from enum import IntEnum


class Effect(IntEnum):
    NO_EFFECT = 0
    NOT_EFFECTIVE = 1
    NORMAL = 2
    SUPEREFFECTIVE = 3


class Types(IntEnum):
    Normale = 0
    Fuoco = 1
    Acqua = 2
    Elettro = 3
    Erba = 4
    Ghiaccio = 5
    Lotta = 6
    Veleno = 7
    Terra = 8
    Volante = 9
    Psico = 10
    Coleottero = 11
    Roccia = 12
    Spettro = 13
    Drago = 14
    Buio = 15
    Acciaio = 16


D = (b'\xaa\xaa\xaaJe\xbe\xaa\xd9\xbbf\xae\xaej\xb5\xa8\xea\x9a\x9ei\xd9\xe6e'
     b'\xb6\xbe\xab\x9e\xab\x99\\\xbe\xab\xa5\xa9h\xbbk\x89\xea\xea{\xaa\xda'
     b'\x9a\xaa\xfaj\x86k\x96zm\xba\xb6{\xaaJ\xaa\xab\xaeZ\xaa\xaa\xaa\xe6\xaa'
     b'\x9a\xba\xe5\x95\xba\xaa\xea@')


def get(i1, i2):
    i = i1 * len(Types) + i2
    a, o = divmod(i, 4)
    return Effect((D[a] >> ((3 - o) << 1)) & 0x3)


def getTypeName(i):
    return Types(i).name


if __name__ == "__main__":
    f = operator.itemgetter(1)
    for type_ in Types:
        value = type_.value
        name = type_.name
        if not (value and value % 3):
            print()
        print("{:02}) {}".format(value + 1, name), end="\t" * 5)

    print()
    print("-" * 100)
    print()

    i1 = int(input("Primo tipo: ")) - 1
    i2 = int(input("Secondo tipo: ")) - 1

    if not (0 <= i1 < 17 and 0 <= i2 < 17):
        exit("Valore non valido!")

    v = get(i1, i2)
    if v == Effect.NO_EFFECT:
        esito = "non ha effetto..."
    elif v == Effect.NOT_EFFECTIVE:
        esito = "non e' molto efficace..."
    elif v == Effect.NORMAL:
        esito = "e' normale."
    else:
        esito = "e' superefficace!"

    print("{} su {} {}".format(getTypeName(i1), getTypeName(i2), esito))
