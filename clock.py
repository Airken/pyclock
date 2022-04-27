import pygame, math, sys, os
from pygame.locals import *
import pygame.gfxdraw
from datetime import datetime
from PIL import Image, ImageDraw
import time

white = (255,255,255)
red = (255, 0, 0)
black = (0,0,0)
green = (0,255,0)
gold = (0xFF, 0xD7, 00)
size = 240


def roint(num):
    return int(round(num))

class DrawClock:
    def __init__(self, surf):
        self.surf = surf
        self.size = 1000
        self.radius = roint(self.size / 2)
        self.center_x = roint((self.size + 2) / 2)
        self.center_y = roint((self.size + 2) / 2)
        self.center_point = (self.center_x, self.center_y)
        self.image = Image.new("RGBA", (self.size + 2, self.size + 2))
        self.draw = ImageDraw.Draw(self.image)

    def draw_plate(self, background, size):
        top = roint(self.center_x - size * self.radius)
        left = roint(self.center_y - size * self.radius)
        bottom = roint(self.center_x + size * self.radius)
        right = roint(self.center_y + size * self.radius)
        self.draw.ellipse([(top, left), (bottom, right)], fill=background)

    def draw_bar(self, bars, length, width, color):
        for bar in range(bars):
            angle = 360.0 / bars * bar
            cos = math.cos(math.radians(angle))
            sin = math.sin(math.radians(angle))
            start_x = roint(self.center_x + self.radius * cos * (1 - length))
            start_y = roint(self.center_y + self.radius * sin * (1 - length))
            end_x = roint(self.center_x + self.radius * cos * 95.0 / 100.0)
            end_y = roint(self.center_y + self.radius * sin * 95.0 / 100.0)
            self.draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)

    def draw_hours(self):
        self.draw_bar(12, 3 / 20, 20, white)

    def draw_minutes(self):
        self.draw_bar(60, 2 / 20, 10, white)

    def draw_hand(self, angle, length, width, color):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        start_x = roint(self.center_x - self.radius * cos * length * 1 / 5)
        start_y = roint(self.center_y - self.radius * sin * length * 1 / 5)
        end_x = roint(self.center_x + self.radius * length * cos)
        end_y = roint(self.center_y + self.radius * length * sin)
        self.draw.line([(start_x, start_y), (end_x, end_y)], fill=color, width=width)

    def update(self):
        second = float(datetime.now().second)
        minute = float(datetime.now().minute)
        hour = float(datetime.now().hour)
        # Minute Hand
        angle = 6 * minute + second / 10 - 90
        self.draw_hand(angle, 8 / 15, 20, gold)
        # Hour Hand
        angle = 30 * (hour % 12) + 5 * minute / 10 - 90
        self.draw_hand(angle, 6 / 15, 30, gold)
        # Second Hand
        angle = 6 * second - 90
        self.draw_hand(angle, 10 / 15, 10, gold)

    def blit(self):
        _width, _height = self.surf.get_size()
        self.image = self.image.resize((roint(_width), roint(_height)), Image.BILINEAR)
        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.surf.blit(self.image, (0, 0))

if os.environ.get('ENV') == 'Pi':
    os.putenv('SDL_FBDEV', "/dev/fb1")
    os.environ["SDL_VIDEODRIVER"] = "fbcon"

pygame.display.init()
pygame.mixer.quit()
pygame.mouse.set_visible(False)
main_surf = pygame.display.set_mode((roint(size),roint(size)))
c = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    main_surf.fill(white)

    wallclock = DrawClock(main_surf)
    wallclock.draw_plate(black, 1)
    wallclock.draw_plate(red, 3 / 10)
    wallclock.draw_hours()
    wallclock.draw_minutes()
    wallclock.update()
    wallclock.blit()

    pygame.display.flip()
    c.tick(2)
