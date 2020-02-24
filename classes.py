import random
import pygame
from consts import *


def init_buttons1():
    button1 = Button(*BUTTON1, random.randint(0, 255), 'play')
    button2 = Button(*BUTTON2, random.randint(0, 255), 'exit')

    return [button1, button2]


def init_circles():
    circles = []
    for i in range(15):
        circles.append(Circle(random.randint(0, WINDOW_SIZE), random.randint(0, WINDOW_SIZE), random.randint(20, 50), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
    return circles


class Button:
    def __init__(self, coords, sizex, sizey, color, text):
        self.coords = coords
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.text = text
        self.delta = 0
        self.shrift = pygame.font.SysFont('arial', 30).render(self.text, 0, WHITE)
        self.button = pygame.Rect(self.coords[0] - self.delta, self.coords[1] - self.delta, self.sizex + 2*self.delta, self.sizey + 2*self.delta)

    def update(self):
        self.button = pygame.Rect(self.coords[0] - self.delta, self.coords[1] - self.delta, self.sizex + 2*self.delta, self.sizey + 2*self.delta)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.button)
        surface.blit(self.shrift, (self.coords[0] + 2*self.sizex//5, self.coords[1]))


class Menu:
    def __init__(self, buttons, circles):
        self.buttons = buttons
        self.circles = circles

    def check_mouse_pos(self):
        for i in self.buttons:
            if i.button.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return i

    def draw_animation(self, circles, surface):
        for i in circles:
            i.draw(surface)

    def draw(self, surface):
        for i in self.buttons:
            i.draw(surface)


class Circle:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def move(self):
        if self.y - self.r <= WINDOW_SIZE:
            self.y += 10
        else:
            self.randomize()

    def randomize(self):
        self.x = random.randint(0, WINDOW_SIZE)
        self.y = random.randint(0, WINDOW_SIZE)
        self.r = random.randint(20, 50)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)