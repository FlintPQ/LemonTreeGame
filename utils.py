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
    def __init__(self, filename='None', cols=-1, rows=-1, infinite=True, reverse=False):
        self.sprite_sheet = SpriteSheet(filename, cols, rows)

        if reverse:
            self.sprite_sheet.cells.reverse()

        self.infinite = infinite

        self.animation_speed = 500  # pic time in milisec
        self.cur_sprite_index = 0
        self._time_from_last_sprite_update_buffer = 0

    def get_next_sprite(self, timedelta, reversed=False):
        self._time_from_last_sprite_update_buffer += timedelta
        how_many_sprites_passed = math.floor(
            self._time_from_last_sprite_update_buffer / self.animation_speed)

        if how_many_sprites_passed >= 1:
            self._time_from_last_sprite_update_buffer = 0
            if reversed:
                if not self.infinite and self.cur_sprite_index - how_many_sprites_passed < 0:
                    return True
                self.cur_sprite_index = (
                                            self.cur_sprite_index - how_many_sprites_passed)\
                                        % self.sprite_sheet.totalCellCount
            else:
                if not self.infinite and self.cur_sprite_index + how_many_sprites_passed > self.sprite_sheet.totalCellCount - 1:
                    return True
                self.cur_sprite_index = (
                                            self.cur_sprite_index + how_many_sprites_passed)\
                                        % self.sprite_sheet.totalCellCount

        return self.sprite_sheet.get_sprite(self.cur_sprite_index)


def cords_dot_on_circle(angle, center_cords, R):
    return (center_cords[0] + R * math.sin(math.radians(angle)),
            center_cords[1] + R * math.cos(math.radians(angle)))


def get_dot_angle_on_circle(cords, center_cords):
    a = math.atan2(cords[0] - center_cords[0], cords[1] - center_cords[1]) / math.pi * 180
    if a < 0:
        a = a + 360
    return a


def summarize_angles(angle1, angle2):
    angle1 = angle1 + angle2
    if angle1 >= 360:
        angle1 -= 360


class HitBoxDot:
    def __init__(self, cords, R, basic_angle):
        self.x = cords[0]
        self.y = cords[1]
        self.distance_from_center = R
        self.basic_angle = basic_angle

    def update(self, center_cords, angle):
        self.x, self.y = cords_dot_on_circle(summarize_angles(self.basic_angle, angle), center_cords, self.distance_from_center)


class HitBox:
    def __init__(self, cords: list, width, height, angle: list):
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
                HitBoxDot(a, self.R, get_dot_angle_on_circle(a, self.cords)),
                HitBoxDot(b, self.R, get_dot_angle_on_circle(b, self.cords)),
                HitBoxDot(c, self.R, get_dot_angle_on_circle(c, self.cords)),
                HitBoxDot(d, self.R, get_dot_angle_on_circle(d, self.cords))
            ]

    def update(self):
        for _ in self.dots_list:
            _.update(self.cords, self.angle[0])


class PhysicsChecker:
    def __init__(self, cur_games_obj_set):
        self.all_objects = cur_games_obj_set

    def check_collisions(self):
        for i in self.all_objects:
            _l = list()
            for j in self.all_objects.copy().remove(i):
                if self.check_box_collision(i, j):
                    _l.append(j)
            i.collision_reaction(_l)

    def check_box_collision(self, box1, box2):

        for i in range(len(box1.dots_list)):
            dot1 = box1.dots_list[i]
            dot2 = box1.dots_list[(i + 1) % 4]
            for j in box2.dots_list:
                dot3 = box2.dots_list[j]
                dot4 = box2.dots_list[(j + 1) % 4]

                if self.check_lines_collision(dot1, dot2, dot3, dot4) >= 1:
                    return True
                else:
                    return False

    def check_lines_collision(self, cords1, cords2, cords3, cords4):
        x1, y1 = cords1
        x2, y2 = cords2
        x3, y3 = cords3
        x4, y4 = cords4
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
                return 0  # Lines hasn't got collision and they are not parallel


class IPhysics:
    def __init__(self):
        self.physics_flags = {'uses_physics'}
        self.hitbox = HitBox(self.cords)


pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.image.save(SpriteSheet('sheet.png', 4, 3).get_sprite(2), 'opa.png')
