import turtle
import math
import random
from typing import List, Tuple, Dict, Any

# =================================================================
# CONFIGURATION & DATA (Data-Driven Design)
# =================================================================
SIM_CONFIG = {
    "screen_width": 1200,
    "screen_height": 800,
    "bg_color": "#050505",  # Deep space black
    "time_scale": 0.5,
    "star_count": 150
}

# Senior Tip: Move hardcoded data into a structure for easy maintenance
PLANET_DATA = [
    {"name": "Mercury", "color": "#A5A5A5", "size": 5, "radius": 60, "speed": 0.8},
    {"name": "Venus",   "color": "#E3BB76", "size": 8, "radius": 90, "speed": 0.6},
    {"name": "Earth",   "color": "#2271B3", "size": 9, "radius": 120, "speed": 0.4},
    {"name": "Mars",    "color": "#E27B58", "size": 7, "radius": 150, "speed": 0.3},
    {"name": "Jupiter", "color": "#D39C7E", "size": 15, "radius": 200, "speed": 0.2},
    {"name": "Saturn",  "color": "#C5AB6E", "size": 13, "radius": 260, "speed": 0.15, "has_rings": True},
    {"name": "Uranus",  "color": "#BBE1E4", "size": 11, "radius": 310, "speed": 0.1},
    {"name": "Neptune", "color": "#6081FF", "size": 11, "radius": 360, "speed": 0.08},
]

# =================================================================
# CORE CLASSES
# =================================================================

class CelestialBody:
    """Base class demonstrating Type Hinting and Encapsulation."""
    def __init__(self, name: str, color: str, size: float):
        self.name = name
        self.t = turtle.Turtle()
        self.t.hideturtle()  # We show it only when positioned
        self.t.shape("circle")
        self.t.color(color)
        self.t.shapesize(size / 10)
        self.t.penup()
        self.angle = random.uniform(0, 360)

    @property
    def pos(self) -> Tuple[float, float]:
        """Abstract property for coordinates."""
        return self.t.position()

class Planet(CelestialBody):
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data["name"], data["color"], data["size"])
        self.radius = data["radius"]
        self.speed = data["speed"]
        self.has_rings = data.get("has_rings", False)
        self.t.showturtle()

    def update_position(self, dt: float):
        """Standardizes movement logic."""
        self.angle += self.speed * dt
        x = self.radius * math.cos(math.radians(self.angle))
        y = self.radius * math.sin(math.radians(self.angle))
        self.t.goto(x, y)

class Satellite(CelestialBody):
    """Demonstrates Composition: A body that follows a parent."""
    def __init__(self, name: str, parent: Planet, orbit_dist: int, speed: float):
        super().__init__(name, "white", 3)
        self.parent = parent
        self.orbit_dist = orbit_dist
        self.speed = speed
        self.t.showturtle()

    def update_position(self, dt: float):
        self.angle += self.speed * dt
        px, py = self.parent.pos
        x = px + self.orbit_dist * math.cos(math.radians(self.angle))
        y = py + self.orbit_dist * math.sin(math.radians(self.angle))
        self.t.goto(x, y)

# =================================================================
# ENGINE CLASS
# =================================================================

class SolarSystemEngine:
    """The 'Controller' that manages the simulation lifecycle."""
    def __init__(self):
        self.screen = self._setup_screen()
        self.pen = turtle.Turtle(visible=False)
        self.pen.speed(0)
        
        # Initialize Bodies
        self.planets = [Planet(p) for p in PLANET_DATA]
        self.earth = next(p for p in self.planets if p.name == "Earth")
        self.moon = Satellite("Moon", self.earth, 20, 2.5)
        
        self._draw_static_elements()

    def _setup_screen(self) -> turtle.Screen:
        s = turtle.Screen()
        s.bgcolor(SIM_CONFIG["bg_color"])
        s.setup(SIM_CONFIG["screen_width"], SIM_CONFIG["screen_height"])
        s.tracer(0)
        return s

    def _draw_static_elements(self):
        """Draws stars and orbits once to save performance."""
        # Stars
        self.pen.color("white")
        for _ in range(SIM_CONFIG["star_count"]):
            self.pen.penup()
            self.pen.goto(random.randint(-600, 600), random.randint(-400, 400))
            self.pen.dot(random.randint(1, 2))
        
        # Orbits
        self.pen.color("#333333")
        for p in self.planets:
            self.pen.penup()
            self.pen.goto(0, -p.radius)
            self.pen.pendown()
            self.pen.circle(p.radius)
            
        # Sun
        sun = turtle.Turtle(shape="circle")
        sun.color("#FFCC00")
        sun.shapesize(3)
        sun.penup()

    def run(self):
        """The main animation loop."""
        def frame():
            # Clear dynamic labels/rings with one go
            self.pen.clear()
            
            # Update all celestial bodies
            dt = SIM_CONFIG["time_scale"]
            for p in self.planets:
                p.update_position(dt)
                
                # Draw Labels using the shared pen (More efficient than individual turtles)
                self.pen.penup()
                self.pen.goto(p.t.xcor(), p.t.ycor() + 15)
                self.pen.color("white")
                self.pen.write(p.name, align="center", font=("Verdana", 8, "normal"))

                # Draw Rings if applicable
                if p.has_rings:
                    self.pen.goto(p.t.xcor(), p.t.ycor() - 10)
                    self.pen.pendown()
                    self.pen.circle(20)

            self.moon.update_position(dt)
            
            self.screen.update()
            self.screen.ontimer(frame, 20)
        
        frame()
        self.screen.mainloop()

if __name__ == "__main__":
    sim = SolarSystemEngine()
    sim.run()