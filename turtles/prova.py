from turtle import *
from math import sqrt


def dist(x, y):
    return sqrt(sum((i - j) ** 2 for i, j in zip(x, y)))


turtle = Turtle()
turtle.color('red', 'yellow')
turtle.begin_fill()
pos = turtle.position()
for i in range(0, 100):
    turtle.forward(10 * i + 20)
    turtle.left(200)
    if dist(turtle.position(), pos) <= 1E-8:
        break
turtle.end_fill()
done()
