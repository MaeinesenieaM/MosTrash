from mostrash import *

#A partir daqui é o código da demonstração.
pygame.init()

window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

running = True

quadrado = Square(Point(0.0, 0.0), 0.0)
quadrado_mouse = Square(Point(0, 0), 10)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = to_cartesian(pygame.mouse.get_pos())

    mouse_x_abs = (mouse_pos.x * mouse_pos.x) ** 0.5
    mouse_y_abs = (mouse_pos.y * mouse_pos.y) ** 0.5

    distance_color = 127.0 * (mouse_y_abs + mouse_x_abs)

    window.fill([distance_color, distance_color, distance_color])

    quadrado.size = quadrado.size + 0.5
    quadrado.draw(pygame.display.get_surface(), pygame.Color(20, 20, 20), from_corner = True)

    quadrado_mouse.set_pos(mouse_pos)
    quadrado_mouse.draw(pygame.display.get_surface(), pygame.Color(198, 20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()