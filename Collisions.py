import pygame as pg


class Player:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 50
        self.height = 50
        self.speed = 50
        self.direction = None
        self.rect = [self.x, self.y, self.width, self.height]
        self.dir_dict = {'Right': lambda x: [x[0] + self.speed, x[1], x[2], x[3]],
                         'Left': lambda x: [x[0] - self.speed, x[1], x[2], x[3]],
                         'Down': lambda x: [x[0], x[1] + self.speed, x[2], x[3]],
                         'Up': lambda x: [x[0], x[1] - self.speed, x[2], x[3]],
                         None: self.rect}
        self.update(self.direction)

    def draw(self, screen):
        pg.draw.rect(screen, (255, 0, 0), self.rect)

    def update(self, direction):
        self.next_rect = self.dir_dict[self.direction]


class GameState:
    def __init__(self, player, *objects):
        self.player = player
        self.list_objects = list(objects).append(player)
        self.clock = pg.time.Clock()
        self.display: pg.Surface = pg.display.set_mode((1600, 900), 0, 32)
        self.pressed = []

    def check_collision(self, obj, direct):
        for j in self.list_objects:
            if obj != j and pg.Rect.colliderect(obj.next_rect, j.next_rect) and direct == 'Left':
                obj.send_event(('collision', 'L'))
                break
            elif obj != j and pg.Rect.colliderect(obj.next_rect, j.next_rect) and direct == "Right":
                obj.send_event(('collision', 'R'))
                break
            elif obj != j and pg.Rect.colliderect(obj.next_rect, j.next_rect) and direct == "Up":
                obj.send_event(('collision', 'U'))
                break
            elif obj != j and pg.Rect.colliderect(obj.next_rect, j.next_rect) and direct == "Down":
                obj.send_event(('collision', 'D'))
                break
            elif obj != j and direct == 'Left':
                obj.x -= obj.speed
                break
            elif obj != j and direct == 'Right':
                obj.x += obj.speed
                break
            elif obj != j and direct == 'Up':
                obj.y -= obj.speed
                break
            elif obj != j and direct == 'Down':
                obj.y += obj.speed
                break

    def run(self):
        self.display.fill(pg.Color('White'))
        self.pressed = pg.key.get_pressed()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                break
            if self.pressed[pg.K_RIGHT]:
                self.player.update('Right')
                self.check_collision(self.player, 'Right')
            elif self.pressed[pg.K_LEFT]:
                self.player.update('Left')
                self.check_collision(self.player, 'Left')
            elif self.pressed[pg.K_UP]:
                self.player.update('Up')
                self.check_collision(self.player, 'Up')
            elif self.pressed[pg.K_DOWN]:
                self.player.update('Down')
                self.check_collision(self.player, 'Down')
        for i in self.list_objects:
            i.draw()

        self.clock.tick(60)
        pg.display.flip()
