from math import exp
import csv
import numpy
import sys
from functools import partial
import monia_parser
import datetime


def freshness_relation(delta, rate):
    """
    Data il timestamp tc associato all'attivita' di 
    interesse svolta dall'utente i nei riguardi dell'azione
    svolta da j nel timestamp tp
    """
    try:
        return 2 / (1 + exp(rate * delta))
    except OverflowError:
        return 0


def compute_freshness_relation(file_in, file_out):
    row_buffer = None
    with open(file_out, "w", newline="") as out_file, open(file_in, "r", newline="") as in_file:
        writer = csv.writer(out_file, delimiter=";")
        writer.writerow(["userid", "follower_id", "freshness_relation"])

        # lettura file
        # Finche' non si arriva alla fine del file...
        while row_buffer != []:
            posts_info, interaction_info, row_buffer = monia_parser.parse_next_user(in_file, row_buffer)
            # Per ogni coppia di utenti si va a creare una lista di coppie (timestamp_post, timestamp_interazione)
            for (j, i), interactions in interaction_info.items():
                interactions_pair = [(posts_info[j, p], tc)
                                     for (tc, p, _) in interactions]
                # Si ordina la lista di coppie rispetto ai timestamps di interazione
                interactions_pair.sort(key=lambda t: t[1])
                # Latenza tra i timestamp di post e di interazione per ogni coppia di utenti
                deltas = numpy.array([(tc - tp).days for (tp, tc) in interactions_pair])
                # velocita' di crescita della funzione di freshness
                rate = 1 / (1 + numpy.std(deltas))
                # Calcolo freshness
                freshness_rate = partial(freshness_relation, rate=rate)
                freshness_vec = numpy.vectorize(freshness_rate)
                fr_list = freshness_vec(deltas)
                writer.writerow([j, i, ",".join(str(f) for f in fr_list)])


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif argc == 1:
        input_file = r"prova.txt"
        output_file = r"prova.csv"
    else:
        exit("Uso: python3 freshness_relations.py <input_file> <output_file>")

    compute_freshness_relation(input_file, output_file)
