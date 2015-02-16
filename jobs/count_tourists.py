__author__ = 'davide'

import os.path as osp
import glob

if __name__ == "__main__":
    folder = "/home/davide/Scaricati"  # percorso cartella dove sono i file
    N = "0"  # id della citta' da contare

    count = 0

    for file_ in glob.glob(osp.join(folder, "*_T.txt")):
        with open(file_) as fh:
            for line in fh:
                line = line.strip()
                if line.split()[-1] == N:
                    count += 1

    print("Conteggio totale relativo alla citta'", N, "=", count)