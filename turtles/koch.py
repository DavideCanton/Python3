__author__ = 'davide'

from turtle import *

DEPTH = 5


def koch(turtle, length, last):
    if last == 0:
        turtle.forward(length)
    else:
        l3 = length / 3
        koch(turtle, l3, last - 1)
        turtle.left(60)
        koch(turtle, l3, last - 1)
        turtle.right(120)
        koch(turtle, l3, last - 1)
        turtle.left(60)
        koch(turtle, l3, last - 1)


if __name__ == "__main__":
    turtle = Turtle()
    turtle.color('red', 'yellow')
    length = 500.0
    turtle.penup()
    turtle.backward(length / 2.0)
    turtle.left(90)
    turtle.forward(length / 4.0)
    turtle.right(90)
    turtle.pendown()

    turtle.begin_fill()
    for d in range(1, DEPTH + 1):
        turtle.speed(d * 10)
        for _ in range(3):
            koch(turtle, length, d)
            turtle.right(120)
    turtle.end_fill()
    done()
