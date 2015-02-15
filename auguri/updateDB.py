import sqlite3

conn = sqlite3.connect("sms_auguri.db")

with open("auguri.txt") as f:
    # transaction
    with conn:
        for line in f:
            name, date, *text = line.split(";")
            text = ";".join(text).strip()
            num = (text if text == "Voce" else "FB")
            conn.execute("insert into Auguri values (null,?,?,?,?)",
                         (name, num, text, date))
