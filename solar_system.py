import turtle
import math
import random

# =========================
# Screen setup
# =========================
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Solar System - Python Turtle")
screen.setup(width=1200, height=800)
screen.tracer(0)

# =========================
# Main drawing turtle
# =========================
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# =========================
# Draw stars
# =========================
def draw_stars(count=150):
    pen.color("white")
    for _ in range(count):
        pen.penup()
        pen.goto(
            random.randint(-600, 600),
            random.randint(-400, 400)
        )
        pen.dot(random.randint(1, 3))

# =========================
# Planet class
# =========================
class Planet:
    def __init__(self, color, size, orbit_radius, speed):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.shapesize(size / 10)
        self.t.penup()
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = random.randint(0, 360)

    def move(self):
        x = self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.orbit_radius * math.sin(math.radians(self.angle))
        self.t.goto(x, y)
        self.angle += self.speed

# =========================
# Draw Sun
# =========================
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3)
sun.penup()
sun.goto(0, 0)

# =========================
# Draw orbit paths
# =========================
def draw_orbit(radius):
    pen.penup()
    pen.goto(0, -radius)
    pen.pendown()
    pen.color("gray")
    pen.circle(radius)
    pen.penup()

# =========================
# Create planets
# =========================
mercury = Planet("gray", 5, 60, 4)
venus   = Planet("orange", 8, 90, 3)
earth   = Planet("blue", 9, 120, 2)
mars    = Planet("red", 7, 150, 1.6)
jupiter = Planet("brown", 15, 200, 1)
saturn  = Planet("gold", 13, 250, 0.8)
uranus  = Planet("light blue", 11, 300, 0.6)
neptune = Planet("blue", 11, 350, 0.5)

planets = [
    mercury,
    venus,
    earth,
    mars,
    jupiter,
    saturn,
    uranus,
    neptune
]

# =========================
# Draw background elements
# =========================
draw_stars()

for p in planets:
    draw_orbit(p.orbit_radius)

# =========================
# Animation loop
# =========================
while True:
    for p in planets:
        p.move()
    screen.update()
