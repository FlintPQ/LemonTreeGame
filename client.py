from classes import *

pygame.init()

window1 = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
menu1 = Menu(init_buttons1(), init_circles())
clock = pygame.time.Clock()

while True:
    window1.fill(WHITE)
    button = menu1.check_mouse_pos()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            quit()

        if i.type == pygame.MOUSEBUTTONUP and button:
            print(button.text)

    if button:
        button.delta = 10
    else:
        for i in menu1.buttons:
            i.delta = 0

    for i in menu1.buttons:
        i.update()

    menu1.draw_animation(menu1.circles, window1)

    for i in menu1.circles:
        i.move()

    menu1.draw(window1)

    clock.tick(FRAMES_PER_SECOND)
    pygame.display.update()