import pygame

pygame.init()

window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

running = True

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class FPoint:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

class Square:
    def __init__(self, point, size):
        self.pos = point
        self.size = float(size)

def to_cartesian(raster_point):
    x, y = raster_point

    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
    cart_x = (x - window_x_center) / window_x_center
    cart_y = (window_y_center - y) / window_y_center

    return cart_x, cart_y

def to_raster(caster_point):
    x, y = caster_point
    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())

    raster_x = (window_x_center * x)+ window_x_center
    raster_y = (window_y_center * y)+ window_y_center

    return raster_x, raster_y

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    quadrado = Square(FPoint(0.0, 0.0), 25.5)

    mouse_pos = to_cartesian(pygame.mouse.get_pos())

    mouse_x_abs = (mouse_pos[0] * mouse_pos[0]) ** 0.5
    mouse_y_abs = (mouse_pos[1] * mouse_pos[1]) ** 0.5

    distance_color = 127.0 * (mouse_y_abs + mouse_x_abs)

    window.fill([distance_color, distance_color, distance_color])

    rect = pygame.Rect(10.0, 10.0, 10.0, 10.0)

    pygame.draw.rect(pygame.display.get_surface(), [123, 123, 189] , rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()