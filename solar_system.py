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
# Main drawing turtle
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
# Planet class (WITH LABEL)
# =========================
class Planet:
    def __init__(self, name, color, size, orbit_radius, speed):
        self.name = name
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.shapesize(size / 10)
        self.t.penup()

        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.color("white")
        self.label.penup()

        self.orbit_radius = orbit_radius
        self.speed = speed
        self.angle = random.randint(0, 360)

    def move(self):
        x = self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.orbit_radius * math.sin(math.radians(self.angle))
        self.t.goto(x, y)

        # Position label slightly above planet
        self.label.goto(x, y + 12)
        self.label.clear()
        self.label.write(self.name, align="center", font=("Arial", 8, "normal"))

        self.angle += self.speed * TIME_SCALE

# =========================
# Draw Sun
# =========================
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(3)
sun.penup()
sun.goto(0, 0)

sun_label = turtle.Turtle()
sun_label.hideturtle()
sun_label.color("white")
sun_label.penup()
sun_label.goto(0, -35)
sun_label.write("Sun", align="center", font=("Arial", 10, "bold"))

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
# Draw legend
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
# Draw background
# =========================
draw_stars()
for p in planets:
    draw_orbit(p.orbit_radius)

draw_legend()

# =========================
# Animation loop
# =========================
def animate():
    for p in planets:
        p.move()
    screen.update()
    screen.ontimer(animate, 30)

animate()
screen.mainloop()
