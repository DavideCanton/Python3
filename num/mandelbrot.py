from PIL import Image
from multiprocessing.pool import Pool

WIDTH = 640
HEIGHT = 480
xa = -2.0
xb = 1.0
ya = -1.5
yb = 1.5
maxIt = 256


def draw_mandel(p):
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pix_map = img.load()

    for ky in range(HEIGHT):
        for kx in range(WIDTH):
            c = complex(xa + (xb - xa) * kx / WIDTH, ya + (yb - ya) * ky / HEIGHT)
            z = complex(0.0, 0.0)
            for i in range(maxIt):
                z = z ** p + c
                if abs(z) >= 2.0:
                    break
            rd = i % 4 * 64
            gr = i % 8 * 32
            bl = i % 16 * 16
            pix_map[kx, ky] = rd, gr, bl

    img.save("mandel/mandel_{}.gif".format(p))


if __name__ == "__main__":
    with Pool(processes=4) as pool:
        pool.map(draw_mandel, range(16))
    pool.join()