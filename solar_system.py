import turtle
import math
import random
from typing import List, Dict, Any

# =================================================================
# GLOBAL CONFIGURATION
# =================================================================
TIME_SCALE = 0.4
TILT_FACTOR = 0.6  # Compresses the Y-axis for a 3D perspective effect
ASTEROID_COUNT = 180

PLANET_DATA = [
    {"name": "Mercury", "color": "#ADB5BD", "size": 4,  "a": 70,  "e": 0.205, "speed": 1.2},
    {"name": "Venus",   "color": "#E3BB76", "size": 7,  "a": 100, "e": 0.006, "speed": 0.9},
    {"name": "Earth",   "color": "#2271B3", "size": 8,  "a": 140, "e": 0.016, "speed": 0.7},
    {"name": "Mars",    "color": "#E27B58", "size": 6,  "a": 180, "e": 0.093, "speed": 0.6},
    {"name": "Jupiter", "color": "#D39C7E", "size": 16, "a": 280, "e": 0.048, "speed": 0.3},
    {"name": "Saturn",  "color": "#C5AB6E", "size": 14, "a": 350, "e": 0.056, "speed": 0.2, "rings": True},
    {"name": "Uranus",  "color": "#BBE1E4", "size": 11, "a": 410, "e": 0.047, "speed": 0.15},
    {"name": "Neptune", "color": "#6081FF", "size": 11, "a": 470, "e": 0.008, "speed": 0.1},
]

# =================================================================
# CLASSES
# =================================================================

class Planet:
    def __init__(self, data: Dict[str, Any]):
        self.name = data["name"]
        self.a = data["a"]          
        self.e = data["e"]          
        self.base_speed = data["speed"]
        self.has_rings = data.get("rings", False)
        self.color = data["color"]
        self.angle = random.randint(0, 360)

        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(self.color)
        self.t.shapesize(data["size"] / 10)
        self.t.penup()

    def get_position(self) -> tuple:
        rad = math.radians(self.angle)
        # Polar equation for an ellipse
        r = (self.a * (1 - self.e**2)) / (1 + self.e * math.cos(rad))
        x = r * math.cos(rad)
        y = r * math.sin(rad) * TILT_FACTOR # Apply Tilt
        return x, y, r

    def update(self, label_pen: turtle.Turtle):
        x, y, r = self.get_position()
        self.t.goto(x, y)
        
        # Physics: Move faster at perihelion (Kepler's Second Law)
        velocity_mult = (self.a / r) ** 1.5 
        self.angle += self.base_speed * TIME_SCALE * velocity_mult

class SolarSystem:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("#050508") # Deep space black
        self.screen.title("Advanced Keplerian Simulation - 3D Perspective")
        self.screen.setup(width=1.0, height=1.0)
        self.screen.tracer(0)

        self.pen = turtle.Turtle(visible=False)
        self.label_pen = turtle.Turtle(visible=False)
        self.ring_pen = turtle.Turtle(visible=False)
        
        self.planets = [Planet(p) for p in PLANET_DATA]
        self._draw_background()

    def _draw_sun_glow(self):
        # Draw layers of the sun for a glow effect
        glow_colors = ["#FF4500", "#FF8C00", "#FFD700", "#FFFF00"]
        sizes = [45, 35, 25, 15]
        for color, size in zip(glow_colors, sizes):
            self.pen.penup()
            # Draw flattened circle for perspective
            self.pen.goto(0, -(size * TILT_FACTOR))
            self.pen.color(color)
            self.pen.begin_fill()
            for deg in range(0, 361, 10):
                rad = math.radians(deg)
                self.pen.goto(size * math.cos(rad), (size * math.sin(rad)) * TILT_FACTOR)
            self.pen.end_fill()

    def _draw_background(self):
        # Stars
        for _ in range(250):
            self.pen.penup()
            self.pen.color(random.choice(["white", "#ADD8E6", "#FFE4B5"]))
            self.pen.goto(random.randint(-800, 800), random.randint(-500, 500))
            self.pen.dot(random.randint(1, 2))

        # Asteroid Belt
        self.pen.color("#444444")
        for _ in range(ASTEROID_COUNT):
            dist = random.uniform(215, 245)
            ang = random.uniform(0, 360)
            rad = math.radians(ang)
            self.pen.penup()
            self.pen.goto(dist * math.cos(rad), (dist * math.sin(rad)) * TILT_FACTOR)
            self.pen.dot(random.randint(1, 2))

        # Orbits (Ellipses)
        self.pen.width(1)
        for p in self.planets:
            self.pen.penup()
            self.pen.color("#222222")
            for a in range(0, 361, 5):
                rad = math.radians(a)
                r = (p.a * (1 - p.e**2)) / (1 + p.e * math.cos(rad))
                self.pen.goto(r * math.cos(rad), (r * math.sin(rad)) * TILT_FACTOR)
                self.pen.pendown()
        
        self._draw_sun_glow()

    def draw_saturn_rings(self, x, y):
        self.ring_pen.clear()
        self.ring_pen.color("#8A7A5F")
        self.ring_pen.width(2)
        for radius in [20, 23, 26]:
            self.ring_pen.penup()
            for deg in range(0, 361, 20):
                rad = math.radians(deg)
                rx = x + radius * math.cos(rad)
                ry = y + (radius * 0.4) * math.sin(rad) # Flat ring perspective
                self.ring_pen.goto(rx, ry)
                self.ring_pen.pendown()

    def animate(self):
        self.label_pen.clear()
        self.label_pen.color("white")
        
        for p in self.planets:
            p.update(self.label_pen)
            px, py, _ = p.get_position()
            
            # Draw dynamic labels
            self.label_pen.penup()
            self.label_pen.goto(px, py + 15)
            self.label_pen.write(p.name, align="center", font=("Verdana", 7, "bold"))
            
            if p.has_rings:
                self.draw_saturn_rings(px, py)

        self.screen.update()
        self.screen.ontimer(self.animate, 20)

if __name__ == "__main__":
    sim = SolarSystem()
    sim.animate()
    turtle.mainloop()