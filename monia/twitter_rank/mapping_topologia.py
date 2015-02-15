__author__ = 'Monia'
import csv


def compute_mapping_topology(file_tp, file_mp, file_out):
    with open(file_tp) as tp_file, open(file_mp) as mp_file, open(file_out, "w") as out_file:
        reader_mp = csv.reader(mp_file, delimiter=";")
        diz_id_user = {}
        for row in reader_mp:
            user = row[0]
            id_user = int(row[1])
            diz_id_user[user] = id_user
        for row in tp_file:
            splitted = row.split("\t")
            id_u1 = diz_id_user[splitted[0]]
            id_u2 = diz_id_user[splitted[1]]
            print("{}\t{}\t{}".format(id_u1, id_u2, splitted[2].strip()), file=out_file)


if __name__ == "__main__":
    file_in = r"/home/davide/Scaricati/TwitterRank/file/UserPosts-en_v2-cleaned/following-en.csv"
    file_out = r"/home/davide/Scaricati/TwitterRank/file/UserPosts-en_v2-cleaned/following-en_mapped.csv"
    file_mp = r"/home/davide/Scaricati/TwitterRank/file/UserPosts-en_v2-cleaned/userIDs.txt"

    compute_mapping_topology(file_in, file_mp, file_out)