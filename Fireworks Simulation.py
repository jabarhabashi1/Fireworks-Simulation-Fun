import turtle
import random
import math
import colorsys

#graphical settings
screen = turtle.Screen()
screen.bgcolor('black')
screen.title('Advanced Fireworks')
screen.setup(width=800, height=600)
screen.tracer(5)  # Increase rendering speed by reducing intermediate frames
screen.colormode(255)

# Special effects settings
PARTICLE_SIZE = 0.8
GLOW_RADIUS = 15
EXPLOSION_SPEED = 2.5
FADE_RATE = 8
RAINBOW_SPEED = 0.02

fireworks = []


class Firework:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.shapesize(0.5)
        self.t.color(self.random_bright_color())
        self.t.penup()
        self.t.goto(random.randint(-350, 350), -280)
        self.velocity = random.uniform(15, 20)
        self.gravity = 0.25
        self.particles = []
        self.exploded = False

    def random_bright_color(self):
        h = random.random()
        s = 1
        v = 1
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return tuple(int(c * 255) for c in rgb)

    def update(self):
        if not self.exploded:
            self.t.sety(self.t.ycor() + self.velocity)
            self.velocity -= self.gravity
            if self.velocity < 0 or self.t.ycor() > 250:
                self.explode()

        for p in self.particles[:]:
            # Move particles
            p[0].goto(p[0].xcor() + p[3][0], p[0].ycor() + p[3][1])

            # Apply gravity
            p[3] = (p[3][0] * 0.98, p[3][1] - self.gravity)

            # Change color to create a rainbow effect
            p[2][0] = (p[2][0] + RAINBOW_SPEED) % 1.0
            rgb = colorsys.hsv_to_rgb(p[2][0], 1, p[2][1])
            p[0].color(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )

            # Reduce brightness and size
            p[2][1] = max(0, p[2][1] - FADE_RATE / 255)
            p[0].shapesize(PARTICLE_SIZE * p[2][1])

            if p[2][1] <= 0.1:
                p[0].hideturtle()
                self.particles.remove(p)

    def explode(self):
        self.exploded = True
        self.t.hideturtle()

        # Create 120 particles for higher density
        for _ in range(20):
            p = turtle.Turtle()
            p.shape("circle")
            p.shapesize(PARTICLE_SIZE)
            p.penup()
            p.goto(self.t.pos())

            # Set random speed
            angle = math.radians(random.uniform(0, 360))
            speed = random.uniform(EXPLOSION_SPEED / 2, EXPLOSION_SPEED)

            # Calculate movement vector
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed

            # Initialize HSV color values
            hue = random.random()
            brightness = 1.0  # Start with maximum brightness

            self.particles.append([
                p,
                speed,
                [hue, brightness],  # [Hue, Value]
                (dx, dy)
            ])


def create_firework(x, y):
    fireworks.append(Firework())


def update():
    screen.update()
    for fw in fireworks[:]:
        fw.update()
        if fw.exploded and not fw.particles:
            fireworks.remove(fw)
    screen.ontimer(update, 30)  # Increase update rate


screen.onscreenclick(create_firework)
update()
screen.mainloop()