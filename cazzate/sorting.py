__author__ = 'Kami'

import random


def selection_sort(v):
    for i in range(len(v)):
        cur_min = i
        for j in range(i + 1, len(v)):
            if v[j] < v[cur_min]:
                cur_min = j
        v[cur_min], v[i] = v[i], v[cur_min]


def bubble_sort(v):
    last_swap = len(v) - 1
    for i in range(len(v)):
        for j in range(last_swap):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                last_swap = j


def insertion_sort(v):
    for i in range(1, len(v)):
        val = v[i]
        j = i - 1
        while j >= 0 and v[j] > val:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = val


def merge_sort(v):
    def merge_sort_aux(v, i, j):
        if i < j:
            m = (i + j) // 2
            merge_sort_aux(v, i, m)
            merge_sort_aux(v, m + 1, j)
            merge(v, i, m, j)

    return merge_sort_aux(v, 0, len(v) - 1)


def merge(v, i, m, j):
    aux = [0] * (j - i + 1)

    i1, i2, i3 = i, m + 1, 0

    while i1 <= m and i2 <= j:
        if v[i1] <= v[i2]:
            aux[i3] = v[i1]
            i1 += 1
        else:
            aux[i3] = v[i2]
            i2 += 1
        i3 += 1

    while i1 <= m:
        aux[i3] = v[i1]
        i1 += 1
        i3 += 1
    while i2 <= j:
        aux[i3] = v[i2]
        i2 += 1
        i3 += 1

    v[i:j + 1] = aux


def natural_merge_sort(v):
    def merge_sort_aux(v, i, j):
        if i < j and any(v[x] > v[x + 1] for x in range(i, j)):
            m = (i + j) // 2
            merge_sort_aux(v, i, m)
            merge_sort_aux(v, m + 1, j)
            merge(v, i, m, j)

    return merge_sort_aux(v, 0, len(v) - 1)


if __name__ == "__main__":
    v = [random.randint(0, 20) for _ in range(10)]
    print(v)
    natural_merge_sort(v)
    print(v)