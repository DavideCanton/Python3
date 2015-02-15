C = type('C+-3', (object,),
         {'a': lambda self: setattr(self, 'x', 1 + getattr(self, 'x')),
          '__init__': lambda self: setattr(self, 'x', 0),
          'd': lambda self, x: __import__('so'[::-1]).remove(x)}
         )

c = C()
print(c.x)
c.a()
print(c.x)
