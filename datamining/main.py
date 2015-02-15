__author__ = 'davide'

import Image

W = H = 16


def creaImg(bits, index):
    im = Image.new("L", (W, H), 255)
    pix = im.load()
    for i in range(W):
        for j in range(H):
            b = int(bits[i * 16 + j])
            pix[j, i] = (1 - b) * 255
    im.save(str(index) + ".png")

if __name__ == "__main__":
    with open("semeion2.arff") as f:
        for index, line in enumerate(f):
            if index >= 262:
                l = line.strip().split(", ")
                creaImg(l[:-1], index - 262)
                print("Scritta immagine", (index - 262))