from math import exp
import csv
import sys

def freshness_relation(rate, tc, tp):
    """
    Data il timestamp tc si vuole calcolare il valore di 
    freshness_relation rispetto a tp, estremo destro dell'intervallo
    preso in esame, e il rate che rappresenta la velocita' 
    di convergenza della funzione a 1
    """
    return 2 / (1 + exp(-rate * (tp - tc))) - 1

def compute_freshness(file_in, file_out, t_end):
    """
    A partire da file_in, in cui ogni riga contiene
    un userid piu' la lista di post da lui effettuati nel formato (timestamp,#fav), 
    si vuole calcolare per ogni utente 
    il valore di freshness_relation ad esso associato rispetto a t_end,
    e memorizzando il tutto in file_out
    """
    with open(file_in, "r", newline="") as in_file, open(file_out, "w", newline="") as out_file:
        reader = csv.reader(in_file, delimiter=";")
        writer = csv.writer(out_file, delimiter=";")
        
        #Salta la riga corrsipondente all'header del file
        iter_reader = iter(reader)
        next(iter_reader)
        
        writer.writerow(["userid", "freshness_relation"])
        for row in iter_reader:
            #Timestamp dell'azione piu' recente
            ts = get_last_timestamp(row[1])
            #freshness_relation
            f_ts = freshness_relation(1, ts, t_end)
            writer.writerow([row[0], f_ts])
                       
def get_last_timestamp(posts):
    """
    Data una stringa contenente una lista di post
    nel formato (timestamp,#fav), estrae il timestamp
    dell'ultima coppia (in quanto ordinati).
    """
    i = posts.rfind("(") + 1
    ts = 0
    while posts[i].isdigit():
        ts = ts * 10 + int(posts[i])
        i += 1
    return ts

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 4:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        t_end = sys.argv[3]
    elif argc == 1:
        input_file = r"..."
        output_file = r"..."
        t_end = 133
    else:
        exit("Uso: python3 freshness_relation.py <input_file> <output_file> <t_end>")
    try:
        t_end = int(t_end)
    except ValueError:
        exit("Valore di t_end non valido!")
    else:
        compute_freshness(input_file, output_file, t_end)
