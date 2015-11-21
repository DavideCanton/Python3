import re
import pathlib
import itertools as it
import string

__author__ = 'Davide'


def mySplit(phrase):
    def grouper(c):
        if c in string.punctuation:
            return "P"
        if c in string.whitespace:
            return "S"
        return "L"

    return ["".join(g) for (k, g) in it.groupby(phrase, grouper)]


def capitalize_words(title):
    ret = "".join(map(str.capitalize, mySplit(title)))
    # handle 's
    return ret.replace("'S", "'s")


class T:
    def __init__(self, funcs):
        self.funcs = funcs

    def __le__(self, iterable):
        return tuple(f(x) for (x, f) in zip(iterable, self.funcs))


def load_titles(file_path):
    titles = {1: {}}
    serie = 1

    with file_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                serie += 1
                titles[serie] = {}
            else:
                data = line.split(" | ")
                funcs = T([int, capitalize_words, capitalize_words])
                number, eng_title, it_title = funcs <= data
                titles[serie][number] = "{} ({})".format(eng_title, it_title)

    return titles


def extract_number(episode_name):
    match = re.search(r"\d+x(\d+)", episode_name)
    if match:
        return int(match.group(1))
    match = re.search(r"S\d+E(\d+)", episode_name)
    if match:
        return int(match.group(1))
    raise ValueError("Can't find episode name!")


def main():
    series = [5]
    titles = load_titles(pathlib.Path("files/bb_titles.txt"))

    root = pathlib.Path(r"C:\Users\Davide\Videos\Breaking Bad")
    for serie in series:
        folder = root / "{} serie".format(serie)
        if not folder.exists():
            continue

        for episode in folder.iterdir():
            number = extract_number(episode.name)
            title = titles[serie][number]

            new_name = "Breaking Bad - {}x{:02} - {}".format(serie, number,
                                                             title)

            prompt = "Vuoi rinominare {} in {}?".format(episode, new_name)
            if input(prompt).lower() in {"s", "y", ""}:
                try:
                    episode.rename(episode.with_name(new_name))
                except Exception as e:
                    print("Can't rename. Error: {}".format(e))


if __name__ == "__main__":
    main()
