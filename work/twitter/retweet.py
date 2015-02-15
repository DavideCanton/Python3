from collections import defaultdict
import re
import os
import os.path

U_RE = re.compile("^U\s+(?:.+/)*(\w+)")
RT_RE = re.compile("^W\s+RT\s+@(\w+)")


def load_mapping(mapping_path):
    mapping = {}
    with open(mapping_path) as mapp_file:
        print("Generating mapping from ", mapping_path, "...", sep="")
        for index, line in enumerate(mapp_file):
            line_splitted = line.split()
            mapping[line_splitted[1]] = line_splitted[0]
            if index and index % 1000000 == 0:
                print("Processed", index, "rows.")
        print("End of mapping generation.")
    return mapping


def load_rt(rt_folder, mapping):
    retweets = defaultdict(set)
    retweeter = None

    counter = 0
    for rt_path in os.listdir(rt_folder):
        if not rt_path.endswith("txt"):
            continue
        print("Reading from", rt_path)
        with open(os.path.join(rt_folder, rt_path), errors="ignore") as rt_file:
            for line in rt_file:
                if line[0] == "U":
                    match = U_RE.match(line)
                    if not match:
                        print(line)
                    retweeter = mapping.get(match.group(1))
                elif line[0] == "W":
                    match = RT_RE.match(line)
                    if not match:
                        continue
                    original_tweeter = mapping.get(match.group(1))
                    if not original_tweeter or not retweeter:
                        continue
                    retweets[original_tweeter].add(retweeter)
                    counter += 1
                    if counter and counter % 1000000 == 0:
                        print("Inserted", counter, "retweets.")
    return retweets


def map_topology(topology_path, out_path, out2_path, retweets):
    chunk_size = 1 << 29
    print("Generating subset topology.")
    edge_buffer = defaultdict(list)
    not_sources = set()

    with open(topology_path) as topology_file:
        with open(out_path, "w", buffering=chunk_size) as out_file:
            with open(out2_path, "w", buffering=chunk_size) as out2_file:
                for index, line in enumerate(topology_file):
                    followee, follower = line.split()
                    if followee in retweets:
                        # ha ricevuto almeno un retweet
                        flag = follower in retweets[followee]

                        # memorizzo l'arco follower --flag--> followee
                        edge_buffer[follower].append((followee, flag))
                        # followee non e' un nodo source
                        not_sources.add(followee)

                        # se followee era nel buffer, ora che so che non e' source
                        # posso scrivere tutti gli archi uscenti da lui (e toglierli dal buffer)
                        if followee in edge_buffer:
                            for (follower_k, flag_f) in edge_buffer.pop(followee):
                                print(followee, follower_k, int(flag_f), file=out_file)
                                print(follower_k, followee, int(flag_f), file=out2_file)

                    if index and index % 1000000 == 0:
                        print("Read", index, "rows.")

                # processo i rimanenti nel buffer
                while edge_buffer:
                    followee, values = edge_buffer.popitem()
                    # se il nodo non e' source, vado a scrivere gli archi uscenti da lui
                    if followee in not_sources:
                        for (follower, flag) in values:
                            print(followee, follower, int(flag), file=out_file)
                            print(follower, followee, int(flag), file=out2_file)
                        not_sources.remove(followee)


if __name__ == "__main__":
    mapping_path = r"/mnt/DATA/DATA/TwitterKwak/numeric2screen"
    topology_path = r"/mnt/DATA/DATA/TwitterKwak/twitter_rv.net"
    rt_folder = r"/mnt/DATA/DATA/Twitter - 50millions Tweets/Filtered(RT_Only)"

    # out_file1 conterra' follower followee flag
    out_file1 = r"/mnt/DATA/DATA/TwitterKwak/follower_followee_flag"
    # out_file2 conterra' followee follower flag
    out_file2 = r"/mnt/DATA/DATA/TwitterKwak/followee_follower_flag"

    mapping = load_mapping(mapping_path)
    retweets = load_rt(rt_folder, mapping)
    del mapping
    map_topology(topology_path, out_file1, out_file2, retweets)