import turtle
import math
import random

# =========================
# Global time scale
# =========================
TIME_SCALE = 0.3

# =========================
# Screen setup
# =========================
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Solar System - Python Turtle")
screen.setup(width=1200, height=800)
screen.tracer(0)

# =========================
# Utility turtle
# =========================
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# =========================
# Draw stars
# =========================
def draw_stars(count=200):
    pen.color("white")
    for _ in range(count):
        pen.penup()
        pen.goto(
            random.randint(-600, 600),
            random.randint(-400, 400)
        )
        pen.dot(random.randint(1, 3))

# =========================
# Planet class (with label)
# =========================
class Planet:
    def __init__(self, name, color, size, orbit_radius, speed):
        self.name = name
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = random.randint(0, 360)

        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.shapesize(size / 10)
        self.t.penup()

        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.color("white")
        self.label.penup()

    def position(self):
        x = self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.orbit_radius * math.sin(math.radians(self.angle))
        return x, y

    def move(self):
        x, y = self.position()
        self.t.goto(x, y)

        self.label.goto(x, y + 12)
        self.label.clear()
        self.label.write(self.name, align="center", font=("Arial", 8, "normal"))

        self.angle += self.speed * TIME_SCALE

# =========================
# Sun
# =========================
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3)
sun.penup()

sun_label = turtle.Turtle()
sun_label.hideturtle()
sun_label.color("white")
sun_label.penup()
sun_label.goto(0, -35)
sun_label.write("Sun", align="center", font=("Arial", 10, "bold"))

# =========================
# Orbits
# =========================
def draw_orbit(radius):
    pen.penup()
    pen.goto(0, -radius)
    pen.pendown()
    pen.color("gray")
    pen.circle(radius)
    pen.penup()

# =========================
# Planets
# =========================
mercury = Planet("Mercury", "gray", 5, 60, 0.8)
venus   = Planet("Venus", "orange", 8, 90, 0.6)
earth   = Planet("Earth", "blue", 9, 120, 0.4)
mars    = Planet("Mars", "red", 7, 150, 0.3)
jupiter = Planet("Jupiter", "brown", 15, 200, 0.2)
saturn  = Planet("Saturn", "gold", 13, 250, 0.15)
uranus  = Planet("Uranus", "light blue", 11, 300, 0.1)
neptune = Planet("Neptune", "blue", 11, 350, 0.08)

planets = [
    mercury, venus, earth, mars,
    jupiter, saturn, uranus, neptune
]

# =========================
# Moon (orbits Earth)
# =========================
moon = turtle.Turtle()
moon.shape("circle")
moon.color("light gray")
moon.shapesize(0.4)
moon.penup()

moon_angle = random.randint(0, 360)
MOON_RADIUS = 20
MOON_SPEED = 2.5

# =========================
# Saturn rings
# =========================
rings = turtle.Turtle()
rings.hideturtle()
rings.color("#d8c690")
rings.penup()

def draw_saturn_rings(x, y):
    rings.clear()
    rings.goto(x, y - 5)
    rings.setheading(0)
    rings.pendown()
    rings.width(2)

    for size in range(18, 26, 2):
        rings.penup()
        rings.goto(x, y - size / 2)
        rings.pendown()
        rings.circle(size)
    rings.penup()

# =========================
# Legend
# =========================
def draw_legend():
    legend = turtle.Turtle()
    legend.hideturtle()
    legend.color("white")
    legend.penup()
    legend.goto(420, 300)
    legend.write("Solar System", font=("Arial", 14, "bold"))

    y = 260
    for p in planets:
        legend.goto(420, y)
        legend.write(f"• {p.name}", font=("Arial", 10, "normal"))
        y -= 20

# =========================
# Background
# =========================
draw_stars()
for p in planets:
    draw_orbit(p.orbit_radius)
draw_legend()

# =========================
# Animation
# =========================
def animate():
    global moon_angle

    for p in planets:
        p.move()

    # Moon orbiting Earth
    ex, ey = earth.position()
    mx = ex + MOON_RADIUS * math.cos(math.radians(moon_angle))
    my = ey + MOON_RADIUS * math.sin(math.radians(moon_angle))
    moon.goto(mx, my)
    moon_angle += MOON_SPEED * TIME_SCALE

    # Saturn rings
    sx, sy = saturn.position()
    draw_saturn_rings(sx, sy)

    screen.update()
    screen.ontimer(animate, 30)

animate()
screen.mainloop()
