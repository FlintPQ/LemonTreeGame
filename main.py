import string
from config import CONFIG
import pygame
from config import CONFIG, keys_dict

class Player:
    def __init__(self, cords: list):
        self.cords = cords
        self.obj_type = 'Player'
        self.speed = 70  # Points per second
        self.sprite = pygame.image.load('player_sprite.png')
        self.sprite_size = self.sprite.get_rect().size

    def move(self, direction):
        amount_of_pixels_to_move = self.speed / 1000 * time_delta
        if direction == 'forward':
            self.cords[1] -= amount_of_pixels_to_move
        elif direction == 'backward':
            self.cords[1] += amount_of_pixels_to_move
        elif direction == 'left':
            self.cords[0] -= amount_of_pixels_to_move
        elif direction == 'right':
            self.cords[0] += amount_of_pixels_to_move

    def move_forward(self):
        self.move('forward')

    def move_backward(self):
        self.move('backward')

    def move_left(self):
        self.move('left')

    def move_right(self):
        self.move('right')

    def draw(self):
        image_cords = (self.cords[0] - self.sprite_size[0] // 2, self.cords[1] - self.sprite_size[1] // 2)
        win.blit(self.sprite, image_cords)

    def update(self):
        self.draw()


class KeyController:
    def __init__(self, obj):
        if obj.obj_type == 'Player':
            self._init_player(obj)

    def _init_player(self, player):
        self.controls = {
            keys_dict[CONFIG.get('PlayerMovementControls', 'forward')]: player.move_forward,
            keys_dict[CONFIG.get('PlayerMovementControls', 'backward')]: player.move_backward,
            keys_dict[CONFIG.get('PlayerMovementControls', 'left')]: player.move_left,
            keys_dict[CONFIG.get('PlayerMovementControls', 'right')]: player.move_right,

        }

    def do_actions(self, keys_checker):
        for i in self.controls:
            if keys_checker[i]:
                self.controls[i]()

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

    player.update()
    #print(type(player))


    pygame.display.flip()

    time_delta = proj_clock.get_time()
    if time_delta < 8:
        pygame.time.wait(8 - time_delta)
        time_delta = 8

    #print(proj_clock.get_fps())

pygame.quit()