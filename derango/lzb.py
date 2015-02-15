# coding=utf-8
import collections
import string


class LZ_77:
    def __init__(self, lsb, llab):
        """Creates a LZ77 encoder/decoder with a search buffer of length lsb
        and a look-ahead buffer of length llab"""
        self.lsb = lsb
        self.llab = llab
        #creates empty buffers
        self.sb = collections.deque([None] * self.lsb, maxlen=self.lsb)
        self.lab = []
        self.dsb = collections.deque([None] * self.lsb, maxlen=self.lsb)

    def _search_longest_match(self, sb, lab):
        """Computes the longest match between the search buffer and the
        look-ahead buffer (they may overlap), returns the starting index
        of the match and the length of the match"""
        i = len(sb) - 1
        max_i, max_s = i + 1, 0
        #questa parte e' inefficiente ma e' il modo piu' semplice
        #per fare il matching
        while i >= 0:
            if sb[i] == lab[0]:
                j = i
                try:
                    while (j - i < len(lab) - 1 and
                           j < self.lsb and
                           sb[j] == lab[j - i]):
                        j += 1
                    if j >= self.lsb:
                        while (j - i < len(lab) - 1 and
                               j < self.lsb + len(lab) and
                               lab[j - self.lsb] == lab[j - i]):
                            j += 1
                except IndexError:
                    print(i, j)
                j -= i
                if j == len(lab) - 1:
                    return len(sb) - i, j
                elif j > max_s:
                    max_i, max_s = i, j
            i -= 1
        return len(sb) - max_i, max_s

    def feed_encode(self, ch):
        """Sends the character byte ch to the encoder"""
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
        """Ends the encoding returning all the matches left until the
        look-ahead buffer is empty"""
        while self.lab:
            d, l = self._search_longest_match(self.sb, self.lab)
            c = self.lab[l]
            i = l + 1
            self.sb.extend(self.lab[:i])
            self.lab = self.lab[i:]
            yield d, l, c

    def feed_decode(self, p):
        """Decodes a portion of the string using the triple p"""
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
        return b"".join(map(lambda i: bytes([i]), lab))


class LZ_78:
    def __init__(self):
        """Creates a LZ78 encoder/decoder"""
        self.dictionary = {}
        self.last = 1
        self.w = b""
        self.d = [b""]

    def feed_encode(self, k):
        """Encodes the character byte k"""
        k = bytes([k])
        if self.w + k in self.dictionary:
            self.w += k
        else:
            if self.w in self.dictionary:
                t = self.dictionary[self.w]
            else:
                t = (0, k)
            self.dictionary[self.w + k] = (self.last, t[0], k)
            self.last += 1
            self.w = b""
            return t[0], k

    def end(self):
        """Ends the encoding with the last tuple"""
        if self.w:
            t = self.dictionary[self.w]
            yield (t[1], t[2])

    def feed_decode(self, t):
        """Decodes the tuple t"""
        n, k = t
        s = self.d[n] + k
        self.d.append(s)
        return s


class LZ_W:
    def __init__(self, symb_list):
        """Creates a LZW encoder/decoder using the symbol table symb_list
        (array of character bytes)"""
        self.dictionary = {}
        last = 0
        for last, symbol in enumerate(symb_list, start=1):
            self.dictionary[symbol] = (last, None)
        self.last = last + 1
        self.w = b""
        self.d = [b""] + list(symb_list)
        self.old = -1

    def feed_encode(self, k):
        """Encodes the character byte k"""
        k = bytes([k])
        if self.w + k in self.dictionary:
            self.w += k
        else:
            if self.w in self.dictionary:
                t = self.dictionary[self.w]
            else:
                t = (0, k)
            self.dictionary[self.w + k] = (self.last, t[0])
            self.last += 1
            self.w = k
            return t[0]

    def end(self):
        """Ends the encoding with the last byte char"""
        if self.w:
            t = self.dictionary[self.w]
            yield t[0]

    def feed_decode(self, n):
        """Decodes the byte n"""
        if self.old < 0:
            self.old = n
            return self.d[n]
        if n < len(self.d):
            s = self.d[n]
            o = bytes([s[0]])
            self.d.append(self.d[self.old] + o)
        else:
            o = self.d[self.old]
            oi = bytes([o[0]])
            s = o + oi
            self.d.append(s)
        self.old = n
        return s


def main():
    input_string = input("Stringa>")

    # --- LZ77 ---
    #seach_buf_len = int(input("Search buffer di>"))
    #lookahead_buf_len = int(input("Look-ahead buffer di>"))
    #encoder = LZ_77(seach_buf_len, lookahead_buf_len)

    # --- LZ78 ---
    #encoder = LZ_78()

    # --- LZW ---
    chs = list(map(lambda i: bytes([i]), range(256)))
    encoder = LZ_W(chs)

    encoding = []
    for byte_char in input_string.encode():
        encoded = encoder.feed_encode(byte_char)
        if encoded is not None:
            encoding.append(encoded)

    #if encoder has the end() attribute, call the end() function to get
    #the last tuple
    if hasattr(encoder, 'end'):
        last_tuples = encoder.end()
        if last_tuples:
            for tuple_ in last_tuples:
                encoding.append(tuple_)

    #Print encoding
    print(" ".join(map(str, encoding)))

    #check if decoding is correct
    decoded_chars = [encoder.feed_decode(t) for t in encoding]
    decoded_string = b"".join(decoded_chars).decode()
    print(decoded_string)
    print("Risultato corretto?", input_string == decoded_string)

if __name__ == "__main__":
    main()