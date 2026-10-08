import turtle as t, math as m, time

s = t.Screen()
s.setup(700, 700)
s.bgcolor("black")
s.tracer(0)

p = t.Turtle()
p.hideturtle()
p.pencolor("blue")
p.width(1)

arms = 11
steps = 70

for j in range(steps):
    t_val = j / steps
    r_dist = 30 + 225 * (t_val ** 0.9)
    cr = 22 * ((1 - t_val) ** 0.85) + 1.8
    
    for i in range(arms):
        a0 = 2 * m.pi * i / arms
        angle = a0 + 1.8 * (t_val ** 1.2) - 0.4 * m.sin(m.pi * t_val)
        
        x = r_dist * m.cos(angle)
        y = r_dist * m.sin(angle)
        
        p.penup()
        p.goto(x, y - cr)
        p.setheading(0)
        p.pendown()
        p.circle(cr)
        
    s.update()
    time.sleep(0.025)

t.done()