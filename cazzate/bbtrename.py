__author__ = 'davide'

import pathlib
import re
from sys import stderr, argv

RE_EPISODE = re.compile(r"S(\d+)E(\d+)")
APOSTROFI = re.compile(r"(?<=L) (?=[AEIOU])")


def remove_trail_parts(parts):
    for i, el in enumerate(parts):
        if len(el) > 1 and all(str.isupper(s) for s in el[:2]):
            return parts[:i]
    return parts


if __name__ == "__main__":
    DIR = argv[1]
    # DIR = r"G:\The Big Bang Theory\8 serie"
    path = pathlib.Path(DIR)

    for filename in path.iterdir():
        if "The.Big.Bang" in filename.name:
            splitted = filename.name.split(".")
            extension = splitted[-1]

            # The.Big.Bang.Theory
            header = " ".join(splitted[:4])

            # NxN
            episode = splitted[4]
            if "x" not in episode:
                # S{NN}E{NN}
                m = RE_EPISODE.match(episode)
                episode = "{}x{:>02}".format(int(m.group(1)), int(m.group(2)))

            # Titolo e bla bla bla
            tail = " ".join(remove_trail_parts(splitted[5:]))
            # Apostrofi
            tail = re.sub(APOSTROFI, "'", tail)

            newname = "{}.{}".format(" - ".join([header, episode, tail]),
                                     extension)
            new_path = filename.parent / newname
            answer = input("Vuoi rinominare {} in {}?".format(filename,
                                                              new_path))
            if answer in "sSyY":
                try:
                    filename.rename(new_path)
                    print("OK!")
                except OSError as e:
                    print(e, file=stderr)


