from math import sqrt

import pygame
from pygame.rect import Rect


def get_normalized_vector(vec):
    vec_length = sqrt(vec[0] ** 2 + vec[1] ** 2)
    x = vec[0] / vec_length
    y = vec[1] / vec_length
    return Vec(x, y)

def skalar(dot1, dot2):
    return dot1.x * dot2.x + dot1.y * dot2.y

class Physics:
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

    def get_crossing_dot(self, p1, p2, p3, p4):
        # сначала расставим точки по порядку
        if p2.x < p1.x:
            p1, p2 = p2, p1

        # и p3.x <= p4.x
        if p4.x < p3.x:
            p3, p4 = p4, p3

        if p1.x > p3.x:
            p1, p3 = p3, p1
            p2, p4 = p4, p2

        # проверим существование потенциального интервала для точки пересечения отрезков
        if p2.x < p3.x:
            return False  # ибо у отрезков нету взаимной абсциссы

        # если оба отрезка вертикальные
        if (p1.x - p2.x == 0) and (p3.x - p4.x == 0):

            # если они лежат на одном X
            if p1.x == p3.x:
                # проверим пересекаются ли они, т.е. есть ли у них общий Y
                # для этого возьмём отрицание от случая, когда они НЕ пересекаются
                if not ((max(p1.y, p2.y) < min(p3.y, p4.y)) or (min(p1.y, p2.y) > max(p3.y, p4.y))):
                    return True

            return False

            # найдём коэффициенты уравнений, содержащих отрезки
            # f1(x) = A1*x + b1 = y
            # f2(x) = A2*x + b2 = y

        # если первый отрезок вертикальный
        if (p1.x - p2.x) == 0:
            # найдём Xa, Ya - точки пересечения двух прямых
            Xa = p1.x
            A2 = (p3.y - p4.y) / (p3.x - p4.x)
            b2 = p3.y - A2 * p3.x
            Ya = A2 * Xa + b2

            if p3.x <= Xa <= p4.x and min(p1.y, p2.y) <= Ya and max(p1.y, p2.y) >= Ya:
                return Vec(Xa, Ya)

            return False

        # если второй отрезок вертикальный
        if p3.x - p4.x == 0:
            # найдём Xa, Ya - точки пересечения двух прямых
            Xa = p3.x
            A1 = (p1.y - p2.y) / (p1.x - p2.x)
            b1 = p1.y - A1 * p1.x
            Ya = A1 * Xa + b1

            if p1.x <= Xa and p2.x >= Xa and min(p3.y, p4.y) <= Ya and max(p3.y, p4.y) >= Ya:
                return Vec(Xa, Ya)

            return False
            # оба отрезка невертикальные
        A1 = (p1.y - p2.y) / (p1.x - p2.x)
        A2 = (p3.y - p4.y) / (p3.x - p4.x)
        b1 = p1.y - A1 * p1.x
        b2 = p3.y - A2 * p3.x

        if A1 == A2:
            return False  # отрезки параллельны

        # Xa - абсцисса точки пересечения двух прямых
        Xa = (b2 - b1) / (A1 - A2)

        if (Xa < max(p1.x, p3.x)) or (Xa > min(p2.x, p4.x)):
            return False  # точка Xa находится вне пересечения проекций отрезков на ось X

        else:
            return Vec(Xa, A2 * Xa + b2)

    def spot_pillar_dot(self, *args, vec=None):
        # args must be Vec object
        max_dur = -9999999999999999999
        _ = 0
        ind = -999
        for i in range(len(args)):
            _ = skalar(args[i % 4], vec)

            if _ > max_dur:
                max_dur = _
                ind = i

        return args[ind]

    def normal_vec_edge(self, dot1, dot2):
        return Vec(dot2.y - dot1.y, dot1.x - dot2.x)

    def FindAxisLeastPenetration(self, dots, wall, vec):
        best_distance = -999999999999
        best_index = -999999999999
        normalized_vec = get_normalized_vector(vec)

        for i in range(len(wall.dots_list)):
            # n = normal_vec_edge(A.dots_list[i % 4],
            #                    A.dots_list[(i + 1) % 4])
            # n_length = sqrt(n.x ** 2 + n.y ** 2)
            # n.x = n.x / n_length
            # n.y = n.y / n_length
            s = self.spot_pillar_dot(*dots, vec=normalized_vec)
            v = wall.dots_list[i]
            d = skalar(normalized_vec, Vec(s.x - v.x, s.y - v.y))
            if d > best_distance:
                best_distance = d
                best_index = i

        return best_distance

    def inPolygon(self, polygon, dot):
        xp = list()
        yp = list()
        for i in polygon.dots_list:
            xp.append(i.x)
            yp.append(i.y)
        x, y = dot.x, dot.y
        c = 0
        if dot.x in xp and dot.y in yp:
            return True

        for i in range(len(xp)):
            if (((yp[i] <= y and y <= yp[i - 1]) or (yp[i - 1] <= y and y <= yp[i])) and
                    (x >= (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
                c = 1 - c

        if c == 1:
            return True
        else:
            return False

    def get_back_impulse(self, moving, wall):
        moving_dots = list()

        for i in range(len(moving.dots_list)):
            if self.inPolygon(wall, moving.dots_list[i]):
                moving_dots.append(moving.dots_list[i])
            for j in range(len(wall.dots_list)):
                dot = self.get_crossing_dot(moving.dots_list[i % len(moving.dots_list)],
                                       moving.dots_list[(i + 1) % len(moving.dots_list)],
                                       wall.dots_list[j % len(moving.dots_list)],
                                       moving.dots_list[(j + 1) % len(moving.dots_list)])
                if dot:
                    moving_dots.append(dot)

        impulse_power = self.FindAxisLeastPenetration(moving_dots, wall, moving.move_buffer)
        return impulse_power



class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('Only x and y are possible')


class Box:
    def __init__(self, d1, d2, d3, d4):
        self.dots_list = [d1, d2, d3, d4]
        self.move_buffer = [100, 0]

x = 40
y = 30
b = Box(Vec(100 - y, 100 - x), Vec(130 - y, 150 - x), Vec(80 - y, 200 - x), Vec(40 - y, 150 - x))
a = Box(Vec(100, 10), Vec(200, 10), Vec(200, 101), Vec(100, 100))

g = Physics(list())
print(g.get_back_impulse(b, a))
print(g.get_crossing_dot(a.dots_list[2], a.dots_list[3], b.dots_list[0], b.dots_list[1]))
print(g.inPolygon(a, Vec(100, 10)))
vec = [0, -40]
norm_vec = [0, -1]

dot = g.spot_pillar_dot(*b.dots_list, vec=Vec(0, -1))

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.draw.polygon(win, (255,0,0), [[a.dots_list[0].x , a.dots_list[0].y] , [a.dots_list[1].x, a.dots_list[1].y], [a.dots_list[2].x, a.dots_list[2].y], [a.dots_list[3].x, a.dots_list[3].y]])
pygame.draw.polygon(win, (255,255,255), [[b.dots_list[0].x, b.dots_list[0].y], [b.dots_list[1].x, b.dots_list[1].y], [b.dots_list[2].x, b.dots_list[2].y], [b.dots_list[3].x, b.dots_list[3].y]])

pygame.display.update()
while True:
    for e in pygame.event.get():
        pass
