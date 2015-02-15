from functools import lru_cache

__author__ = 'Monia'

import csv
import os.path as osp
import numpy as np


SEPARATOR = "EOMinDoc"
SEPARATOR_DT = " "
GAMMA = 0.85
NTOPIC = 10
WEIGHT = [0.1] * NTOPIC

FOLDER = r"/home/davide/PycharmProjects/Python3/monia/twitter_rank/file/"
FILE_REL = osp.join(FOLDER, r"UserPosts-en_v2-cleaned/following-en_mapped.csv")
FILE_TWEETS = osp.join(FOLDER, r"UserPosts-en_v2-cleaned/UserPosts_doc2mat.txt")
FILE_OUT = osp.join(FOLDER, r"UserPosts-en_v2-cleaned/res_twitterRank_u.csv")
FILE_DT = osp.join(FOLDER, r"Res_lda_R/dt.csv")


def read_dt(file_dt):
    with open(file_dt) as dt_file:
        reader = csv.reader(dt_file, delimiter=SEPARATOR_DT)
        values = next(reader)
        dt = np.zeros((len(values), NTOPIC), dtype=np.uint32)

        for i, line in enumerate(reader):
            line = np.array([int(n) for n in line[1:]])
            dt[:, i] = line
    return dt


def read_relations(file_relations, n):
    relations = [[] for _ in range(n)]
    with open(file_relations) as f:
        for row in f:
            splitted = row.split("\t")
            follower, following = map(int, splitted[:2])
            relations[follower].append(following)

    relations = [np.array(el, dtype=np.uint32) for el in relations]
    return relations


def dt_acc(dt, tp):
    @lru_cache(maxsize=1000000)
    def wrapper(i):
        s = dt[i, :].sum()
        return 0 if np.allclose(s, 0) else float(dt[i, tp]) / s

    return wrapper


def compute_transition_prob(tp, num_tweets, relations, dt):
    docs = dt.shape[0]
    # p = np.zeros((docs,docs))
    p = np.memmap("/media/davide/OS/Users/Davide/Downloads/p_t.tmp",
                  dtype='float32', mode='w+', shape=(docs, docs))

    get_dt_val = dt_acc(dt, tp)

    for i in range(docs):
        dt_i_tp = get_dt_val(i)
        for j in range(i, docs):
            dt_j_tp = get_dt_val(j)
            den = num_tweets[relations[i]].sum()
            if not np.allclose(den, 0):
                s = 1 - abs(dt_i_tp - dt_j_tp)
                p[i, j] = p[j, i] = s * num_tweets[j] / den
    return p


def compute_twitter_rank_topic(tp, dt, num_tweets, relations):
    e_t = dt[:, tp]
    e_t = (1 - GAMMA) * e_t / e_t.sum()
    n = e_t.shape[0]

    p_t = compute_transition_prob(tp, num_tweets, relations, dt)

    col_sum = np.array(p_t.sum(0)).flatten()
    for i in range(n):
        if np.allclose(col_sum[i], 0):
            p_t[:, i] = 1. / n
        else:
            p_t[:, i] /= col_sum[i]

    tr_t_pre = np.ones_like(e_t) / n

    while True:
        tr_t = GAMMA * p_t.dot(tr_t_pre) + e_t

        if np.allclose(tr_t_pre, tr_t):
            return tr_t

        tr_t_pre = tr_t


def counter_num_tweet(file_tweet, separator):
    lengths = []
    with open(file_tweet) as tweet_file:
        for row in tweet_file:
            tweets = row.split(separator)
            lengths.append(len(tweets))
    return np.array(lengths, dtype=np.uint32)


def compute_twitter_rank(dt, num_tweets, relations):
    res = np.zeros(dt.shape[0])
    for ti, w in enumerate(WEIGHT):
        res += w * compute_twitter_rank_topic(ti, dt, num_tweets, relations)
        print("TwitterRank", ti, "calcolato")
    return res


def print_res(file_out, res):
    with open(file_out, "w") as out_file:
        for i, r in enumerate(res):
            print("{};{}".format(i, r), file=out_file)


if __name__ == "__main__":
    dt = read_dt(FILE_DT)
    print("Matrice DT letta")
    num_tweets = counter_num_tweet(FILE_TWEETS, SEPARATOR)
    print("Numero di tweet calcolato")
    relations = read_relations(FILE_REL, dt.shape[0])
    print("Topologia rete letta")
    res = compute_twitter_rank(dt, num_tweets, relations)
    print("TwitterRank Calcolato")
    print_res(FILE_OUT, res)