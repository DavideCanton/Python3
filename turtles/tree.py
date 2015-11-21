__author__ = 'Davide'

import turtle

EDGES = 6
LEN = 200
ANGLE = 45


def tree(t, cnt, curLen):
    if cnt == 0:
        return
    curLen = max(curLen, 1)
    pos = t.pos()

    t.color("red")
    t.left(ANGLE)
    t.forward(curLen)
    t.right(ANGLE)
    t.dot(5)
    tree(t, cnt - 1, curLen / 2)

    t.up()
    t.goto(*pos)
    t.down()

    t.color("blue")
    t.right(ANGLE)
    t.forward(curLen)
    t.left(ANGLE)
    t.dot(5)
    tree(t, cnt - 1, curLen / 2)


def main():
    t = turtle.Turtle()
    turtle.mode("logo")
    t.screen.screensize(800, 600)
    t.up()
    t.goto(0, -300)
    t.down()
    tree(t, EDGES, LEN)
    turtle.done()

if __name__ == "__main__":
    main()