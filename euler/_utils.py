import heapq as hq


def genera_primi():
    yield 2
    todel = [(4, 2)]
    n = 3
    while True:
        if todel[0][0] != n:
            yield n
            hq.heappush(todel, (n * n, n))
        else:
            while todel[0][0] == n:
                p = todel[0][1]
                hq.heapreplace(todel, (n + p, p))
        n += 1
