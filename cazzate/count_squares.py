import itertools as it


def is_square(path):
    if len(set(path)) != 4:
        return False

    path = sorted(path)
    path[-2], path[-1] = path[-1], path[-2]

    if (path[0][0] != path[1][0] or path[1][1] != path[2][1] or
                path[2][0] != path[3][0] or path[3][1] != path[0][1]):

        return False

    l = abs(path[0][1] - path[1][1])

    if abs(path[1][0] - path[2][0]) != l:
        return False

    if abs(path[2][1] - path[3][1]) != l:
        return False

    if abs(path[3][0] - path[0][0]) != l:
        return False

    print("Square {} with edge length {}".format(path, l))

    return True


def main():
    vertexes = {(i, j) for i in range(0, 9, 2) for j in range(0, 9, 2)}
    vertexes |= {(1, 3), (1, 5), (3, 3), (3, 5)}
    vertexes |= {(5, 3), (5, 5), (7, 3), (7, 5)}

    squares = [path for path in it.combinations(vertexes, 4) if is_square(path)]

    cnt = len(squares)

    print("Squares: {}".format(cnt))
    print(squares[0])


if __name__ == "__main__":
    main()
