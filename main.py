import math
import string
from config import CONFIG
import pygame
from config import CONFIG, keys_dict
from utils import Animation
import os


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Weapon:
    def __init__(self):
        self.image = pygame.transform.scale(load_image('weapon.png'),
                                            (115, 115))
        self.x, self.y = None, None
        self.is_in_buffer = False
        self.delta_x, self.delta_y = 0, 0

    def append_in_buffer(self, delta_x, delta_y, mouse_pos):
        self.is_in_buffer = True
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.x = mouse_pos[0] - delta_x
        self.y = mouse_pos[1] - delta_y

    def update_pos(self, mouse_pos):
        self.x = mouse_pos[0] - self.delta_x
        self.y = mouse_pos[1] - self.delta_y

    def delete_from_buffer(self):
        self.x, self.y = None, None
        self.is_in_buffer = False
        self.delta_x, self.delta_y = 0, 0

    def draw(self, cords):
        win.blit(self.image, cords)


class Inventory:
    def __init__(self):
        self.content = []
        self.capacity = 16
        self.x = 680
        self.y = 900
        self.w, self.h = 70, 50
        self.window_x = 40
        self.window_y = 40
        self.window_w = 500
        self.window_h = 500
        self.cells_x, self.cells_y = 90, 80
        self.cells_w, self.cells_h = 460, 460
        self.cell_side = 115
        self.cross_x = 540
        self.cross_y = 40
        self.cross_side = 35
        self.closed_omage = load_image('closed_inventory.png', -1)
        self.open_image = load_image('chest_or_inventory.png', -1)
        self.events = []
        self.state = 'close'

    def get_cell(self, pos):
        if self.cells_x <= pos[0] <= self.cells_x + self.cells_w \
                and self.cells_y <= pos[1] <= self.cells_h + self.cells_y:
            cell = (((pos[0] - self.cells_x) // self.cell_side) + 1) *\
                   (((pos[1] - self.cells_y) // self.cell_side) + 1) - 2
            if cell < len(self.content):
                thing = self.content[cell]
            else:
                thing = None
            return cell, thing
        return None

    def check_events(self):
        for i in self.events:
            if i == 'open':
                self.state = 'open'
            elif i == 'close':
                self.state = 'close'

        self.events = []

    def append(self, thing):
        if len(self.content) < self.capacity:
            self.content.append(thing)
            return True
        return False

    def delete(self, cell):
        del self.content[cell]

    def draw(self):
        if self.state == 'closed':
            win.blit(self.closed_omage, (self.window_x, self.window_y))
        elif self.state == 'open':
            win.blit(self.open_image, (self.window_x, self.window_y))
            for i in range(len(self.content)):
                if not self.content[i].x and not self.content[i].y:
                    x = self.cells_x + (i % 5) * self.cell_side
                    y = self.cells_y + i // 5 * self.cell_side
                else:
                    x, y = self.content[i].x, self.content[i].y
                win.blit(self.content[i].image, (x, y))

    def append_event(self, e):
        self.events.append(e)

    def update(self, time_delta):
        self.check_events()
        self.draw()


class Chest:
    def __init__(self, x, y, *args):
        self.x = x
        self.y = y
        self.h = 31
        self.w = 30
        self.capacity = 16
        self.content = list(args)
        self.window_x = 540
        self.window_y = 40
        self.open_window_h = 620
        self.open_window_w = 620
        self.cell_side = 115
        self.cells_x = 590
        self.cells_y = 80
        self.cells_w, self.cells_h = 460, 460
        self.cross_x, self.cross_y = 1040, 40
        self.cross_side = 35
        self.animation_dict = {
            'closed_or_opening': Animation('chest.jpeg', 1, 4)
        }
        self.animation = Animation('opa.png', 1, 1)
        self.static_image = load_image('one_chest.png')
        self.open_chest_image = load_image('chest_or_inventory.png', -1)
        self.events = []
        self.state = 'close'

    def get_cell(self, pos):
        if self.cells_x <= pos[0] <= self.cells_x + self.cells_w \
                and self.cells_y <= pos[1] <= self.cells_h:
            cell = (((pos[0] - self.cells_x) // self.cell_side) + 1) * \
                     (((pos[1] - self.cells_y) // self.cell_side) + 1) - 2
            if cell < len(self.content):
                thing = self.content[cell]
            else:
                thing = None
            return cell, thing
        return None

    def append(self, thing):
        if len(self.content) < self.capacity:
            self.content.append(thing)
            return True
        return False

    def delete(self, cell):
        del self.content[cell]
        return True

    def draw(self, time_delta):
        image_cords = (self.x,
                       self.y)
        if self.state == 'opening':
            cur_image = self.animation.get_next_sprite(time_delta)
        elif self.state == 'closing':
            cur_image = self.animation.get_next_sprite(time_delta, reversed=True)
        elif self.state == 'close':
            cur_image = self.static_image
        elif self.state == 'open':
            image_cords = (self.window_x, self.window_y)
            cur_image = self.open_chest_image
        win.blit(cur_image, image_cords)
        if self.state == 'open':
            for i in range(len(self.content)):
                if not self.content[i].x and not self.content[i].y:
                    x = self.cells_x + (i % 4) * self.cell_side
                    y = self.cells_y + i // 4 * self.cell_side
                else:
                    x, y = self.content[i].x, self.content[i].y
                win.blit(self.content[i].image, (x, y))

    def check_events(self, time_delta):
        for i in self.events:
            if i == 'open':
                self.state = 'open'
            elif i == 'close':
                self.state = 'close'

        self.events = []

    def append_event(self, e):
        self.events.append(e)

    def update(self, time_delta):
        self.check_events(time_delta)
        self.draw(time_delta)


def is_cancel(pos, board):
    if board.cross_x <= pos[0] <= board.cross_x + board.cell_side and \
            board.cross_y <= pos[1] <= board.cross_y + board.cell_side:
        return True
    return False


def found_object(cords):
    for i in list_obj:
        if i.x <= cords[0] <= i.x + i.w and i.y <= cords[1] <= i.y + i.h:
            return i
    return None


class Player:
    class Events:
        def __init__(self, go_func=None):
            self.go_events = list()
            self.events_set = set()
            self.reaction_dict = {
                'go': go_func
            }

        def clear(self):
            self.go_events = list()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w, self.h = 50, 50
        self.events = Player.Events(self.go)
        self.animation_dict = {
            'go_forward': Animation('sheet.png', 4, 3)
        }
        self.animation = Animation('idle.png', 1, 1)
        self.move_buffer = [0, 0]
        self.obj_type = 'Player'
        self.speed = 70  # Points per second
        self.sprite = pygame.image.load('player_sprite.png').convert()
        self.sprite_size = self.sprite.get_rect().size
        self.has_opened_window = False
        self.game_state = 'game'
        self.inventory = Inventory()
        self.board = self.inventory
        self.cur_weapon = Weapon()
        self.inventory.content = [Weapon(), Weapon(), Weapon()]
        self.buffer = None
        self.chest = None

    def check_events(self, time_delta):
        if not self.has_opened_window:
            for i in self.events.events_set:
                self.events.reaction_dict[i](time_delta)

        self.events.clear()

    def change_pos(self):
        self.x += self.move_buffer[0]
        self.y += self.move_buffer[1]
        self.move_buffer = [0, 0]

    def move(self, x, y):
        self.move_buffer[0] += x
        self.move_buffer[1] += y

    def append_chest(self, chest):
        self.chest = chest

    def go(self, time_delta):
        self.animation = self.animation_dict['go_forward']
        amount_of_pixels_to_move = self.speed / 1000 * time_delta
        x_move, y_move = 0, 0

        if 'forward' in self.events.go_events:
            y_move -= amount_of_pixels_to_move
        if 'backward' in self.events.go_events:
            y_move += amount_of_pixels_to_move
        if 'left' in self.events.go_events:
            x_move -= amount_of_pixels_to_move
        if 'right' in self.events.go_events:
            x_move += amount_of_pixels_to_move

        if x_move and y_move:
            x_move /= math.sqrt(2)
            y_move /= math.sqrt(2)

        self.move(x_move, y_move)

    def draw(self, time_delta):
        cur_image = self.animation.get_next_sprite(time_delta)
        image_cords = (self.x - self.sprite_size[0] // 2,
                       self.y - self.sprite_size[1] // 2)
        win.blit(cur_image, image_cords)

    def update(self, time_delta):
        self.check_events(time_delta)
        self.change_pos()
        self.draw(time_delta)

    def create_buffer(self, pos, thing: Weapon, cell, board):
        y = (cell // 4) * board.cell_side + board.cells_y
        x = (cell % 4) * board.cell_side + board.cells_x
        delta_x = pos[0] - x
        delta_y = pos[1] - y
        thing.append_in_buffer(delta_x, delta_y, pos)
        self.buffer = thing, board, cell

    def delete_buffer(self):
        print(self.buffer)
        self.buffer[0].delete_from_buffer()
        self.buffer = None

    def open_window(self, game_state):
        self.game_state = game_state
        self.has_opened_window = True

    def close_window(self):
        self.game_state = 'game'
        self.has_opened_window = False


class ChestInventoryGUI:
    def __init__(self, chest: Chest, inventory: Inventory, player: Player):
        self.inventory = inventory
        self.chest = chest
        self.player = player

    def do_event(self, e, pos):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if is_cancel(pos, self.chest):
                return False
            cell = self.chest.get_cell(pos)
            board = self.chest
            if not cell:
                cell = self.inventory.get_cell(pos)
                board = self.inventory
            if cell and cell[1]:
                board.delete(cell[0])
                self.player.create_buffer(pos, cell[1], cell[0], board)
        elif e.type == pygame.MOUSEBUTTONUP:
            if self.player.buffer:
                cell = self.chest.get_cell(pos)
                board = self.chest
                if not cell:
                    cell = self.inventory.get_cell(pos)
                    board = self.inventory
                if cell:
                    board.append(cell[1])
                else:
                    self.player.buffer[1].append(self.player.buffer[0])
                self.player.delete_buffer()
        elif e.type == pygame.MOUSEMOTION:
            if self.player.buffer:
                self.player.buffer[0].update_pos(pos)
        return True

    def update(self):
        pass


class MouseController:
    def __init__(self):
        self.chest_inventory_gui = None

    def check_events(self, e, mouse_pos, player):
        if self.chest_inventory_gui and player.game_state == 'chest':
            if not self.chest_inventory_gui.do_event(e, mouse_pos):
                self.chest_inventory_gui = None
            print('send.message to CIGUI')
        if e.type == pygame.MOUSEBUTTONDOWN:
            obj = found_object(mouse_pos)
            #if obj:
                #obj.events.append('Mouse_down')
            if type(obj) == Chest:
                self.chest_inventory_gui = ChestInventoryGUI(obj, player.inventory, player)
                obj.state = 'open'
                player.game_state = 'chest'
                player.inventory.state = 'open'
                print('create bufffer')
        elif e.type == pygame.MOUSEBUTTONUP:
            pass
        elif e.type == pygame.MOUSEMOTION:
            pass


class KeyController:
    def __init__(self, obj):
        if obj.obj_type == 'Player':
            self._init_player(obj)

    def _init_player(self, player):
        self.player_obj = player
        self.go_controls = {
            keys_dict[CONFIG.get('PlayerMovementControls', 'forward')]: 'forward',
            keys_dict[CONFIG.get('PlayerMovementControls', 'backward')]: 'backward',
            keys_dict[CONFIG.get('PlayerMovementControls', 'left')]: 'left',
            keys_dict[CONFIG.get('PlayerMovementControls', 'right')]: 'right',

        }

    def send_actions(self, keys_checker):
        for i in self.go_controls:
            if keys_checker[i] and not self.player_obj.has_opened_window:
                self.player_obj.events.go_events.append(self.go_controls[i])
                self.player_obj.events.events_set.add('go')


class Game:
    def __init__(self):
        self.RUN = True
        self.game_state = 'game'
        self.global_game_time = 0
        self.CUR_time_delta = 0
        self.clocker = pygame.time.Clock()
        self.player = Player(100, 100)
        self.inventory = self.player.inventory
        self.chest = Chest(300, 300, Weapon(), Weapon())
        self.object_list = [self.player, self.inventory, self.chest]
        self.key_controller = KeyController(self.player)
        self.mouse_controller = MouseController()

    def check_keyboard(self):
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        self.RUN = False

        keys_checker = pygame.key.get_pressed()
        self.key_controller.send_actions(keys_checker)

    def check_collisions(self):
        pass

    def time_delta_update(self):
        self.CUR_time_delta = self.clocker.get_time()
        if self.CUR_time_delta < 8:
            pygame.time.wait(8 - self.CUR_time_delta)
            self.CUR_time_delta = 8

    def update_state(self):
        win.fill(pygame.Color('Black'))

        for obj in self.object_list:
            obj.update(100)

        pygame.display.flip()

    def runGame(self):
        while self.RUN:
            mouse_pos = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.RUN = False
                self.mouse_controller.check_events(e, mouse_pos, self.player)
            self.check_keyboard()

            self.update_state()
            self.time_delta_update()
            self.clocker.tick(50)


pygame.init()
win = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("Game")
game = Game()
list_obj = game.object_list
game.runGame()



    # print(proj_clock.get_fps())

pygame.quit()
