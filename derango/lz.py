# coding=utf-8
import collections

class LZ_77:
    def __init__(self, lsb, llab):
        self.lsb = lsb
        self.llab = llab
        self.sb = collections.deque([None] * self.lsb, maxlen=self.lsb)
        self.lab = []
        self.dsb = collections.deque([None] * self.lsb, maxlen=self.lsb)

    def _search_longest_match(self, sb, lab):
        i = len(sb) - 1
        max_i, max_s = i + 1, 0
        while i >= 0:
            if sb[i] == lab[0]:
                j = i
                while j - i < len(lab) - 1 and j < self.lsb and sb[j] == lab[j - i]:
                    j += 1
                if j >= self.lsb:
                    while j - i < len(lab) - 1 and j < self.lsb + len(lab) and lab[j - self.lsb] == lab[j - i]:
                        j += 1
                j -= i
                if j == len(lab):
                    return len(sb) - i, j
                else:
                    if j > max_s:
                        max_i, max_s = i, j
            i -= 1
        return len(sb) - max_i, max_s


    def feed_encode(self, ch):
        self.lab.append(ch)
        if len(self.lab) < self.llab:
            return None

        d, l = self._search_longest_match(self.sb, self.lab)
        c = self.lab[l]
        i = l + 1
        self.sb.extend(self.lab[:i])
        self.lab = self.lab[i:]
        return d, l, c

    def end(self):
        while self.lab:
            d, l = self._search_longest_match(self.sb, self.lab)
            c = self.lab[l]
            i = l + 1
            self.sb.extend(self.lab[:i])
            self.lab = self.lab[i:]
            yield d, l, c


    def feed_decode(self, p):
        d, l, c = p
        lab = []
        if l != 0:
            for i in range(-d, -d + l):
                if i >= 0:
                    lab.append(lab[i])
                else:
                    lab.append(self.dsb[i])
        lab.append(c)
        self.dsb.extend(lab)
        return "".join(lab)


class LZ_78:
    def __init__(self):
        self.dictionary = {}
        self.last = 1
        self.w = ""
        self.d = [""]

    def feed_encode(self, k):
        if self.w + k in self.dictionary:
            self.w += k
        else:
            if self.w in self.dictionary:
                t = self.dictionary[self.w]
            else:
                t = (0, k)
            self.dictionary[self.w + k] = (self.last, t[0], k)
            self.last += 1
            self.w = ""
            return t[0], k

    def feed_decode(self, t):
        n, k = t
        s = self.d[n] + k
        self.d.append(s)
        return s


class LZ_W:
    def __init__(self, symb_list):
        self.dictionary = {}
        last = 0
        for last, s in enumerate(symb_list, start=1):
            self.dictionary[s] = (last, None)
        self.last = last + 1
        self.w = ""
        self.d = [""] + list(symb_list)
        self.old = -1

    def feed_encode(self, k):
        if self.w + k in self.dictionary:
            self.w += k
        else:
            if self.w in self.dictionary:
                t = self.dictionary[self.w]
            else:
                t = (0, k)
            self.dictionary[self.w + k] = self.last, t[0]
            self.last += 1
            self.w = k
            return t[0]

    def feed_decode(self, n):
        if self.old < 0:
            self.old = n
            return self.d[n]
        if n < len(self.d):
            s = self.d[n]
            self.d.append(self.d[self.old] + s[0])
        else:
            o = self.d[self.old]
            s = o + o[0]
            self.d.append(s)
        self.old = n
        return s


def main():
    input_string = input("Stringa>")

    #LZ77
    #seach_buf_len = int(input("Search buffer di>"))
    #lookahead_buf_len = int(input("Look-ahead buffer di>"))
    #encoder = LZ_77(seach_buf_len, lookahead_buf_len)

    #LZ78
    encoder = LZ_78()

    #LZW
    #chs = list(map(lambda i: bytes([i]), range(256)))
    #encoder = LZ_W(chs)

    encoding = []
    for ch in input_string:
        encoded = encoder.feed_encode(ch)
        if encoded is not None:
            encoding.append(encoded)

    #if encoder has the end() attribute, call the end() function to get
    #the last tuple
    if hasattr(encoder, 'end'):
        last_tuple = encoder.end()
        if last_tuple is not None:
            encoding.extend(list(last_tuple))

    #Print encoding
    print(" ".join(map(str, encoding)))

    decoded_chars = [encoder.feed_decode(t) for t in encoding]
    decoded_string = "".join(decoded_chars)
    print(decoded_string)
    print("Risultato corretto?", input_string == decoded_string)

if __name__ == "__main__":
    main()