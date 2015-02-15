__author__ = 'davide'


class Process:
    def begin(self):
        pass

    def do(self, files):
        self.begin()
        with open(files[-1], "w") as out:
            for fp in files[:-1]:
                with open(fp) as f:
                    self.process(f, out)
        self.end()

    def process(self, in_f, out_f):
        raise NotImplementedError

    def end(self):
        pass


class Uppercase(Process):
    def process(self, in_f, out_f):
        for line in in_f:
            out_f.write(line.upper())
        out_f.write("\n")


class Finder(Process):
    def begin(self):
        self.first = True

    def process(self, in_f, out_f):
        if self.first:
            self.words = [line.strip() for line in in_f]
            self.first = False
        else:
            for i, line in enumerate(in_f):
                line = line.strip()
                if line in self.words:
                    out_f.write("Trovata {} in {}:{}\n".format(line, in_f.name, i))


if __name__ == "__main__":
    p = Finder()
    p.do(["a.txt", "b.txt", "c.txt"])