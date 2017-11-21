import turtle
import time

t = turtle

t.right(180)
c = ['red', 'white', 'red', 'blue']
for i in range(4):
    t.color("", c[i])
    t.begin_fill()
    t.penup()
    t.goto(0, (150 - i*50))
    t.pendown()
    t.circle((200 - i*50), 360)
    t.end_fill()

t.color("", "white")
t.begin_fill()
t.left(108)
for i in range(5):
    t.forward(95.1)
    t.right(144)
t.end_fill()
