# coding=utf-8

__author__ = 'davide'

import operator
import os
import sys
from collections import defaultdict
from datetime import datetime


def to_date(date_, time_):
    # y-m-d h:m:s
    splitted_date = [int(x) for x in date_.split("-")]
    splitted_time = [int(x) for x in time_.split(":")]
    return datetime(*(splitted_date + splitted_time))


def find_residenza(mapping, user):
    city_dict = mapping[user]
    for city, status in city_dict.items():
        if status == "R":
            return city
    return None


def processChunk(queue, folder, mapping):
    if not queue:
        return
    queue.sort(key=operator.itemgetter(1))
    last_city = queue[0][0]
    last_file_res = open(os.path.join(folder, "c_" + last_city + "_R.txt"), "a")
    last_file_tour = open(os.path.join(folder, "c_" + last_city + "_T.txt"), "a")
    for data in queue:
        city = data[0]
        user = data[1]
        if user not in mapping:
            continue
        city_dict = mapping[user]
        if city not in city_dict:
            continue
        if city != last_city:
            last_city = city
            last_file_res.close()
            last_file_tour.close()
            last_file_res = open(os.path.join(folder, "c_" + last_city + "_R.txt"), "a")
            last_file_tour = open(os.path.join(folder, "c_" + last_city + "_T.txt"), "a")        
        status = city_dict[city]
        if status == "R":
            last_file_res.write(" ".join(data) + "\n")
        else:
            residenza = find_residenza(mapping, user)
            if residenza is not None:
                data.append(residenza)
                last_file_tour.write(" ".join(data) + "\n")
    last_file_res.close()
    last_file_tour.close()
    queue.clear()


def load_mapping(path):
    mapping = defaultdict(dict)
    with open(path) as file_handle:
        for row in file_handle:
            user, city, esito = row.split()
            mapping[user][city] = esito
    return mapping


def main(file_name, folder):
    print("Loading index...")
    mapp = load_mapping(os.path.join(folder, "dest.txt"))
    N = 100000
    queue = []
    print("Start processing...")
    with open(file_name) as file_handle:
        for row in file_handle:
            data = row.split()
            date_, time_ = data[2:4]
            try:
                to_date(date_, time_)
                queue.append(data)
                if len(queue) == N:
                    processChunk(queue, folder, mapp)
            except ValueError:
                pass
    processChunk(queue, folder, mapp)
    print("End processing!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit("Parametri non validi!")
    file_name = sys.argv[1]
    folderR = sys.argv[2]
    if not os.path.exists(folderR):
        os.makedirs(folderR)
    main(file_name, folderR)