import numpy
import csv
import re
import sys
from luckers_functions import dsa

def compute_activity(file_in, file_out):
    """
    A partire da file_in, dove ogni riga contiene
    un userid piu' la lista di post da lui effettuati nel formato (timestamp,#fav), 
    si vuole calcolare per ogni utente una lista di valori 
    in cui ciascun valore rappresenta l'activity dell'utente 
    in un dato timestamp in cui ha svolto un'azione
    """
    with open(file_in, "r", newline="") as in_file, open(file_out, "w", newline="") as out_file:
        reader = csv.reader(in_file, delimiter=";")
        writer = csv.writer(out_file, delimiter=";")
        iter_reader = iter(reader)
        next(iter_reader)
        writer.writerow(["userid", "activity"])
        pattern = re.compile(r"\(\d+,(\d+)\)")
        for row in iter_reader:
            # lista del numero di azioni effettuate in ogni timestamp
            posts = [int(m.group(1)) for m in pattern.finditer(row[1])]  
            if len(posts) > 1:       
                # lista dei punti derivati  
                pointsD = dsa.derivate(posts)  
                # threshold
                eps = numpy.std(pointsD)
                # lista dei segmenti
                seg = dsa.segmentation(pointsD, eps)
                # lista delle coppie (pendenza, lunghezza segmento)
                appr = dsa.approx(seg)
                filled = dsa.fill(appr)
                pairs = ",".join(str(t[1]) for t in filled)
                writer.writerow([row[0], pairs])
 
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif argc == 1:
        input_file = r"D:\Universita\Lavoro\Flickr_favorites\favorites_timeseries"
        output_file = r"D:\Universita\Lavoro\Flickr_favorites\prova.csv"
    else:
        exit("Uso: python3 activity.py <input_file> <output_file>")
    
    compute_activity(input_file, output_file)

