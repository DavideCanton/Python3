# coding=utf-8

__author__ = 'davide'

from collections import namedtuple, defaultdict, deque
from datetime import datetime
import operator
import os
import sys
import re

Visita = namedtuple('Visita', 'presenze first last')

def to_date(date_, time_):
    # y-m-d h:m:s
    splitted_date = [int(x) for x in date_.split("-")]
    splitted_time = [int(x) for x in time_.split(":")]
    return datetime(*(splitted_date + splitted_time))


def update(user_city, date):
    presenze = user_city.presenze + 1
    first = min(user_city.first, date)
    last = max(user_city.last, date)
    return user_city._replace(presenze=presenze, first=first, last=last)


def make_dict(name):
    count = 0
    visite = defaultdict(dict)
    with open(name) as file_handle:
        for row in file_handle:
            try:
                city, user, date_, time_, _ = row.split()
                date = to_date(date_, time_)
                visite_u = visite[user]
                if city in visite_u:
                    user_city = visite_u[city]
                    user_city = update(user_city, date)
                else:
                    user_city = Visita(1, date, date)
                visite_u[city] = user_city
                if count % 1000000 == 0:
                    print("Processed {} tuples...".format(count))
                count += 1
            except ValueError:
                pass
    print("Processed {} tuples...".format(count))
    return visite


def calcola_residenze(visite):
    residenze = {}
    gt_1 = []
    vuote = 0

    while visite:
        user, data = visite.popitem()
        pres_max_n, int_max_n = None, None
        pres_max, int_max = set(), set()
        turista = []

        for (city, v) in data.items():
            turista.append(city)
            d = v.last - v.first
            if pres_max_n is None:
                pres_max_n = v.presenze
                int_max_n = d

            if pres_max_n < v.presenze:
                pres_max = {city}
                pres_max_n = v.presenze
            elif pres_max_n == v.presenze:
                pres_max.add(city)

            if int_max_n < d:
                int_max = {city}
                int_max_n = d
            elif int_max_n == d:
                int_max.add(city)

        residente_set = pres_max & int_max
        
        if len(residente_set) > 1:
            gt_1.append(len(residente_set))
        elif len(residente_set) == 0:
            vuote += 1

        if residente_set:
            residente = residente_set.pop()
            turista.remove(residente)
            residenze[user, residente] = "R"
        for city in turista:
            residenze[user, city] = "T"
            
    print("Numero di utenti senza residenza:", vuote)
    print("Numero di utenti con più città candidate:", len(gt_1))
    if gt_1:
        print("Media di numero di città candidate:", sum(gt_1) / len(gt_1))

    return residenze


def main(file_name, folderR):
    with open(os.path.join(folderR, "dest.txt"), "w") as outfile:
        visite = make_dict(file_name)
        residenze = calcola_residenze(visite)
        for (k, v) in residenze.items():
            if k[1] is not None:
                outfile.write("{} {} {}\n".format(k[0], k[1], v))
    print("Index created!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit("Parametri non validi!")
    file_name = sys.argv[1]
    folderR = sys.argv[2]

    if not os.path.exists(folderR):
        os.makedirs(folderR)
    main(file_name, folderR)