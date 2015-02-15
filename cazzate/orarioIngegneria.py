from urllib import request
import re
import time
import winsound
import datetime

path = ("http://www.ingegneria.unical.it/"
        "webingegneria/areastudenti/orario/"
        "sistema_provvisorio/Specialistica/25.xls")
regex = re.compile("2012(\s)*-(\s)*2013")

while True:
    resp = request.urlopen(path)
    content = resp.read().decode("ascii", errors="ignore")
    now = datetime.datetime.now()
    if regex.search(content):
        print("{}> Orari usciti!".format(now))
        winsound.Beep(300, 1000)
        exit()
    else:
        print("{}> Niente...".format(now))
    time.sleep(600)
