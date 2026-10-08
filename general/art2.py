import turtle
import math
import random
import colorsys
from collections import deque

# ==============================================================================
# DISPLAY & CANVAS CONFIGURATION
# ==============================================================================
WIDTH, HEIGHT = 900, 750
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("#030106")  # Imperial lacquer night void
screen.title("Imperial Celestial Loong // Chinese Dragon & Flaming Pearl Engine")
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
# KINEMATIC SPINE & SIMULATION STATE
# ==============================================================================
NUM_SEGMENTS = 85        # Length of the serpentine body
SEG_BASE_LEN = 11.5      # Distance between vertebrae

# Initialize spine coordinates
spine_x = [-i * SEG_BASE_LEN for i in range(NUM_SEGMENTS)]
spine_y = [0.0 for _ in range(NUM_SEGMENTS)]

class DragonState:
    # Target (The Flaming Pearl of Wisdom)
    target_x = 180.0
    target_y = 100.0
    pearl_orbit_time = 0.0
    auto_pearl = True

    # Kinematics
    head_vx = 0.0
    head_vy = 0.0
    time = 0.0

    # Shaders / Effects
    flash_energy = 0.0
    breath_particles = []

state = DragonState()

# ==============================================================================
# EMBERS & FIRE BREATH PARTICLE SYSTEM
# ==============================================================================
class Spark:
    def __init__(self, x, y, vx, vy, hue, life=35):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.hue = hue
        self.life = life
        self.max_life = life

    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.93
        self.vy *= 0.93
        self.life -= 1
        return self.life > 0

def discharge_fire_breath(origin_x, origin_y, angle, count=28):
    for _ in range(count):
        spread = random.uniform(-0.5, 0.5)
        spd = random.uniform(6.0, 16.0)
        vx = math.cos(angle + spread) * spd
        vy = math.sin(angle + spread) * spd
        # Crimson to incandescent solar gold
        hue = random.choice([0.02, 0.06, 0.12, 0.15])
        state.breath_particles.append(Spark(origin_x, origin_y, vx, vy, hue, life=random.randint(20, 45)))

# ==============================================================================
# INVERSE KINEMATICS & SMOOTH CURSOR PURSUIT
# ==============================================================================
def update_physics():
    # 1. Update Pearl (Target) Position
    if state.auto_pearl:
        state.pearl_orbit_time += 0.022
        t = state.pearl_orbit_time
        state.target_x = 280.0 * math.cos(t) + 70.0 * math.sin(2.3 * t)
        state.target_y = 210.0 * math.sin(1.2 * t) + 80.0 * math.cos(2.8 * t)

    # 2. Smooth Steering Pursuit: Dragon hunts the Pearl
    dx = state.target_x - spine_x[0]
    dy = state.target_y - spine_y[0]
    dist = math.hypot(dx, dy)

    # Sinuous serpentine wave added to lateral navigation
    undulation = 0.45 * math.sin(state.time * 0.16)
    target_heading = math.atan2(dy, dx) + undulation

    # Acceleration with turning inertia
    max_speed = 13.5
    accel = 0.085
    target_vx = math.cos(target_heading) * max_speed
    target_vy = math.sin(target_heading) * max_speed

    state.head_vx += (target_vx - state.head_vx) * accel
    state.head_vy += (target_vy - state.head_vy) * accel

    spine_x[0] += state.head_vx
    spine_y[0] += state.head_vy

    # 3. Progressive Distance-Constraint Relaxation along Vertebrae
    for i in range(1, NUM_SEGMENTS):
        seg_dist = SEG_BASE_LEN * (1.0 - 0.70 * (i / NUM_SEGMENTS))

        vx = spine_x[i] - spine_x[i - 1]
        vy = spine_y[i] - spine_y[i - 1]
        d = math.hypot(vx, vy)
        if d == 0:
            d = 0.001

        # Traveling lateral wave along body
        norm_i = i / NUM_SEGMENTS
        wave = 2.6 * math.sin(state.time * 0.18 - i * 0.24) * norm_i
        nx = -vy / d
        ny = vx / d

        spine_x[i] = spine_x[i - 1] + (vx / d) * seg_dist + nx * wave
        spine_y[i] = spine_y[i - 1] + (vy / d) * seg_dist + ny * wave

