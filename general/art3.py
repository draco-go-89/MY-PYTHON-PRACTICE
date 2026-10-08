import turtle
import math
import random
import colorsys

# ==============================================================================
# DISPLAY & CANVAS CONFIGURATION
# ==============================================================================
WIDTH, HEIGHT = 1000, 700
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("#020108")  # Obsidian cosmic void
screen.title("Twin Celestial Dragons of Yin & Yang // Sovereign Astral Ballet")
screen.colormode(255)
screen.tracer(0, 0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

hud = turtle.Turtle()
hud.hideturtle()
hud.speed(0)
hud.penup()

# ==============================================================================
# SHARED SIMULATION STATE & CELESTIAL PEARL
# ==============================================================================
class GlobalState:
    pearl_x = 0.0
    pearl_y = 0.0
    auto_dance = True
    dance_time = 0.0
    flash_energy = 0.0
    sparks = []

state = GlobalState()

# Particle system for celestial sparks & breath
class CelestialSpark:
    def __init__(self, x, y, vx, vy, hue, life=36):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.hue = hue
        self.life = life
        self.max_life = life

    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.94
        self.vy *= 0.94
        self.life -= 1
        return self.life > 0

def spawn_celestial_burst(x, y, count=40, palette="dual"):
    for _ in range(count):
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(5.0, 15.0)
        vx = math.cos(ang) * spd
        vy = math.sin(ang) * spd
        if palette == "solar":
            hue = random.choice([0.03, 0.08, 0.13])
        elif palette == "lunar":
            hue = random.choice([0.52, 0.62, 0.74])
        else:
            hue = random.choice([0.05, 0.12, 0.54, 0.72])
        state.sparks.append(CelestialSpark(x, y, vx, vy, hue, life=random.randint(22, 48)))

# ==============================================================================
# CELESTIAL DRAGON CLASS (YIN / YANG SKELETAL SYSTEM)
# ==============================================================================
NUM_VERTEBRAE = 52
SEG_LEN = 11.8

class CelestialDragon:
    def __init__(self, name, theme, phase_offset):
        self.name = name
        self.theme = theme  # 'solar' (Gold/Vermilion) or 'lunar' (Cyan/Violet)
        self.phase_offset = phase_offset

        # Vertebral positions
        self.spine_x = [-i * SEG_LEN for i in range(NUM_VERTEBRAE)]
        self.spine_y = [0.0 for _ in range(NUM_VERTEBRAE)]
        self.head_vx = 0.0
        self.head_vy = 0.0

    def update(self, global_time):
        # 1. Coupled Orbital Pursuit (Dancing around the Pearl in a double-helix)
        orbit_r = 75.0 + 20.0 * math.sin(global_time * 0.08)
        orbit_ang = global_time * 0.055 + self.phase_offset
        target_x = state.pearl_x + orbit_r * math.cos(orbit_ang)
        target_y = state.pearl_y + orbit_r * math.sin(orbit_ang)

        # 2. Smooth Heading Steering with Harmonic Serpentine Undulation
        dx = target_x - self.spine_x[0]
        dy = target_y - self.spine_y[0]
        dist = math.hypot(dx, dy)

        slither = 0.42 * math.sin(global_time * 0.20 + self.phase_offset)
        desired_heading = math.atan2(dy, dx) + slither

        spd = min(14.0, max(6.0, dist * 0.08))
        accel = 0.09
        self.head_vx += (math.cos(desired_heading) * spd - self.head_vx) * accel
        self.head_vy += (math.sin(desired_heading) * spd - self.head_vy) * accel

        self.spine_x[0] += self.head_vx
        self.spine_y[0] += self.head_vy

        # 3. Kinematic Relaxation Down the Spine
        for i in range(1, NUM_VERTEBRAE):
            seg_dist = SEG_LEN * (1.0 - 0.65 * (i / NUM_VERTEBRAE))
            vx = self.spine_x[i] - self.spine_x[i - 1]
            vy = self.spine_y[i] - self.spine_y[i - 1]
            d = math.hypot(vx, vy)
            if d == 0:
                d = 0.001

            norm_i = i / NUM_VERTEBRAE
            wave = 2.4 * math.sin(global_time * 0.22 - i * 0.28 + self.phase_offset) * norm_i
            nx, ny = -vy / d, vx / d

            self.spine_x[i] = self.spine_x[i - 1] + (vx / d) * seg_dist + nx * wave
            self.spine_y[i] = self.spine_y[i - 1] + (vy / d) * seg_dist + ny * wave

    def render(self, global_time):
        # ----------------------------------------------------------------------
        # A. DORSAL FLAME CREST & TRANSLUCENT FINS
        # ----------------------------------------------------------------------
        for i in range(NUM_VERTEBRAE - 1, 0, -1):
            x1, y1 = self.spine_x[i], self.spine_y[i]
            x0, y0 = self.spine_x[i - 1], self.spine_y[i - 1]
            dx, dy = x0 - x1, y0 - y1
            seg_dist = math.hypot(dx, dy)
            if seg_dist == 0:
                continue
            nx, ny = -dy / seg_dist, dx / seg_dist

            norm_i = i / NUM_VERTEBRAE
            body_radius = math.sin(norm_i * math.pi) * 22.0 * (1.0 - norm_i * 0.4)

            # Bioluminescent shockwave pulse
            wave_pos = (global_time * 0.45) % (NUM_VERTEBRAE * 1.3)
            pulse = math.exp(-0.4 * ((i - wave_pos) ** 2))
            energy = min(1.0, pulse + state.flash_energy)

            # Theme Palette
            if self.theme == "solar":
                base_hue = (0.02 + norm_i * 0.11 + global_time * 0.004) % 1.0
            else:
                base_hue = (0.54 + norm_i * 0.22 + global_time * 0.004) % 1.0

            val = min(1.0, 0.55 + norm_i * 0.45 + energy * 0.5)
            sat = max(0.12, 0.95 - energy * 0.85)
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(base_hue, sat, val)]
            pen.pencolor(r, g, b)

            # Dorsal Mane Spine Flutes
            if i % 2 == 0 and i < NUM_VERTEBRAE - 8:
                mane_h = body_radius * (1.8 + 0.4 * math.sin(i * 0.5 - global_time * 0.15))
                tip_x = x1 + nx * mane_h - (dx / seg_dist) * 10.0
                tip_y = y1 + ny * mane_h - (dy / seg_dist) * 10.0
                pen.pensize(max(1.0, (1.0 - norm_i) * 2.2))
                pen.penup()
                pen.goto(x1, y1)
                pen.pendown()
                pen.goto(tip_x, tip_y)
                pen.goto(x0, y0)

            # Lateral Rib Arcs
            pen.pensize(max(1.0, (1.0 - norm_i) * 2.5))
            for side in (-1, 1):
                pen.penup()
                pen.goto(x1, y1)
                pen.pendown()
                pen.goto(x1 + nx * side * body_radius, y1 + ny * side * body_radius)

        # ----------------------------------------------------------------------
        # B. BIG FAN TAIL & CURLING MICRO-SPIRALS
        # ----------------------------------------------------------------------
        tx, ty = self.spine_x[-1], self.spine_y[-1]
        tdx = self.spine_x[-1] - self.spine_x[-2]
        tdy = self.spine_y[-1] - self.spine_y[-2]
        tail_ang = math.atan2(tdy, tdx)

        # Big Silk Fan Plumes (7 Feathers)
        num_plumes = 7
        for p in range(num_plumes):
            frac_p = (p - (num_plumes // 2)) / (num_plumes // 2)
            p_ang = tail_ang + frac_p * 0.85
            plume_len = 55.0 - abs(frac_p) * 20.0
            p_hue = (base_hue + abs(frac_p) * 0.08) % 1.0
            pr, pg, pb = [int(c * 255) for c in colorsys.hsv_to_rgb(p_hue, 0.9, 0.95)]
            pen.pencolor(pr, pg, pb)
            pen.pensize(max(1.2, (1.0 - abs(frac_p)) * 2.8))

            pen.penup()
            pen.goto(tx, ty)
            pen.pendown()
            cpx, cpy = tx, ty
            for st in range(10):
                c_ang = p_ang + 0.14 * math.sin(global_time * 0.22 + st * 0.4)
                cpx += math.cos(c_ang) * (plume_len / 10.0)
                cpy += math.sin(c_ang) * (plume_len / 10.0)
                pen.goto(cpx, cpy)

        # Micro-Tails: 4 Logarithmic Golden Spirals curling to microscopic dots
        for sp_i in (-1.5, -0.5, 0.5, 1.5):
            pen.pensize(1)
            s_hue = (base_hue + sp_i * 0.04) % 1.0
            sr, sg, sb = [int(c * 255) for c in colorsys.hsv_to_rgb(s_hue, 0.8, 1.0)]
            pen.pencolor(sr, sg, sb)

            cx, cy = tx, ty
            s_ang = tail_ang + sp_i * 0.5
            rad = 22.0
            pen.penup()
            pen.goto(cx, cy)
            pen.pendown()
            for _ in range(24):
                s_ang += 0.34 * (1 if sp_i > 0 else -1)
                rad *= 0.92
                cx += math.cos(s_ang) * rad * 0.25
                cy += math.sin(s_ang) * rad * 0.25
                pen.goto(cx, cy)
            pen.dot(2.5, (255, 255, 255))

        # ----------------------------------------------------------------------
        # C. INCANDESCENT SPINAL LIGHTNING CORE
        # ----------------------------------------------------------------------
        pen.penup()
        pen.goto(self.spine_x[-1], self.spine_y[-1])
        pen.pendown()
        for i in range(NUM_VERTEBRAE - 1, -1, -1):
            norm_i = i / NUM_VERTEBRAE
            pen.pensize(max(1.5, (1.0 - norm_i) * 5.0))
            core_col = [int(c * 255) for c in colorsys.hsv_to_rgb(base_hue, 0.85, 1.0)]
            pen.pencolor(core_col)
            pen.goto(self.spine_x[i], self.spine_y[i])

        # White-Hot razor axis
        pen.pensize(1.2)
        pen.pencolor(255, 255, 255)
        pen.penup()
        pen.goto(self.spine_x[-1], self.spine_y[-1])
        pen.pendown()
        for i in range(NUM_VERTEBRAE - 1, -1, -2):
            pen.goto(self.spine_x[i], self.spine_y[i])

        # ----------------------------------------------------------------------
        # D. DRAGON HEAD, HORNS, WHISKERS & RADIANT EYES
        # ----------------------------------------------------------------------
        hx, hy = self.spine_x[0], self.spine_y[0]
        h_dir = math.atan2(self.spine_y[0] - self.spine_y[1], self.spine_x[0] - self.spine_x[1])
        ortho = h_dir + math.pi / 2.0

        # Cranial Aura
        pen.penup()
        pen.goto(hx, hy)
        if self.theme == "solar":
            pen.dot(32, (150, 25, 10))
            pen.dot(20, (255, 140, 20))
            eye_col = (255, 230, 40)
        else:
            pen.dot(32, (15, 30, 150))
            pen.dot(20, (30, 180, 255))
            eye_col = (140, 240, 255)
        pen.dot(10, (255, 255, 255))

        # Radiant Eyes
        for s in (-1, 1):
            ex = hx + math.cos(h_dir) * 5.0 + math.cos(ortho) * (s * 8.0)
            ey = hy + math.sin(h_dir) * 5.0 + math.sin(ortho) * (s * 8.0)
            pen.goto(ex, ey)
            pen.dot(5.5, eye_col)
            pen.dot(2, (255, 255, 255))

        # Stag Antlers
        for s in (-1, 1):
            pen.pensize(2.2)
            pen.pencolor(eye_col)
            rx = hx - math.cos(h_dir) * 3.0 + math.cos(ortho) * (s * 6.0)
            ry = hy - math.sin(h_dir) * 3.0 + math.sin(ortho) * (s * 6.0)
            pen.penup()
            pen.goto(rx, ry)
            pen.pendown()
            ha = h_dir + math.pi + s * 0.70
            mx = rx + math.cos(ha) * 24.0
            my = ry + math.sin(ha) * 24.0
            pen.goto(mx, my)
            # Fork
            pen.pensize(1.2)
            pen.goto(mx + math.cos(ha - s * 0.45) * 16.0, my + math.sin(ha - s * 0.45) * 16.0)

        # Long Sinuous Whiskers
        for s in (-1, 1):
            pen.pensize(1.2)
            wx = hx + math.cos(ortho) * (s * 6.0)
            wy = hy + math.sin(ortho) * (s * 6.0)
            pen.penup()
            pen.goto(wx, wy)
            pen.pendown()
            wa = h_dir + s * 0.35
            for seg in range(24):
                frac_w = seg / 24.0
                wa += 0.30 * math.sin(global_time * 0.22 - seg * 0.35) * s
                wx += math.cos(wa) * 7.5
                wy += math.sin(wa) * 7.5
                wr, wg, wb = [int(c * 255) for c in colorsys.hsv_to_rgb(base_hue, 0.8, 1.0 - frac_w * 0.35)]
                pen.pencolor(wr, wg, wb)
                pen.goto(wx, wy)
            pen.dot(3.0, (255, 255, 255))

# Initialize Dragons
dragon_yang = CelestialDragon("Yang (Solar)", "solar", phase_offset=0.0)
dragon_yin = CelestialDragon("Yin (Lunar)", "lunar", phase_offset=math.pi)

# ==============================================================================
# INTER-DRAGON TAIJI PLASMA BRIDGES (LIGHTNING LATTICE)
# ==============================================================================
def draw_taiji_plasma_bridges(global_time):
    pen.pensize(1.0)
    # Scan intermediate vertebrae for harmonic proximity
    for i in range(8, NUM_VERTEBRAE - 10, 3):
        x1, y1 = dragon_yang.spine_x[i], dragon_yang.spine_y[i]
        x2, y2 = dragon_yin.spine_x[i], dragon_yin.spine_y[i]
        dist = math.hypot(x2 - x1, y2 - y1)

        # If dragons pass close, energy arcs between their bodies
        if dist < 140.0:
            arc_alpha = 1.0 - (dist / 140.0)
            hue = (global_time * 0.02 + i * 0.04) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.75, arc_alpha)]
            pen.pencolor(r, g, b)

            # Curved plasma arc with mid-point harmonic wave
            mx = (x1 + x2) * 0.5 + 16.0 * math.sin(global_time * 0.3 + i)
            my = (y1 + y2) * 0.5 + 16.0 * math.cos(global_time * 0.3 + i)

            pen.penup()
            pen.goto(x1, y1)
            pen.pendown()
            pen.goto(mx, my)
            pen.goto(x2, y2)
            pen.dot(max(2.0, arc_alpha * 4.5), (255, 255, 255))

