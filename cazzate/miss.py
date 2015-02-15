class MyRubylikeThing:
    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            print("A missing method was called.")
            print("The object was %r, the method was %r. " % (self, name))
            print("It was called with %r and %r as arguments" % (args, kwargs))
        return _missing

    def m(self, h):
        print(h)


r = MyRubylikeThing()
r.hello("there", "world", also="bye")
r.m("no")