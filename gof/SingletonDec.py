__author__ = 'davide'


def singleton(cls):
    instances = {}

    def wrapper():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return wrapper


@singleton
class C:
    def __init__(self):
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