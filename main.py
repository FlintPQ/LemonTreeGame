import math
import string
from config import CONFIG
import pygame
from config import CONFIG, keys_dict
from utils import Animation


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

    def __init__(self, cords: list):
        self.cords = cords
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

    def check_events(self, time_delta):
        for i in self.events.events_set:
            self.events.reaction_dict[i](time_delta)

        self.events.clear()

    def change_pos(self):
        self.cords[0] += self.move_buffer[0]
        self.cords[1] += self.move_buffer[1]
        self.move_buffer = [0, 0]

    def move(self, x, y):
        self.move_buffer[0] += x
        self.move_buffer[1] += y

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
        image_cords = (self.cords[0] - self.sprite_size[0] // 2, self.cords[1] - self.sprite_size[1] // 2)
        win.blit(cur_image,  image_cords)

    def update(self, time_delta):
        self.check_events(time_delta)
        self.change_pos()
        self.draw(time_delta)


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
            if keys_checker[i]:
                self.player_obj.events.go_events.append(self.go_controls[i])
                self.player_obj.events.events_set.add('go')


class Game:
    def __init__(self):
        self.RUN = True
        self.global_game_time = 0
        self.CUR_time_delta = 0
        self.clocker = pygame.time.Clock()
        self.player = Player([100, 100])
        self.object_list = list().append(self.player)
        self.key_controller = KeyController(self.player)

    def check_keyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_checker = pygame.key.get_pressed()
        self.key_controller.send_actions(keys_checker)

    def check_collisions(self):

    def time_delta_update(self):
        self.CUR_time_delta = self.clocker.get_time()
        if self.CUR_time_delta < 8:
            pygame.time.wait(8 - self.CUR_time_delta)
            self.CUR_time_delta = 8

    def update_state(self):
        win.fill(pygame.Color('Black'))

        for obj in self.object_list:
            obj.update()

        pygame.display.flip()

    def runGame(self):
        while self.RUN:
            self.clocker.tick()
            self.check_keyboard()
            self.update_state()
            self.time_delta_update()

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game")




    # print(proj_clock.get_fps())

pygame.quit()