# ==============================================================================
# CELESTIAL PEARL (YIN-YANG ORBITAL CORE)
# ==============================================================================
def draw_celestial_pearl(global_time):
    px, py = state.pearl_x, state.pearl_y

    # Outer cosmic nebula aura
    pen.penup()
    pen.goto(px, py)
    pen.dot(42, (30, 15, 60))

    # Dual orbiting Yin-Yang sparks
    for idx, (hue, sign) in enumerate([(0.10, 1), (0.58, -1)]):
        ang = global_time * 0.14 * sign
        orb_x = px + 24.0 * math.cos(ang)
        orb_y = py + 24.0 * math.sin(ang)
        pen.goto(orb_x, orb_y)
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.9, 1.0)]
        pen.dot(10, (r, g, b))
        pen.dot(4, (255, 255, 255))

    # Incandescent pearl nucleus
    pen.goto(px, py)
    pen.dot(20, (255, 210, 150))
    pen.dot(9, (255, 255, 255))

# ==============================================================================
# TKINTER EVENT HOOKS (MOUSE PURSUIT & NOVA BURSTS)
# ==============================================================================
canvas = screen.getcanvas()

def on_mouse_move(event):
    state.pearl_x = event.x - WIDTH // 2
    state.pearl_y = (HEIGHT // 2) - event.y
    state.auto_dance = False

def on_left_click(event):
    state.flash_energy = 1.0
    spawn_celestial_burst(state.pearl_x, state.pearl_y, count=55, palette="dual")

def on_right_click(event):
    cx = event.x - WIDTH // 2
    cy = (HEIGHT // 2) - event.y
    spawn_celestial_burst(cx, cy, count=40, palette="solar")
    spawn_celestial_burst(cx, cy, count=40, palette="lunar")

def toggle_auto_dance():
    state.auto_dance = not state.auto_dance

canvas.bind("<Motion>", on_mouse_move)
canvas.bind("<ButtonPress-1>", on_left_click)
canvas.bind("<ButtonPress-3>", on_right_click)
screen.onkey(toggle_auto_dance, "space")
screen.listen()

# ==============================================================================
# HUD & STATS
# ==============================================================================
def draw_hud():
    hud.clear()
    hud.color("#5a4872")
    hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 35)
    hud.write("TWIN CELESTIAL DRAGONS // YIN & YANG BALLET", font=("Consolas", 11, "bold"))
    info = (
        f"Controls:\n"
        f"  [Move Mouse]     Direct the Dual-Chroma Pearl (Dragons Weave & Follow)\n"
        f"  [Left Click]     Celestial Yin-Yang Nova Flash\n"
        f"  [Right Click]    Stardust Vortex at Cursor\n"
        f"  [Space]          Auto Figure-8 Ballet: {'ON' if state.auto_dance else 'OFF'}\n\n"
        f"Vertebrae: 2x{NUM_VERTEBRAE} | Active Sparks: {len(state.sparks)}"
    )
    hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 170)
    hud.write(info, font=("Consolas", 9, "normal"))

