__author__ = 'davide'

import sqlite3
import pathlib
import os
import os.path


CHUNK_SIZE = 200


def to_str(path):
    parts = list(path.parts)
    parts[0] = parts[0][0]
    return "files_{}".format("_".join(parts))


def create_index(root_folder, filename):
    db_connection = sqlite3.connect(filename)
    root_folder = pathlib.Path(root_folder).resolve()
    name = to_str(root_folder)

    try:
        db_connection.execute('delete from {}'.format(name))
    except sqlite3.Error:
        pass

    db_connection.execute(
        'create table if not exists {} (name text primary key)'.format(name))
    insert_stat = "insert into {} values (?)".format(name)
    with db_connection:
        chunk = []
        inserted = 0
        for root, _, files in os.walk(str(root_folder)):
            for file_ in files:
                file_path = pathlib.Path(root, file_)
                relative = str(file_path.relative_to(root_folder))
                chunk.append([relative])
                inserted += 1
                if inserted % CHUNK_SIZE == 0:
                    print("Inseriti {} files".format(inserted))
                    db_connection.executemany(insert_stat, chunk)
                    chunk.clear()


def search(root_folder, pattern, db_path):
    connection = sqlite3.connect(db_path)
    root_folder = pathlib.Path(root_folder).resolve()
    name = to_str(root_folder)
    sql_pattern = pattern.replace('*', '%').replace('?', '_')
    query = 'select * from {} where name like ?'.format(name)
    for row in connection.execute(query, [sql_pattern]):
        yield row[0]


if __name__ == "__main__":
    # create_index(r"D:/Musica", r"D:/music_index.db")
    n = 0
    for n, match in enumerate(search(r"D:/Musica", "*ko*",
                                     r"D:/music_index.db")):
        print(match)
    print("Found", n, "matches.")