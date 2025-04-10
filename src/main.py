import pygame

pygame.init()

window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_y = (mouse_pos[1] % 255)
    window.fill([mouse_y, mouse_y, mouse_y])

    pygame.display.flip()
    clock.tick(60)


def edge_center():
    

pygame.quit()