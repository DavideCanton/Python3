__author__ = 'Kami'

import six

if six.PY2:
    six.print_("2")
else:
    six.print_("3")

s = six.moves.input("ciao>")
six.print_(s)