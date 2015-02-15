__author__ = 'davide'

from turtle import *

turtle = Turtle()
turtle.color('red', 'yellow')
turtle.begin_fill()
pos = turtle.position()

turtle.left(90)
turtle.circle(100, 180)
turtle.left(90)
turtle.penup()
turtle.forward(400)
turtle.pendown()
turtle.left(90)
turtle.circle(100, 180)
turtle.left(90)
turtle.penup()

turtle.end_fill()
done()
