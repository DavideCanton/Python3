import re


class Pokemon:
    def __init__(self, name="", parent=None, number=0):
        self.ev = []
        self.name = name
        self.parent = parent
        self.number = number

    def __repr__(self):
        return "<Pokemon Name:{} ev:{}>".format(self.name, self.ev)

    def __str__(self):
        return "<{}, {}>".format(self.number, self.name)


pattern = re.compile(r"^Evolve (?P<from>.+) \((?P<reason>.+)\)$")
format_table = "{}"

with open("pokedex.txt") as f:
    poke_dict = {}
    for line in f:
        number, name, ev = map(str.strip, line.split("\t", 2))
        number = int(number)
        name = re.sub(r"[\(\)]", "", name)
        this = poke_dict[name] = Pokemon(name=name, number=number)
        match = re.match(pattern, ev)
        if match:
            from_ev = match.group("from")
            reason = match.group("reason")
            if re.match("\d+", reason):
                reason = "Lv " + reason
            parent = poke_dict[from_ev]
            this.parent = parent
            parent.ev.append((reason, this))

    for pokemon in poke_dict.copy():
        if poke_dict[pokemon].parent:
            del poke_dict[pokemon]

    for p in sorted(poke_dict.values(), key=lambda t: t.number):
        s = p
        if len(p.ev) < 2:
            l = [str(p)]
            while p.ev:
                e = p.ev[0]
                l.append(format_table.format(e[0]))
                p = e[1]
                l.append(str(p))
            print("".join(l))
        else:
            # eevee
            for i in range(3):
                l = [str(p)]
                e = p.ev[i]
                l.append(format_table.format(e[0]))
                l.append(e[1].name)
                print("".join(l))
