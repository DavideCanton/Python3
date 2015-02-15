__author__ = 'Kami'

import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Console"

setup(  name = "FunctionalDep",
        version = "1.0",
        description = "FD Program By Kami!",
        options = {},
        executables = [Executable("main.py", base=base)])