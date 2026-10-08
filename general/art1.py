import turtle
import math
import colorsys

# ==============================================================================
# DISPLAY & CANVAS CONFIGURATION
# ==============================================================================
WIDTH, HEIGHT = 950, 950
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("#000000")  # Pitch black cosmic void[cite: 2]
screen.title("Cosmic Chronos Ring-Web // 3D Visualization")  #[cite: 2]
screen.colormode(255)
screen.tracer(0, 0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# Navigator turtle orbiting on the ring track[cite: 2]
nav = turtle.Turtle()
nav.shape("turtle")
nav.shapesize(1.2, 1.2, 2)
nav.color("#d8c88c", "#2d281e")  # Bronze/gold shell with dark body[cite: 2]
nav.penup()

hud = turtle.Turtle()
hud.hideturtle()
hud.speed(0)
hud.penup()

# ==============================================================================
# 3D CAMERA & INTERACTIVE STATE
# ==============================================================================
class Camera:
    # Euler orientation angles (Pitch, Yaw, Roll)
    rot_x = 0.45
    rot_y = -0.30
    rot_z = 0.0
    auto_spin = True
    time = 0.0

    camera_dist = 680.0
    viewport_scale = 560.0

    last_mouse_x = 0
    last_mouse_y = 0
    is_dragging = False

cam = Camera()

# ==============================================================================
# 3D MATRIX TRANSFORMATION & PERSPECTIVE PROJECTION
# ==============================================================================
def project_3d(x, y, z):
    """
    Applies 3D rotation matrices ro(a) followed by pinhole perspective projection[cite: 2].
    """
    # 1. Rotation around X-axis
    cx, sx = math.cos(cam.rot_x), math.sin(cam.rot_x)
    y1 = y * cx - z * sx
    z1 = y * sx + z * cx
    x1 = x

    # 2. Rotation around Y-axis
    cy, sy = math.cos(cam.rot_y), math.sin(cam.rot_y)
    x2 = x1 * cy + z1 * sy
    z2 = -x1 * sy + z1 * cy
    y2 = y1

    # 3. Rotation around Z-axis
    cz, sz = math.cos(cam.rot_z), math.sin(cam.rot_z)
    x3 = x2 * cz - y2 * sz
    y3 = x2 * sz + y2 * cz
    z3 = z2

    # Pinhole perspective division
    denom = cam.camera_dist - z3
    if denom < 10.0:
        denom = 10.0
    factor = cam.viewport_scale / denom
    return x3 * factor, y3 * factor, z3

# ==============================================================================
# 3D GEOMETRY DEFINITIONS
# ==============================================================================
NUM_LOBES = 6  #[cite: 2]
STRANDS_PER_LOBE = 14
LOBE_HUES = [0.92, 0.12, 0.55, 0.65, 0.78, 0.50]  # Spectral anchors[cite: 2]

def render_3d_toroidal_lobes():
    """Renders the 6 toroidal strand bundles rotating in 3D Euclidean space[cite: 2]."""
    pen.pensize(1.1)

    for lobe_idx in range(NUM_LOBES):
        base_phi = lobe_idx * (2.0 * math.pi / NUM_LOBES) + (math.pi / 2.0)
        base_hue = LOBE_HUES[lobe_idx]

        for s in range(STRANDS_PER_LOBE):
            t_frac = s / (STRANDS_PER_LOBE - 1)
            radius = 120.0 + s * 4.5
            dist_offset = 95.0 + s * 2.0

            # 3D Toroidal ring inclination
            tilt_angle = 0.35 * math.sin(base_phi * 2.0 + cam.time * 0.02)
            center_x = dist_offset * math.cos(base_phi)
            center_y = dist_offset * math.sin(base_phi)
            center_z = dist_offset * tilt_angle

            # Dynamic color gradient
            hue = (base_hue + (t_frac - 0.5) * 0.07 + cam.time * 0.002) % 1.0
            val = 0.60 + 0.40 * math.sin(t_frac * math.pi)
            sat = 0.85 - t_frac * 0.12
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, sat, val)]
            pen.pencolor(r, g, b)

            # Trace circle in 3D
            steps = 44
            first_pt = None
            for step in range(steps + 1):
                theta = step * (2.0 * math.pi / steps)
                # Local circle coordinate tilted around normal
                lx = center_x + radius * math.cos(theta) * math.cos(base_phi)
                ly = center_y + radius * math.cos(theta) * math.sin(base_phi)
                lz = center_z + radius * math.sin(theta)

                px, py, _ = project_3d(lx, ly, lz)

                if step == 0:
                    pen.penup()
                    pen.goto(px, py)
                    pen.pendown()
                    first_pt = (px, py)
                else:
                    pen.goto(px, py)

