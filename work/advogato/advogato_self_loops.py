__author__ = 'Kami'

import re
from collections import Counter

if __name__ == "__main__":
    dataset_path = r"complete-dataset"
    out_file = r"advogato_self_loops"

    # pinto,zhp	080903#151#J,###,080911#401#J,###,090228#1453#J

    pattern = re.compile(r'^\s*(\w+)\s*,\s*\1\s+([\w#,]+)')

    c = Counter()

    with open(dataset_path) as file_in:
        with open(out_file, "w") as file_out:
            for line in file_in:
                m = pattern.match(line)
                if m:
                    user = m.group(1)
                    certs = "".join(s[-1] for s in m.group(2).split(","))
                    print(user, certs, file=file_out)
                    if certs[-1] not in "AJMO#":
                        print(line)
                    c[certs[-1]] += 1

    print(c)
    print(sum(c.values()))