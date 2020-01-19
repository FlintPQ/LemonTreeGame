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
    def __init__(self, filename='None', cols=-1, rows=-1, ):
        self.sprite_sheet = SpriteSheet(filename, cols, rows)

    def get
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.image.save(SpriteSheet('sheet.png', 6, 4).get_sprite(0), 'opa.png')