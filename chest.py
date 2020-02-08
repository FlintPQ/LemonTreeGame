import math
import string
from config import CONFIG
import pygame
from config import CONFIG, keys_dict
from utils import Animation



class Chilipizdrik:  # КЛАСС ЧИЛИПИЗДРИК
    def __init__(self):
        pass


class Inventory:
    def __init__(self):
        self.capacity = []
        self.len = 25
        self.x = 40
        self.y = 40
        self.w = 600
        self.h = 640


class Chest:
    def __init__(self, x, y, game, *args):
        self.x = x
        self.y = y
        self.capacity = 25
        self.content = list(args)
        self.h = 50
        self.w = 50
        self.cell_side = 120
        self.open_window_x = 650
        self.open_window_y = 60
        self.open_window_h = 600
        self.open_window_w = 600
        self.cross_x = self.cross_y = self.cross_side = 30
        self.animation_dict = {
            'closed_or_opening': Animation('chest.jpeg', 1, 4)
        }
        self.animation = Animation('opa.png', 1, 1)
        self.static_image = Animation('opa.png', 1, 1)
        self.open_chest_image = Animation('open_chest_image.PNG', 1, 1)
        self.events = []
        self.game = game
        self.player = game.player

    def check_cell(self, x, y):
        if self.open_window_x < x < self.open_window_x + self.open_window_w \
                and self.open_window_y < y < self.open_window_h:
            cell_x = (x - self.open_window_x) // self.cell_side
            cell_y = (y - self.open_window_y) // self.cell_side
            return cell_x, cell_y
        return False

    def append(self, thing, x, y):
        if not self.content[x * y]:
            self.content[x * y - 1] = thing
            return True
        return False

    def delete(self, x: int, y: int):
        thing = self.content[x * y - 1]
        self.content[x][y] = None
        return thing

    def draw(self, time_delta):
        if self.player.game_state == 'opening':
            cur_image = self.animation.get_next_sprite(time_delta)
        elif self.player.game_state == 'closing':
            cur_image = self.animation.get_next_sprite(time_delta, reversed=True)
        elif self.player.game_state == 'game':
            cur_image = self.static_image
        elif self.player.game_state == 'chest':
            cur_image = self.open_chest_image
        image_cords = (self.x - self.w // 2,
                       self.y - self.h // 2)
        self.game.win.blit(cur_image, image_cords)

    def check_events(self, time_delta):
        for i in self.events:
            if i[0] == 'Mouse_down':
                self.player.game_state = 'chest'

        self.events = []

    def update(self, time_delta):
        self.check_events(time_delta)
        self.draw(time_delta)


class MouseController:
    def __init__(self, game):
        self.player = game.player
        self.inventory = self.player.inventory
        self.chest = game.chest
        self.mouse_down = False
        self.motion_and_down = False
        self.was_upped = False

    def check_events(self, e, mouse_pos):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
        elif e.type == pygame.MOUSEBUTTONUP:
            if is_cancel(mouse_pos, self.player.board):
                self.player.check_events('close')
            self.mouse_down = False
            self.motion_and_down = False
            self.was_upped = True
        elif e.type == pygame.MOUSEMOTION and self.mouse_down:
            self.motion_and_down = True

    def update(self, e, mouse_pos):
        print(e.type)
        self.check_events(e, mouse_pos)
        if self.mouse_down and self.player.game_state == 'game':
            found_object(mouse_pos).events.append(('Mouse_down', mouse_pos))
        elif self.mouse_down and not self.motion_and_down and\
                self.player.game_state == 'inventory':
            cell = self.player.inventory.get_cell(mouse_pos)
            if cell:
                self.player.change_weapon(self.player.inventory.get_weapon(cell))
        elif self.mouse_down and self.player.game_state == 'chest':
            if not self.player.buffer and not self.motion_and_down:
                exist_cell = check_cell(mouse_pos, self.player)
                if exist_cell:
                    self.player.buffer = exist_cell[0].get_cell(exist_cell[1])
            if self.player.buffer:
                self.player.buffer.x, self.player.buffer.y = mouse_pos[0], mouse_pos[1]
        elif self.was_upped and self.player.game_state == 'chest' and self.player.buffer:
            exist_cell = check_cell(mouse_pos, self.player)
            if exist_cell and exist_cell[0][exist_cell[1]].append(self.player.buffer):
                self.player.buffer = None
            self.was_upped = False


def is_cancel(pos, board):
    if board.cross_x <= pos[0] <= board.cross_x + board.side and \
            board.cross_y <= pos[1] <= board.cross_y + board.side:
        return True
    return False


def check_cell(pos, player):
    inv_x = player.inventory.cells_x
    inv_y = player.inventory.cells_y

    if inv_x <= pos[0] <= player.inventory.cells_x\
            + player.inventory.cells_w and inv_y <= pos[1]\
            <= inv_y + player.inventory.cells_h:
        return [1, 1]


def found_object(cords):
    for i in list_obj:
        if i.x <= cords[0] <= i.x + i.w and i.y <= cords[1] <= i.y + i.h:
            return i
    return False


list_obj = []
