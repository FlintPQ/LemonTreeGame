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
        self.animation_speed = 2  # pics for sec
        self.cur_sprite_index = 0
        self._time_from_last_sprite_update_buffer = 0

    def get_next_sprite(self, timedelta, reversed=False):
        self._time_from_last_sprite_update_buffer += timedelta
        how_many_sprites_passed = self.animation_speed / 1000 * self._time_from_last_sprite_update_buffer

        if how_many_sprites_passed >= 1:
            if reversed:
                self.cur_sprite_index = (self.cur_sprite_index - math.floor(how_many_sprites_passed)) \
                                        % self.sprite_sheet.totalCellCount

            else:
                self.cur_sprite_index = (self.cur_sprite_index + math.floor(how_many_sprites_passed)) \
                                        % self.sprite_sheet.totalCellCount

        return self.sprite_sheet.get_sprite(self.cur_sprite_index)

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.image.save(SpriteSheet('sheet.png', 4, 3).get_sprite(2), 'opa.png')

