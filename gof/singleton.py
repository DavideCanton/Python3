__author__ = 'davide'


class Prova:
    __instance = None

    def __new__(cls):
        if not Prova.__instance:
            Prova.__instance = super(Prova, cls).__new__(cls)
            Prova.__instance.__initData()
        return Prova.__instance

    def __initData(self):
        self.l = []

    def append(self, n):
        self.l.append(n)


o1 = Prova()
o1.append(10)
o2 = Prova()
o2.append(30)
o3 = Prova()
o3.append(50)
print(o1.l)
print(o2.l)
print(o3.l)
print(o1 is o2 is o3)