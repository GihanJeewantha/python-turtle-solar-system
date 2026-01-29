import turtle
import math
import random
from typing import List, Dict, Any

# =================================================================
# GLOBAL CONFIGURATION (Senior Practice: Centralized Settings)
# =================================================================
TIME_SCALE = 0.3
AU_PIXEL_SCALE = 100 

# =================================================================
# SCIENTIFIC DATA (Kept your original data, added orbital physics)
# =================================================================
PLANET_DATA = [
    {"name": "Mercury", "color": "gray",       "size": 5,  "a": 60,  "e": 0.205, "speed": 0.8},
    {"name": "Venus",   "color": "orange",     "size": 8,  "a": 90,  "e": 0.006, "speed": 0.6},
    {"name": "Earth",   "color": "blue",       "size": 9,  "a": 120, "e": 0.016, "speed": 0.4},
    {"name": "Mars",    "color": "red",        "size": 7,  "a": 150, "e": 0.093, "speed": 0.3},
    {"name": "Jupiter", "color": "brown",      "size": 15, "a": 200, "e": 0.048, "speed": 0.2},
    {"name": "Saturn",  "color": "gold",       "size": 13, "a": 250, "e": 0.056, "speed": 0.15, "rings": True},
    {"name": "Uranus",  "color": "light blue", "size": 11, "a": 300, "e": 0.047, "speed": 0.1},
    {"name": "Neptune", "color": "blue",       "size": 11, "a": 350, "e": 0.008, "speed": 0.08},
]

# =================================================================
# CLASSES
# =================================================================

class Planet:
    def __init__(self, data: Dict[str, Any]):
        self.name = data["name"]
        self.a = data["a"]          # Semi-major axis
        self.e = data["e"]          # Orbital Eccentricity
        self.base_speed = data["speed"]
        self.has_rings = data.get("rings", False)
        self.angle = random.randint(0, 360)

        # Drawing Turtle
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(data["color"])
        self.t.shapesize(data["size"] / 10)
        self.t.penup()

    def get_position(self) -> tuple:
        """Calculates elliptical coordinates using Kepler's First Law."""
        rad = math.radians(self.angle)
        # Polar equation for an ellipse: r = a(1-e^2) / (1 + e*cos(theta))
        r = (self.a * (1 - self.e**2)) / (1 + self.e * math.cos(rad))
        x = r * math.cos(rad)
        y = r * math.sin(rad)
        return x, y, r

    def update(self, label_pen: turtle.Turtle):
        x, y, r = self.get_position()
        self.t.goto(x, y)
        
        # Label Drawing
        label_pen.penup()
        label_pen.goto(x, y + 12)
        label_pen.write(self.name, align="center", font=("Arial", 8, "normal"))

        # Physics: Move faster at perihelion (Kepler's Second Law)
        # Velocity multiplier is inversely proportional to distance r
        velocity_mult = (self.a / r) ** 2
        self.angle += self.base_speed * TIME_SCALE * velocity_mult

class SolarSystem:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.title("Professional Keplerian Simulation")
        self.screen.setup(width=1200, height=800)
        self.screen.tracer(0)

        self.pen = turtle.Turtle(visible=False)
        self.label_pen = turtle.Turtle(visible=False)
        self.ring_pen = turtle.Turtle(visible=False)
        self.ring_pen.color("#d8c690")
        
        self.planets = [Planet(p) for p in PLANET_DATA]
        self.moon = self._setup_moon()
        self.moon_angle = random.randint(0, 360)
        
        self._draw_static_background()

    def _setup_moon(self) -> turtle.Turtle:
        m = turtle.Turtle()
        m.shape("circle")
        m.color("light gray")
        m.shapesize(0.4)
        m.penup()
        return m

    def _draw_static_background(self):
        """Draws elements that don't move every frame."""
        # Stars
        self.pen.color("white")
        for _ in range(200):
            self.pen.penup()
            self.pen.goto(random.randint(-600, 600), random.randint(-400, 400))
            self.pen.dot(random.randint(1, 3))
        
        # Orbits (Drawn as ellipses)
        self.pen.color("gray")
        for p in self.planets:
            self.pen.penup()
            # Draw a fine ellipse for the orbit
            for a in range(0, 361, 2):
                rad = math.radians(a)
                r = (p.a * (1 - p.e**2)) / (1 + p.e * math.cos(rad))
                self.pen.goto(r * math.cos(rad), r * math.sin(rad))
                self.pen.pendown()
            self.pen.penup()

        # Sun
        sun = turtle.Turtle(shape="circle")
        sun.color("yellow")
        sun.shapesize(3)
        sun.penup()
        self.pen.goto(0, -35)
        self.pen.color("white")
        self.pen.write("Sun", align="center", font=("Arial", 10, "bold"))

        # Legend
        self.pen.goto(420, 300)
        self.pen.write("Solar System", font=("Arial", 14, "bold"))
        y = 260
        for p in self.planets:
            self.pen.goto(420, y)
            self.pen.write(f"• {p.name}", font=("Arial", 10, "normal"))
            y -= 20

    def draw_rings(self, x, y):
        self.ring_pen.clear()
        self.ring_pen.width(2)
        for size in range(18, 26, 2):
            self.ring_pen.penup()
            self.ring_pen.goto(x, y - size / 2)
            self.ring_pen.setheading(0)
            self.ring_pen.pendown()
            self.ring_pen.circle(size)

    def animate(self):
        self.label_pen.clear()
        self.label_pen.color("white")
        
        for p in self.planets:
            p.update(self.label_pen)
            if p.has_rings:
                px, py, _ = p.get_position()
                self.draw_rings(px, py)
        
        # Moon Logic
        earth = next(p for p in self.planets if p.name == "Earth")
        ex, ey, _ = earth.get_position()
        mx = ex + 20 * math.cos(math.radians(self.moon_angle))
        my = ey + 20 * math.sin(math.radians(self.moon_angle))
        self.moon.goto(mx, my)
        self.moon_angle += 2.5 * TIME_SCALE

        self.screen.update()
        self.screen.ontimer(self.animate, 30)

# =================================================================
# MAIN ENTRY POINT
# =================================================================
if __name__ == "__main__":
    simulation = SolarSystem()
    simulation.animate()
    turtle.mainloop()