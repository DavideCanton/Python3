__author__ = 'Davide'

from collections import namedtuple
import numpy as np


def format_num(num):
    return (str(round(num * 100, 2)) + "%").center(20)


def make_double_stochastic_matrix(m):
    row = True
    while True:
        if row:
            r = m.sum(1)
            if np.allclose(r, np.ones_like(r)):
                break
            m /= r[:, np.newaxis]
        else:
            c = m.sum(0)
            if np.allclose(c, np.ones_like(c)):
                break
            m /= c
        row = not row


def main():
    Team = namedtuple("Team", "name country round")

    fst_teams = [Team("Real Madrid", "ES", "B"), Team("Barcelona", "ES", "F"),
                 Team("Bayern Monaco", "G", "E"), Team("Chelsea", "EN", "G"),
                 Team("Atletico Madrid", "ES", "A"), Team("Porto", "P", "H"),
                 Team("Borussia Dortmund", "G", "D"),
                 Team("Monaco", "FR", "C")]

    snd_teams = [Team("Arsenal", "EN", "D"), Team("Schalke 04", "G", "G"),
                 Team("Juventus", "IT", "A"), Team("PSG", "FR", "F"),
                 Team("Shakhtar", "UCR", "H"), Team("Basilea", "CH", "B"),
                 Team("Manchester City", "EN", "E"),
                 Team("Bayern Leverkusen", "G", "C")]

    m = np.ones((len(fst_teams), len(snd_teams)), dtype=np.float)
    for i, t1 in enumerate(fst_teams):
        for j, t2 in enumerate(snd_teams):
            if t1.country == t2.country or t1.round == t2.round:
                m[i, j] = 0.

    make_double_stochastic_matrix(m)

    print(r"1st \ 2nd".center(20), end="|")
    for t2 in snd_teams:
        print(t2.name.center(20), end="|")
    print()

    for i, t1 in enumerate(fst_teams):
        print(t1.name.center(20), end="|")
        print("|".join(format_num(n) for n in m[i, :]), end="|")
        print()

    print()

    for i, t1 in enumerate(fst_teams):
        indices = np.argsort(m[i, :])[-3:][::-1]
        names = [(x, snd_teams[x]) for x in indices]
        print("Most probable matches for {}:".format(t1.name), end=" ")
        print(", ".join("{} ({}%)".format(t.name, round(m[i, x] * 100, 2))
                        for (x, t) in names))

    for j, t2 in enumerate(snd_teams):
        indices = np.argsort(m[:, j])[-3:][::-1]
        names = [(x, fst_teams[x]) for x in indices]
        print("Most probable matches for {}:".format(t2.name), end=" ")
        print(", ".join("{} ({}%)".format(t.name, round(m[x, j] * 100, 2))
                        for (x, t) in names))


if __name__ == "__main__":
    main()
