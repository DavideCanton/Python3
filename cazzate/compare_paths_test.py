import os
import pathlib
from contextlib import suppress
from time import perf_counter as timer


def count_file_walk(path: pathlib.Path):
    count = 0

    for root, dirs, files in os.walk(str(path)):
        count += len(files)

    return count


def count_file_rec(path: pathlib.Path):
    count = 0

    with suppress(PermissionError):
        if path.is_dir():
            for d in path.iterdir():
                count += count_file_rec(d)
        elif path.is_file():
            count += 1

    return count


def count_file_scandir(path: pathlib.Path):
    count = 0

    for dir_entry in os.scandir(str(path)):
        if dir_entry.is_dir():
            for d in os.scandir(dir_entry.path):
                count += count_file_scandir(d)
        elif dir_entry.is_file():
            count += 1

    return count


def main():
    path = pathlib.Path(r"C:/Users/Davide/Pictures")

    cur = timer()
    n = count_file_walk(path)
    print("Walk:", n, "time:", timer() - cur)

    cur = timer()
    n = count_file_rec(path)
    print("Rec:", n, "time:", timer() - cur)

    cur = timer()
    n = count_file_scandir(path)
    print("Scandir:", n, "time:", timer() - cur)


if __name__ == "__main__":
    main()