def render_3d_star_vortex():
    """Renders the nested rotating octagram vortex receding along the Z-axis[cite: 2]."""
    layers = 8
    order = 8
    step_skip = 3
    base_radius = 160.0

    for L in range(layers):
        r_scale = base_radius * (0.82 ** L)
        twist = L * 0.18 + cam.time * 0.015  # Continuous vortex spin
        depth_z = -L * 18.0  # Recedes inward creating a 3D gravitational funnel

        vertices = []
        for v in range(order):
            ang = v * (2.0 * math.pi / order) + twist
            vx = r_scale * math.cos(ang)
            vy = r_scale * math.sin(ang)
            vertices.append((vx, vy, depth_z))

        # Color progression from luminous champagne gold to electric cyan[cite: 2]
        if L < 2:
            star_color = (255, 235, 170)
            pen.pensize(1.6)
        elif L < 5:
            hue = (0.12 + L * 0.12 + cam.time * 0.005) % 1.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.70, 0.95)]
            star_color = (r, g, b)
            pen.pensize(1.2)
        else:
            star_color = (190, 240, 255)
            pen.pensize(1.0)

        pen.pencolor(star_color)

        curr = 0
        p0x, p0y, _ = project_3d(*vertices[curr])
        pen.penup()
        pen.goto(p0x, p0y)
        pen.pendown()

        for _ in range(order):
            curr = (curr + step_skip) % order
            px, py, _ = project_3d(*vertices[curr])
            pen.goto(px, py)

def render_boundary_rings_and_singularity():
    """Renders 3D concentric framing rings and the central event horizon[cite: 2]."""
    guide_radii = [160, 125, 88, 62]
    for idx, gr in enumerate(guide_radii):
        pen.pensize(1.0)
        hue = (0.55 + idx * 0.08 + cam.time * 0.003) % 1.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.55, 0.85)]
        pen.pencolor(r, g, b)

        steps = 48
        for step in range(steps + 1):
            theta = step * (2.0 * math.pi / steps)
            px, py, _ = project_3d(gr * math.cos(theta), gr * math.sin(theta), 0)
            if step == 0:
                pen.penup()
                pen.goto(px, py)
                pen.pendown()
            else:
                pen.goto(px, py)

    # Central Singularity / Void[cite: 2]
    cx, cy, _ = project_3d(0, 0, -120)
    pen.penup()
    pen.goto(cx, cy)
    pen.dot(46, (0, 0, 0))  # Black hole interior[cite: 2]

    # White-cyan incandescent event horizon rim[cite: 2]
    pen.pensize(1.6)
    pen.pencolor(230, 245, 255)
    core_r = 24.0
    for step in range(37):
        theta = step * (2.0 * math.pi / 36)
        px, py, _ = project_3d(core_r * math.cos(theta), core_r * math.sin(theta), -120)
        if step == 0:
            pen.penup()
            pen.goto(px, py)
            pen.pendown()
        else:
            pen.goto(px, py)

