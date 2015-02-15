__author__ = 'Davide'

LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def is_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def incr(cur_date):
    cur_date[2] += 7
    month_len = LENGTHS[cur_date[1] - 1]
    if cur_date[1] == 2:
        month_len += int(is_leap(cur_date[0]))
    if cur_date[2] > month_len:
        cur_date[2] -= month_len
        cur_date[1] += 1
    if cur_date[1] > 12:
        cur_date[1] = 1
        cur_date[0] += 1


def main():
    cur_date = [1901, 1, 6]
    end_date = [2000, 12, 31]

    cnt = 0
    while cur_date <= end_date:
        if cur_date[2] == 1:
            cnt += 1
        incr(cur_date)

    print(cnt)


def main2():
    import datetime

    count = sum(datetime.datetime(y, m, 1).weekday() == 6
                for y in range(1901, 2001)
                for m in range(1, 13))

    print(count)


if __name__ == "__main__":
    main()
