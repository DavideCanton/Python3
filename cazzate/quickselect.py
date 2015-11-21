import random

__author__ = 'Davide'


def partition(list_, left, right, pivot_pos):
    pivot = list_[pivot_pos]
    list_[left], list_[pivot_pos] = list_[pivot_pos], list_[left]

    l, r = left + 1, right - 1
    while l < r:
        while l < right and list_[l] <= pivot:
            l += 1
        while r > left and list_[r] > pivot:
            r -= 1
        if l < r:
            list_[l], list_[r] = list_[r], list_[l]

    list_[r], list_[left] = list_[left], list_[r]
    return r


def quickselect(list_, k):
    list_ = list_[:]
    left = 0
    right = len(list_) - 1

    while True:
        pivot_pos = random.randint(left, right)
        pivot_pos = partition(list_, left, right + 1, pivot_pos)

        if k == pivot_pos:
            return list_[k]
        elif k < pivot_pos:
            right = pivot_pos - 1
        else:
            left = pivot_pos + 1


def median(list_):
    len_list = len(list_)
    if len_list % 2 == 1:
        return quickselect(list_, len_list // 2)
    else:
        return (quickselect(list_, len_list // 2) +
                quickselect(list_, len_list // 2 + 1)) // 2


def main():
    l = list(range(10))
    random.shuffle(l)

    print(l)
    print(median(l))


if __name__ == "__main__":
    main()
