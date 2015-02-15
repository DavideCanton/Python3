import collections
from urllib.request import urlopen
import re

__author__ = 'davide'

URL = "http://db.gamefaqs.com/portable/ds/file/chrono_trigger_ds_item.txt"

NAME_REGEX = "^Name: \d{3} (?P<name>.+?) \(.*$"
SHOP_REGEX = "^Shop(s|\(s\)): (?P<shop>.*)$"
CHESTS = "^Chests: (?P<chests>.*)$"
WON = "^Won: (?P<won>.*)$"
CHARM = "^Charm: (?P<charm>.*)$"

TARGET = [29, 33, 44, 47, 51, 64, 84, 95, 104, 105, 130, 142, 156,
          161, 162, 163, 164, 168, 175, 181, 190, 222, 223, 224, 225,
          226, 227]
Item = collections.namedtuple("Item", "name shop chests won charm")

u = urlopen(URL)
s = u.read().decode()
items = {}
current_item = {}
id = 1
for line in s.split("\r\n"):
    m = re.match(NAME_REGEX, line)
    if m:
        current_item['name'] = m.group("name")
        continue
    m = re.match(SHOP_REGEX, line)
    if m:
        current_item['shop'] = m.group("shop")
        continue
    m = re.match(CHESTS, line)
    if m:
        current_item['chests'] = m.group("chests")
        continue
    m = re.match(WON, line)
    if m:
        current_item['won'] = m.group("won")
        continue
    m = re.match(CHARM, line)
    if m:
        try:
            if 'name' not in current_item:
                raise ValueError
            current_item['charm'] = m.group("charm")
            if 'shop' not in current_item:
                current_item['shop'] = ''
            item = Item(**current_item)
            current_item = {}
            items[id] = item
            id += 1
        except ValueError:
            current_item = {}

for id in TARGET:
    d = items[id]._asdict()
    print("ITEM", id)
    for k, v in d.items():
        k = k[0].upper() + k[1:]
        print("{}: {}".format(k, v))
    print()