# ==============================================================================
# RENDERING: THE CHINESE IMPERIAL DRAGON
# ==============================================================================
def draw_dragon():
    pen.clear()

    # --------------------------------------------------------------------------
    # 1. THE FLAMING PEARL OF WISDOM (HO-CHU) AT THE CURSOR
    # --------------------------------------------------------------------------
    px, py = state.target_x, state.target_y

    # Outer celestial fire halo
    halo_hue = (state.time * 0.02) % 1.0
    r_h, g_h, b_h = [int(c * 255) for c in colorsys.hsv_to_rgb(halo_hue, 0.8, 0.5)]
    pen.penup()
    pen.goto(px, py)
    pen.dot(34, (r_h, g_h, b_h))

    # Whirling flame wisps around pearl
    pen.pensize(1.2)
    for p_flame in range(4):
        p_ang = state.time * 0.12 + p_flame * (math.pi / 2.0)
        fx = px + 22.0 * math.cos(p_ang)
        fy = py + 22.0 * math.sin(p_ang)
        pen.pencolor(255, 180, 40)
        pen.penup()
        pen.goto(px, py)
        pen.pendown()
        pen.goto(fx, fy)

    # Core Pearl: hot gold & radiant white nucleus
    pen.penup()
    pen.goto(px, py)
    pen.dot(18, (255, 120, 20))
    pen.dot(10, (255, 235, 160))
    pen.dot(5, (255, 255, 255))

    # --------------------------------------------------------------------------
    # 2. PARTICLES & BREATH EMBERS
    # --------------------------------------------------------------------------
    surviving = []
    for spk in state.breath_particles:
        if spk.step():
            surviving.append(spk)
            alpha = spk.life / spk.max_life
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(spk.hue, 0.9, alpha)]
            pen.penup()
            pen.goto(spk.x, spk.y)
            pen.dot(max(2.0, alpha * 6.0), (r, g, b))
    state.breath_particles = surviving

    # --------------------------------------------------------------------------
    # 3. DORSAL FLAME CREST & IMPERIAL SCALES (VERMILION & GOLD)
    # --------------------------------------------------------------------------
    # Render from tail to head
    for i in range(NUM_SEGMENTS - 1, 0, -1):
        x1, y1 = spine_x[i], spine_y[i]
        x0, y0 = spine_x[i - 1], spine_y[i - 1]

        dx = x0 - x1
        dy = y0 - y1
        seg_dist = math.hypot(dx, dy)
        if seg_dist == 0:
            continue
        nx = -dy / seg_dist
        ny = dx / seg_dist

        norm_i = i / NUM_SEGMENTS
        # Body girth profile
        body_radius = math.sin(norm_i * math.pi) * 26.0 * (1.0 - norm_i * 0.4)

        # Traveling bioluminescent flame shockwave
        wave_pos = (state.time * 0.45) % (NUM_SEGMENTS * 1.4)
        dist_wave = abs(i - wave_pos)
        pulse = math.exp(-0.35 * (dist_wave ** 2))
        total_energy = min(1.0, pulse + state.flash_energy)

        # Traditional Chinese palette: Imperial Gold -> Vermilion Crimson -> Solar Yellow
        base_hue = (0.01 + norm_i * 0.11 + state.time * 0.003) % 1.0
        val = min(1.0, 0.55 + norm_i * 0.45 + total_energy * 0.5)
        sat = max(0.1, 0.95 - total_energy * 0.85)
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(base_hue, sat, val)]
        pen.pencolor(r, g, b)

        # A. Dorsal Mane / Flame Spine Fins (Alternating peaks)
        if i % 2 == 0 and i < NUM_SEGMENTS - 12:
            flame_len = body_radius * (1.9 + 0.5 * math.sin(i * 0.4 - state.time * 0.15))
            f_tip_x = x1 + nx * flame_len - (dx / seg_dist) * 12.0
            f_tip_y = y1 + ny * flame_len - (dy / seg_dist) * 12.0

            pen.pensize(max(1.0, (1.0 - norm_i) * 2.5))
            pen.penup()
            pen.goto(x1, y1)
            pen.pendown()
            # Arched flame barb
            pen.goto(f_tip_x, f_tip_y)
            pen.goto(x0, y0)

        # B. Lateral Scale Arcs
        pen.pensize(max(1.0, (1.0 - norm_i) * 3.0))
        for side in (-1, 1):
            sc_x = x1 + nx * side * body_radius
            sc_y = y1 + ny * side * body_radius
            pen.penup()
            pen.goto(x1, y1)
            pen.pendown()
            pen.goto(sc_x, sc_y)

    # --------------------------------------------------------------------------
    # 4. BIG TAIL & MICRO-TAILS (GRAND FLAMING CAUDAL FAN & SPIRALS)
    # --------------------------------------------------------------------------
    tail_tip_x, tail_tip_y = spine_x[-1], spine_y[-1]
    tail_dx = spine_x[-1] - spine_x[-2]
    tail_dy = spine_y[-1] - spine_y[-2]
    tail_angle = math.atan2(tail_dy, tail_dx)

    # --- PART A: BIG TAIL (Sweeping Silk Flame Fan Plume) ---
    num_plume_ribbons = 9
    for p in range(num_plume_ribbons):
        frac_p = (p - (num_plume_ribbons // 2)) / (num_plume_ribbons // 2)
        spread_ang = tail_angle + frac_p * 0.85
        plume_len = 65.0 - abs(frac_p) * 25.0

        p_hue = (0.02 + abs(frac_p) * 0.10 + state.time * 0.01) % 1.0
        pr, pg, pb = [int(c * 255) for c in colorsys.hsv_to_rgb(p_hue, 0.9, 0.95)]
        pen.pencolor(pr, pg, pb)
        pen.pensize(max(1.2, (1.0 - abs(frac_p)) * 3.2))

        # Undulating silk plume curve
        pen.penup()
        pen.goto(tail_tip_x, tail_tip_y)
        pen.pendown()
        cur_px, cur_py = tail_tip_x, tail_tip_y
        for st in range(12):
            cur_ang = spread_ang + 0.15 * math.sin(state.time * 0.2 + st * 0.4)
            cur_px += math.cos(cur_ang) * (plume_len / 12.0)
            cur_py += math.sin(cur_ang) * (plume_len / 12.0)
            pen.goto(cur_px, cur_py)

    # --- PART B: SMALL TAILS (Delicate Curling Logarithmic Spirals) ---
    for spiral_idx in (-2, -1, 0, 1, 2):
        pen.pensize(1)
        s_hue = (0.08 + spiral_idx * 0.03 + state.time * 0.01) % 1.0
        sr, sg, sb = [int(c * 255) for c in colorsys.hsv_to_rgb(s_hue, 0.8, 1.0)]
        pen.pencolor(sr, sg, sb)

        cur_x, cur_y = tail_tip_x, tail_tip_y
        s_ang = tail_angle + spiral_idx * 0.55
        radius = 24.0
        pen.penup()
        pen.goto(cur_x, cur_y)
        pen.pendown()

        # Logarithmic spiral contraction: r = a * e^(b*theta)
        for _ in range(28):
            s_ang += 0.32 * (1 if spiral_idx >= 0 else -1)
            radius *= 0.92  # Shrinks to a microscopic point
            cur_x += math.cos(s_ang) * radius * 0.24
            cur_y += math.sin(s_ang) * radius * 0.24
            pen.goto(cur_x, cur_y)

        # Micro-dot spark at spiral apex
        pen.dot(2.5, (255, 235, 170))

    # --------------------------------------------------------------------------
    # 5. SPINAL LIGHTNING CORD (INCANDESCENT GOLD/WHITE SKELETON)
    # --------------------------------------------------------------------------
    pen.penup()
    pen.goto(spine_x[-1], spine_y[-1])
    pen.pendown()
    for i in range(NUM_SEGMENTS - 1, -1, -1):
        norm_i = i / NUM_SEGMENTS
        pen.pensize(max(1.8, (1.0 - norm_i) * 5.5))
        core_hue = (0.03 + norm_i * 0.10) % 1.0
        cr, cg, cb = [int(c * 255) for c in colorsys.hsv_to_rgb(core_hue, 0.85, 1.0)]
        pen.pencolor(cr, cg, cb)
        pen.goto(spine_x[i], spine_y[i])

    # White-hot razor cord
    pen.penup()
    pen.pensize(1.2)
    pen.pencolor(255, 255, 255)
    pen.goto(spine_x[-1], spine_y[-1])
    pen.pendown()
    for i in range(NUM_SEGMENTS - 1, -1, -2):
        pen.goto(spine_x[i], spine_y[i])

    # --------------------------------------------------------------------------
    # 6. DRAGON HEAD, STAG ANTLERS, BEARD & LONG WHISKERS
    # --------------------------------------------------------------------------
    hx, hy = spine_x[0], spine_y[0]
    head_dir = math.atan2(spine_y[0] - spine_y[1], spine_x[0] - spine_x[1])
    ortho_dir = head_dir + math.pi / 2.0

    # Luminous Cranial Core & Snout Aura
    pen.penup()
    pen.goto(hx, hy)
    pen.dot(36, (140, 20, 10))   # Crimson aura
    pen.dot(24, (255, 130, 20))  # Solar flame mid-skull
    pen.dot(12, (255, 245, 180)) # Incandescent nucleus

    # Snout Projection
    snout_x = hx + math.cos(head_dir) * 16.0
    snout_y = hy + math.sin(head_dir) * 16.0
    pen.goto(snout_x, snout_y)
    pen.dot(14, (200, 30, 15))

    # Fierce Glowing Golden Eyes
    for side in (-1, 1):
        eye_x = hx + math.cos(head_dir) * 6.0 + math.cos(ortho_dir) * (side * 9.0)
        eye_y = hy + math.sin(head_dir) * 6.0 + math.sin(ortho_dir) * (side * 9.0)
        pen.goto(eye_x, eye_y)
        pen.dot(6, (255, 220, 30))
        pen.dot(2.5, (255, 255, 255))

    # Stag Antlers (Branching Imperial Horns)
    for side in (-1, 1):
        pen.pensize(2.4)
        pen.pencolor(255, 200, 70)  # Polished imperial gold
        horn_root_x = hx - math.cos(head_dir) * 4.0 + math.cos(ortho_dir) * (side * 7.0)
        horn_root_y = hy - math.sin(head_dir) * 4.0 + math.sin(ortho_dir) * (side * 7.0)
        pen.penup()
        pen.goto(horn_root_x, horn_root_y)
        pen.pendown()

        h_ang = head_dir + math.pi + side * 0.70
        h_mid_x = horn_root_x + math.cos(h_ang) * 28.0
        h_mid_y = horn_root_y + math.sin(h_ang) * 28.0
        pen.goto(h_mid_x, h_mid_y)

        # Upper branch
        pen.pensize(1.4)
        b1_x = h_mid_x + math.cos(h_ang - side * 0.45) * 20.0
        b1_y = h_mid_y + math.sin(h_ang - side * 0.45) * 20.0
        pen.goto(b1_x, b1_y)

        # Secondary fork
        pen.penup()
        pen.goto(h_mid_x, h_mid_y)
        pen.pendown()
        b2_x = h_mid_x + math.cos(h_ang + side * 0.40) * 16.0
        b2_y = h_mid_y + math.sin(h_ang + side * 0.40) * 16.0
        pen.goto(b2_x, b2_y)

    # Long Undulating Sensory Whiskers (The Dragon's Barbels)
    for side in (-1, 1):
        pen.pensize(1.3)
        w_root_x = snout_x + math.cos(ortho_dir) * (side * 6.0)
        w_root_y = snout_y + math.sin(ortho_dir) * (side * 6.0)
        pen.penup()
        pen.goto(w_root_x, w_root_y)
        pen.pendown()

        cur_wx, cur_wy = w_root_x, w_root_y
        w_ang = head_dir + side * 0.35
        for seg in range(30):
            frac_w = seg / 30.0
            # Sinuous ribbon wave
            wave_w = 0.32 * math.sin(state.time * 0.22 - seg * 0.32)
            w_ang += wave_w * side
            cur_wx += math.cos(w_ang) * 8.5
            cur_wy += math.sin(w_ang) * 8.5

            wh_hue = (0.11 + frac_w * 0.08) % 1.0  # Radiant gold streamer
            wr, wg, wb = [int(c * 255) for c in colorsys.hsv_to_rgb(wh_hue, 0.85, 1.0 - frac_w * 0.35)]
            pen.pencolor(wr, wg, wb)
            pen.goto(cur_wx, cur_wy)

        # Spark at whisker tip
        pen.dot(3.0, (255, 255, 255))

    # Dissipate flash
    if state.flash_energy > 0:
        state.flash_energy = max(0.0, state.flash_energy - 0.04)

# ==============================================================================
# TKINTER INTERACTION (CURSOR FOLLOW, CLICKS, PEARL HUNTING)
# ==============================================================================
canvas = screen.getcanvas()

def on_mouse_move(event):
    # Convert window coordinates to Turtle centered space
    state.target_x = event.x - WIDTH // 2
    state.target_y = (HEIGHT // 2) - event.y
    state.auto_pearl = False  # Direct cursor control

def on_left_click(event):
    # Left Click: Unleash Fire Roar & Energy Flash
    state.flash_energy = 1.0
    head_dir = math.atan2(spine_y[0] - spine_y[1], spine_x[0] - spine_x[1])
    discharge_fire_breath(spine_x[0], spine_y[0], head_dir, count=45)

def on_right_click(event):
    # Right Click: Stardust Firework Nova at cursor
    cx = event.x - WIDTH // 2
    cy = (HEIGHT // 2) - event.y
    discharge_fire_breath(cx, cy, random.uniform(0, 2 * math.pi), count=50)

def toggle_auto_pearl():
    state.auto_pearl = not state.auto_pearl

canvas.bind("<Motion>", on_mouse_move)
canvas.bind("<ButtonPress-1>", on_left_click)
canvas.bind("<ButtonPress-3>", on_right_click)
screen.onkey(toggle_auto_pearl, "space")
screen.listen()

# ==============================================================================
# HUD & CONTROL MATRIX
# ==============================================================================
def draw_hud():
    hud.clear()
    hud.color("#7a5229")
    hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 35)
    hud.write("IMPERIAL CELESTIAL LOONG // CHINESE DRAGON ENGINE", font=("Consolas", 11, "bold"))
    info = (
        f"Controls:\n"
        f"  [Move Cursor]   Direct the Flaming Pearl of Wisdom (Dragon pursues)\n"
        f"  [Left Click]    Dragon Fire Breath Shockwave\n"
        f"  [Right Click]   Celestial Firework Nova at Cursor\n"
        f"  [Space]         Toggle Auto Orbit for Pearl: {'ON' if state.auto_pearl else 'OFF'}\n\n"
        f"Vertebrae: {NUM_SEGMENTS} | Sinuous Undulation: Active"
    )
    hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 170)
    hud.write(info, font=("Consolas", 9, "normal"))

# ==============================================================================
# MAIN ENGINE LOOP (~60 FPS)
# ==============================================================================
def engine_loop():
    state.time += 1.0
    update_physics()
    draw_dragon()
    draw_hud()
    screen.update()
    screen.ontimer(engine_loop, 16)

# Launch engine
engine_loop()
screen.mainloop()