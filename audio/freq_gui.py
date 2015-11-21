import numpy as np
import struct
import wave
from audio.draw_animated_bars import animate

CHUNK = 1 << 10
MAX_H = 500


def read_chunk(f, chunk_size, ch):
    data = f.readframes(chunk_size)
    if not data:
        return None
    return np.array(struct.unpack('{n}h'.format(n=chunk_size * ch), data))


def generate(fn):
    f = wave.open(fn)
    ch = f.getnchannels()
    sw = f.getsampwidth()
    data = read_chunk(f, CHUNK // 2, ch)
    buf_len = data.shape[0]
    buf = np.r_[np.zeros(buf_len), data]

    while True:
        data = read_chunk(f, CHUNK // 2, ch)
        buf[:buf_len] = data
        buf = np.roll(buf, buf_len)
        w = np.fft.fft(buf)[:CHUNK]
        yield np.abs(w)


if __name__ == "__main__":
    fn = r"D:\Roba\music\07 - Racecars.wav"
    plt, _ = animate(lambda: generate(fn), CHUNK, MAX_H, 500)
    plt.show()