def update_navigator_turtle():
    """Animates the navigator turtle orbiting along the lower-right cyan track in 3D[cite: 2]."""
    orbit_r = 150.0
    orbit_speed = 0.02
    t_angle = -0.65 + math.sin(cam.time * orbit_speed) * 0.25  # ~4 o'clock orbital arc[cite: 2]

    tx = orbit_r * math.cos(t_angle)
    ty = orbit_r * math.sin(t_angle)
    tz = 25.0 * math.sin(cam.time * 0.04)

    px, py, _ = project_3d(tx, ty, tz)

    # Tangent vector calculation for heading orientation
    dt = 0.01
    next_tx = orbit_r * math.cos(t_angle + dt)
    next_ty = orbit_r * math.sin(t_angle + dt)
    npx, npy, _ = project_3d(next_tx, next_ty, tz)
    heading_deg = math.degrees(math.atan2(npy - py, npx - px))

    nav.goto(px, py)
    nav.setheading(heading_deg)
    nav.showturtle()

# ==============================================================================
# TKINTER INTERACTIVE MOUSE & KEYBOARD BINDINGS
# ==============================================================================
canvas = screen.getcanvas()

def on_press(event):
    cam.last_mouse_x = event.x
    cam.last_mouse_y = event.y
    cam.is_dragging = True

def on_drag(event):
    if not cam.is_dragging:
        return
    dx = event.x - cam.last_mouse_x
    dy = event.y - cam.last_mouse_y
    cam.last_mouse_x = event.x
    cam.last_mouse_y = event.y

    # 3D Trackball Orbit
    cam.rot_y += dx * 0.008
    cam.rot_x += dy * 0.008

def on_release(event):
    cam.is_dragging = False

def on_scroll(event):
    delta = 0
    if hasattr(event, "delta") and event.delta != 0:
        delta = 25.0 if event.delta > 0 else -25.0
    elif event.num == 4:
        delta = 25.0
    elif event.num == 5:
        delta = -25.0
    cam.viewport_scale = max(200.0, min(1300.0, cam.viewport_scale + delta))

canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
canvas.bind("<MouseWheel>", on_scroll)
canvas.bind("<Button-4>", on_scroll)
canvas.bind("<Button-5>", on_scroll)

def toggle_spin():
    cam.auto_spin = not cam.auto_spin

def reset_view():
    cam.rot_x = 0.45
    cam.rot_y = -0.30
    cam.viewport_scale = 560.0

screen.onkey(toggle_spin, "space")
screen.onkey(reset_view, "r")
screen.listen()

# ==============================================================================
# HUD OVERLAY
# ==============================================================================
def draw_hud():
    hud.clear()
    hud.color("#564b73")
    hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 35)
    hud.write("COSMIC CHRONOS RING-WEB // 3D VISUALIZER", font=("Consolas", 11, "bold"))  #[cite: 2]
    info = (
        f"Controls:\n"
        f"  [Left Drag]      Rotate 3D Trackball\n"
        f"  [Scroll Wheel]   Zoom: {int(cam.viewport_scale)}\n"
        f"  [Space]          Auto-Rotation: {'ON' if cam.auto_spin else 'PAUSED'}\n"
        f"  [R]              Reset Perspective\n\n"
        f"Pitch: {math.degrees(cam.rot_x)%360:.1f}° | Yaw: {math.degrees(cam.rot_y)%360:.1f}°"
    )
    hud.goto(-WIDTH // 2 + 25, HEIGHT // 2 - 175)
    hud.write(info, font=("Consolas", 9, "normal"))

# ==============================================================================
# MAIN RENDER LOOP (~60 FPS)
# ==============================================================================
def render_frame():
    pen.clear()

    if cam.auto_spin and not cam.is_dragging:
        cam.rot_y += 0.007
        cam.time += 1.0

    render_3d_toroidal_lobes()
    render_3d_star_vortex()
    render_boundary_rings_and_singularity()
    update_navigator_turtle()
    draw_hud()

    screen.update()
    screen.ontimer(render_frame, 16)

# Launch 3D visualization engine
render_frame()
screen.mainloop()