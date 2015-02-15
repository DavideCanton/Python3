__author__ = 'Kami'

if __name__ == "__main__":
    dataset_path = r"complete-dataset"

    # pinto,zhp	080903#151#J,###,080911#401#J,###,090228#1453#J
    n_certs = 0
    tot = 0

    with open(dataset_path) as file_in:
        for line in file_in:
            certs = list(filter(lambda x: x != "###", line.split()[1].split(",")))
            if len(certs) > 1:
                n_certs += 1
            tot += 1

    print("Read dataset.")

    print(n_certs)
    print(n_certs / tot)