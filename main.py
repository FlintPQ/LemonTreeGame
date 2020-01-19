import math
import string
from config import CONFIG
import pygame
from config import CONFIG, keys_dict

class Player:
    class Events:
        def __init__(self):
            self.go_events = list()

        def clear(self):
            self.go_events = list()

    def __init__(self, cords: list):
        self.cords = cords
        self.events = Player.Events()
        self.move_buffer = [0, 0]
        self.obj_type = 'Player'
        self.speed = 70  # Points per second
        self.sprite = pygame.image.load('player_sprite.png').convert()
        self.sprite_size = self.sprite.get_rect().size

    def check_events(self, time_delta):
        if self.events.go_events:
            self.go(time_delta)

        self.events.clear()


    def change_pos(self):
        self.cords[0] += self.move_buffer[0]
        self.cords[1] += self.move_buffer[1]
        self.move_buffer = [0, 0]

    def move(self, x, y):
        self.move_buffer[0] += x
        self.move_buffer[1] += y

    def go(self, time_delta):
        if len(self.events.go_events) > 1:
            pass
            g = 7
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

    def draw(self):
        image_cords = (self.cords[0] - self.sprite_size[0] // 2, self.cords[1] - self.sprite_size[1] // 2)
        win.blit(self.sprite, image_cords)


    def update(self, time_delta):
        self.check_events(time_delta)
        self.change_pos()
        self.draw()


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

    def do_actions(self, keys_checker):
        for i in self.go_controls:
            if keys_checker[i]:
                self.player_obj.events.go_events.append(self.go_controls[i])


pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game")
time_delta = 0
run = True
proj_clock = pygame.time.Clock()
player = Player([100, 100])

MainGameController = KeyController(player)

while run:
    proj_clock.tick()
    win.fill(pygame.Color('Black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys_checker = pygame.key.get_pressed()
    MainGameController.do_actions(keys_checker)

    player.update(time_delta)
    #print(type(player))


    pygame.display.flip()

    time_delta = proj_clock.get_time()
    if time_delta < 8:
        pygame.time.wait(8 - time_delta)
        time_delta = 8

    #print(proj_clock.get_fps())

pygame.quit()