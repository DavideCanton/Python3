import csv
from luckers_functions import dsa
import numpy
import sys
from luckers_functions import parser

def compute_activity_relation(file_in, file_out):
    row_buffer = None
    with open(file_out, "w", newline="") as out_file , open(file_in, "r", newline="") as in_file: 
        writer = csv.writer(out_file, delimiter=";")
        writer.writerow(["userid", "follower_id", "activity_relation"])        

        # lettura file
        # Finche' non si arriva alla fine del file...
        while row_buffer != []:
            _ , interaction_info, row_buffer = parser.parse_next_user(in_file, row_buffer)
            for (j, i), interactions in interaction_info.items():                
                # Si ordina la lista di coppie rispetto ai timestamps di interazione
                posts = [t[2] for t in sorted(interactions)]
                if len(posts) > 1:    
                    pointsD = dsa.derivate(posts)  
                    # threshold
                    eps = numpy.std(pointsD)
                    # lista dei segmenti
                    seg = dsa.segmentation(pointsD, eps)
                    # lista delle coppie (pendenza, lunghezza segmento)
                    appr = dsa.approx(seg)
                    filled = dsa.fill(appr)
                    pairs = ",".join(str(t[1]) for t in filled)
                    writer.writerow([j, i, pairs])
                    
if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif argc == 1:
        input_file = r"..."
        output_file = r"..."
    else:
        exit("Uso: python3 activity_relations.py <input_file> <output_file>")
    
    compute_activity_relation(input_file, output_file)
