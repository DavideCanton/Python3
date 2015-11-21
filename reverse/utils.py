__author__ = 'Davide'


def compare_on(field):
    def f(cls):
        setattr(cls, "__eq__",
                lambda self, other: getattr(self, field) == getattr(other,
                                                                    field))
        setattr(cls, "__ne__",
                lambda self, other: getattr(self, field) != getattr(other,
                                                                    field))
        setattr(cls, "__gt__",
                lambda self, other: getattr(self, field) > getattr(other,
                                                                   field))
        setattr(cls, "__lt__",
                lambda self, other: getattr(self, field) < getattr(other,
                                                                   field))
        setattr(cls, "__ge__",
                lambda self, other: getattr(self, field) >= getattr(other,
                                                                    field))
        setattr(cls, "__le__",
                lambda self, other: getattr(self, field) <= getattr(other,
                                                                    field))
        return cls

    return f
