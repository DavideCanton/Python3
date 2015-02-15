from tkinter import tix, ttk
from tkinter.constants import *
import re
import itertools as it


class GUI(tix.Tk):
    def __init__(self, master=None):
        tix.Tk.__init__(self, master)
        self.title("Regex Matching")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.frame1 = ttk.Frame(self, relief=GROOVE, borderwidth=1, padding=5)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.grid(row=0, column=0, sticky=W + E)

        ttk.Label(self.frame1, text="Text:") \
            .grid(row=0, column=0, padx=10, pady=5)
        self.text = tix.StringVar()
        ttk.Entry(self.frame1, textvariable=self.text) \
            .grid(row=0, column=1, padx=10, sticky=W + E)
        ttk.Label(self.frame1, text="Regex:") \
            .grid(row=1, column=0, padx=10, pady=5)
        self.regex = tix.StringVar()
        ttk.Entry(self.frame1, textvariable=self.regex) \
            .grid(row=1, column=1, padx=10, sticky=W + E)

        self.frame2 = ttk.Frame(self, relief=GROOVE, borderwidth=1, padding=5)
        self.frame2.grid(row=1, column=0, sticky=NW + SE)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.varList = []
        self.spanList = []
        for i in range(10):
            ttk.Label(self.frame2, text="Group {}:".format(i)) \
                .grid(row=i, column=0, padx=10, pady=5)
            var = tix.StringVar()
            self.varList.append(var)
            span = tix.StringVar()
            self.spanList.append(span)
            ttk.Label(self.frame2, textvariable=var) \
                .grid(row=i, column=1, padx=10, sticky=W + E)
            ttk.Label(self.frame2, textvariable=span) \
                .grid(row=i, column=2, padx=10, sticky=W + E)
        ttk.Button(self.frame2, text="Start Match", command=self.startMatch) \
            .grid(row=10, column=0, columnspan=3, padx=10, sticky=W + E)

    def startMatch(self, *args):
        text = self.text.get()
        regex = self.regex.get()
        matches = re.finditer(regex, text)
        for v, s, m in it.zip_longest(self.varList, self.spanList, matches):
            if not m:
                v.set("")
                s.set("")
            else:
                if v is None:
                    break
                v.set(m.group())
                s.set("Start: {} End: {}".format(*m.span()))


g = GUI()
g.mainloop()
