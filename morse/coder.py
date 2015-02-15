__author__ = 'davide'

import pygame.mixer as pymixer
import pygame.time as pytime

SHORT, LONG = 1, 3


class Signal:
    __slots__ = ("length", "pause")

    def __init__(self, length=SHORT, pause=False):
        self.length = length
        self.pause = pause

    def __len__(self):
        return self.length

    def __str__(self):
        if self.pause:
            return " " * self.length
        else:
            return "." if self.length == SHORT else "-"


N = Signal(pause=True)
D = Signal()
L = Signal(length=LONG)

code = {
    'a': (D, L),
    'b': (L, D, D, D),
    'c': (L, D, L, D),
    'd': (L, D, D),
    'e': (D,),
    'f': (D, D, L, D),
    'g': (L, L, D),
    'h': (D, D, D, D),
    'i': (D, D),
    'j': (D, L, L, L),
    'k': (L, D, L),
    'l': (D, L, D, D),
    'm': (L, L),
    'n': (L, D),
    'o': (L, L, L),
    'p': (D, L, L, D),
    'q': (L, L, D, L),
    'r': (D, L, D),
    's': (D, D, D),
    't': (L,),
    'u': (D, D, L),
    'v': (D, D, D, L),
    'w': (D, L, L),
    'x': (L, D, D, L),
    'y': (L, D, L, L),
    'z': (L, L, D, D),
    '0': (L, L, L, L, L),
    '1': (D, L, L, L, L),
    '2': (D, D, L, L, L),
    '3': (D, D, D, L, L),
    '4': (D, D, D, D, L),
    '5': (D, D, D, D, D),
    '6': (L, D, D, D, D),
    '7': (L, L, D, D, D),
    '8': (L, L, L, D, D),
    '9': (L, L, L, L, D),
    '.': (D, L, D, L, D, L),
    ',': (L, L, D, D, L, L),
    ':': (L, L, L, D, D, D),
    '?': (D, D, L, L, D, D),
    '=': (L, D, D, D, L),
    '-': (L, D, D, D, D, L),
    '(': (L, D, L, L, D),
    ')': (L, D, L, L, D, L),
    '"': (D, L, D, D, L, D),
    "'": (D, L, L, L, L, D),
    '/': (L, D, D, L, D),
    '_': (D, D, L, L, D, L),
    '@': (D, L, L, D, L, D),
    '!': (L, D, L, D, L, L),
}

LETTER_PAUSE = (N,)
WORD_PAUSE = (N, N, N)
PHRASE_PAUSE = (N, N, N, N, N)


def encodeMessage(msg):
    encoded = []
    for word in msg.split():
        for letter in word:
            encoded.extend(code[letter.lower()])
            encoded.extend(LETTER_PAUSE)
        del encoded[-len(LETTER_PAUSE):]
        encoded.extend(WORD_PAUSE)
    del encoded[-len(WORD_PAUSE):]
    return encoded


def playAlphabet(sounds, msg):
    for signal in msg:
        delay = len(signal) * 1000
        if signal.pause:
            pytime.wait(delay)
        else:
            sound = sounds[0 if len(signal) == SHORT else 1]
            sound.play()
            pytime.delay(delay)
            sound.stop()


if __name__ == "__main__":
    pymixer.init()
    msg = "bruuuuu"
    encoded = encodeMessage(msg)
    morse = "".join([str(c) for c in encoded])
    print(morse)
    long_sound = pymixer.Sound("lungo.au")
    short_sound = pymixer.Sound("corto.au")
    playAlphabet((short_sound, long_sound), encoded)