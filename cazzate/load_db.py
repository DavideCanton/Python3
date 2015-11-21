import sqlite3
import json


def load_pin_data():
    conn = sqlite3.connect(r"C:\Users\Davide\Documents\db stuff\data.db")

    conn.execute("""CREATE TABLE IF NOT EXISTS PINS (
    number INT PRIMARY KEY,
    name VARCHAR(255),
    value INT,
    class VARCHAR(255),
    brand VARCHAR(50),
    info1 TEXT,
    levels INT,
    limits DOUBLE,
    tinpin TEXT,
    howtoget TEXT,
    spec TEXT,
    reboot DOUBLE,
    psych VARCHAR(255),
    info2 TEXT,
    boot DOUBLE)""")

    for i in range(1, 305):
        s = str(i).rjust(3, '0')
        print(s)

        with open(
                r"C:\Users\Davide\Documents\db stuff\d_{}.txt".format(s)) as f:
            # transaction
            with conn:
                data = json.load(f)
                data = [int(data["Number"]),
                        data["Name"],
                        int(data["Value"][2:].replace(",", "")),
                        data.get("Class", ""),
                        data["Brand"],
                        data["Info 1"],
                        int(data["Levels"]),
                        float(data.get("Limit", "-1").split()[0]),
                        data["Tin Pin"],
                        data["How to get"],
                        data.get("Spec", ""),
                        float(data["Reboot"][:-1]),
                        data["Psych"],
                        data["Info 2"],
                        float(data.get("Boot", "-1 ")[:-1])]

                conn.execute(
                    "INSERT INTO PINS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    data)


def load_evolutions():
    conn = sqlite3.connect(r"C:\Users\Davide\Documents\db stuff\data.db")

    conn.execute("""CREATE TABLE IF NOT EXISTS EVOLUTIONS(
    id_ INTEGER PRIMARY KEY AUTOINCREMENT,
    id1 INT,
    id2 INT,
    evtype TEXT,
    FOREIGN KEY(id1) REFERENCES PINS(number),
    FOREIGN KEY(id2) REFERENCES PINS(number)
    )""")

    with open(r"C:\Users\Davide\Documents\db stuff\pin_ev.csv") as f:
        with conn:
            for line in f:
                data = line.strip().split(";")
                ev_type, id1, id2 = data[1:4]

                conn.execute(
                    "INSERT INTO EVOLUTIONS VALUES (NULL,?,?,?)",
                    [int(id1), int(id2), ev_type])


if __name__ == "__main__":
    load_evolutions()