__author__ = 'davide'


class Borg:
    _sh = {}

    def __init__(self):
        self.__dict__ = Borg._sh


class C(Borg):
    def __init__(self):
        super(C, self).__init__()
        if not hasattr(self, 'l'):
            self.l = []

    def m(self, n):
        self.l.append(n)


o1 = C()
o1.m(10)
o2 = C()
o2.m(30)
o3 = C()
o3.m(50)
print(o1.l)
print(o2.l)
print(o3.l)
print(o1 is o2 is o3)