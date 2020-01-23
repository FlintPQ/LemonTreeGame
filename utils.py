import math

import pygame


class SpriteSheet:
    def __init__(self, filename, cols, rows):
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        rect = self.sprite_sheet.get_rect()

        w, h = self.size = (int(rect.width / cols), int(rect.height / rows))
        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])

    def get_sprite(self, cell_index):
        return self.sprite_sheet.subsurface(pygame.Rect(self.cells[cell_index]))


class Animation:
    def __init__(self, filename='None', cols=-1, rows=-1):
        self.sprite_sheet = SpriteSheet(filename, cols, rows)
        self.animation_speed = 250  # pic time in milisec
        self.cur_sprite_index = 0
        self._time_from_last_sprite_update_buffer = 0

    def get_next_sprite(self, timedelta, reversed=False):
        self._time_from_last_sprite_update_buffer += timedelta
        how_many_sprites_passed = math.floor(self._time_from_last_sprite_update_buffer / self.animation_speed)

        if how_many_sprites_passed >= 1:
            self._time_from_last_sprite_update_buffer = 0
            if reversed:
                self.cur_sprite_index = (
                                                    self.cur_sprite_index - how_many_sprites_passed) % self.sprite_sheet.totalCellCount


            else:
                self.cur_sprite_index = (
                                                    self.cur_sprite_index + how_many_sprites_passed) % self.sprite_sheet.totalCellCount

        return self.sprite_sheet.get_sprite(self.cur_sprite_index)


def cords_dot_on_circle(angle, center_cords, R):
    return (center_cords[0] + R * math.sin(math.radians(angle)),
            center_cords[1] + R * math.cos(math.radians(angle)))


def get_dot_angle_on_circle(cords, center_cords):
    a = math.atan2(cords[0] - center_cords[0], cords[1] - center_cords[1]) / math.pi * 180
    if a < 0:
        a = a + 360
    return a


class HitBoxDot:
    def __init__(self, cords, basic_angle):
        self.x = cords[0]
        self.y = cords[1]
        self.basic_angle = basic_angle


class HitBox:
    def __init__(self, cords, width, height, angle):
        self.cords = cords
        self.angle = angle
        self.width = width
        self.height = height
        self.R = math.hypot(self.width // 2, self.height // 2)
        a = (self.cords[0] - self.width // 2, self.cords[1] - self.height // 2)
        b = (self.cords[0] + self.width // 2, self.cords[1] - self.height // 2)
        c = (self.cords[0] - self.width // 2, self.cords[1] + self.height // 2)
        d = (self.cords[0] + self.width // 2, self.cords[1] + self.height // 2)

        self.dots_list = [
                HitBoxDot(a, get_dot_angle_on_circle(a, self.cords)),
                HitBoxDot(b, get_dot_angle_on_circle(b, self.cords)),
                HitBoxDot(c, get_dot_angle_on_circle(c, self.cords)),
                HitBoxDot(d, get_dot_angle_on_circle(d, self.cords))
            ]

    def update(self):
        R =
        x = x0 + 50 * math.sin(radians(90))
        y = y0 + 50 * math.cos(radians(90))
        self.dots_cords = [
            [self.cords[0] + R * math.sin(math.radians(90)), self.cords[1] - self.height // 2],
            [self.cords[0] + self.width // 2, self.cords[1] - self.height // 2],
            [self.cords[0] - self.width // 2, self.cords[1] + self.height // 2],
            [self.cords[0] + self.width // 2, self.cords[1] + self.height // 2]
        ]


class Physics:
    def __init__(self, cur_games_obj_list):
        self.all_objects = cur_games_obj_list

    def check_box_collision(self, box1, box2):
        lines1 = [
            (box1[0], box1[1]),
            (box1[1], box1[2]),
            (box1[2], box1[3]),
            (box1[3], box1[0]),
        ]

        lines2 = [
            (box2[0], box2[1]),
            (box2[1], box2[2]),
            (box2[2], box2[3]),
            (box2[3], box2[0]),
        ]

        checks = list()
        for i in range(len(lines1)):
            if

    def check_lines_collision(self, cords1, cords2):
        x1, y1, x2, y2 = cords1
        x3, y3, x4, y4 = cords2
        denominator = (y4 - y3) * (x1 - x2) - (x4 - x3) * (y1 - y2)
        if denominator == 0:
            if (x1 * y2 - x2 * y1) * (x4 - x3) - (x3 * y4 - x4 * y3) * (x2 - x1) == 0 & (x1 * y2 - x2 * y1) * (
                    y4 - y3) - (x3 * y4 - x4 * y3) * (y2 - y1) == 0:
                return 2  # Lines have collision and they are parallel
            else:
                return -1  # Lines hasn't got collision and they are parallel

        else:
            numerator_a = (x4 - x2) * (y4 - y3) - (x4 - x3) * (y4 - y2)
            numerator_b = (x1 - x2) * (y4 - y2) - (x4 - x2) * (y1 - y2)
            Ua = numerator_a / denominator
            Ub = numerator_b / denominator
            if Ua >= 0 & Ua <= 1 & Ub >= 0 & Ub <= 1:
                return 1  # Lines have collision and they are not parallel
            else:
                return 0  # Lines hasn't got collision


class PhysicsTrait:
    def __init__(self):
        self.physics_flags = {'uses_physics'}


pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.image.save(SpriteSheet('sheet.png', 4, 3).get_sprite(2), 'opa.png')
