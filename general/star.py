import turtle as t, math as m, time

s = t.Screen(); s.setup(700, 700); s.bgcolor("black"); s.tracer(0)
p = t.Turtle(); p.hideturtle()
C = ["#ff0055", "#ff5500", "#ffcc00", "#33ff00", "#00ffcc", "#0066ff", "#9900ff", "#ff00cc"]

V = [((250 if i % 2 == 0 else 98) * m.cos(m.pi / 2 + i * m.pi / 5), 
      (250 if i % 2 == 0 else 98) * m.sin(m.pi / 2 + i * m.pi / 5)) for i in range(10)]
V.append(V[0])

targets = [(V[i][0] + (j / 10) * (V[i+1][0] - V[i][0]), V[i][1] + (j / 10) * (V[i+1][1] - V[i][1])) for i in range(10) for j in range(10)]

for i, (tx, ty) in enumerate(targets):
    col = C[i % len(C)]
    p.pencolor(col); p.width(1.2); p.penup(); p.goto(0, 0); p.pendown(); p.goto(tx, ty)
    
    p.pencolor("#ffffff" if i % 2 == 0 else col); p.width(1)
    for r in (0, 0.785, 1.57, 2.35):
        dx, dy = 5 * m.cos(r), 5 * m.sin(r)
        p.penup(); p.goto(tx - dx, ty - dy); p.pendown(); p.goto(tx + dx, ty + dy)
        
    s.update(); time.sleep(0.06)

s.update(); t.done()