# ==============================================================================
# MAIN RENDER LOOP (~60 FPS)
# ==============================================================================
def engine_loop():
    pen.clear()
    state.dance_time += 1.0
    t = state.dance_time

    # Auto dance figure-8 choreography
    if state.auto_dance:
        state.pearl_x = 280.0 * math.sin(t * 0.025)
        state.pearl_y = 170.0 * math.sin(t * 0.050)

    # 1. Update Physics
    dragon_yang.update(t)
    dragon_yin.update(t)

    # 2. Render Plasma Bridge & Dragons
    draw_taiji_plasma_bridges(t)
    dragon_yang.render(t)
    dragon_yin.render(t)

    # 3. Render Sparks & Pearl
    active_sparks = []
    for spk in state.sparks:
        if spk.step():
            active_sparks.append(spk)
            alpha = spk.life / spk.max_life
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(spk.hue, 0.9, alpha)]
            pen.penup()
            pen.goto(spk.x, spk.y)
            pen.dot(max(2.0, alpha * 6.0), (r, g, b))
    state.sparks = active_sparks

    draw_celestial_pearl(t)

    if state.flash_energy > 0:
        state.flash_energy = max(0.0, state.flash_energy - 0.04)

    draw_hud()
    screen.update()
    screen.ontimer(engine_loop, 16)

# Launch Sovereign Engine
engine_loop()
screen.mainloop()