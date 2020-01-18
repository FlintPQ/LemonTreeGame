import pygame


class Player:
    def __init__(self):
        self.sprite = pygame.image.load('player_sprite.png')
        self.speed = 50  # Points per sec

    def Draw(self):
        win.blit(self.sprite, )

class KeyController:
    def __init__(self):
        pass

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game")

run = True
proj_clock = pygame.time.Clock()


while run:
    time_delta = proj_clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    proj_clock.tick()
pygame.quit()