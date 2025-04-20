import pygame

pygame.init()

window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

running = True

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

#Ponto Cartesiano, vai de −1,0 a 1,0 conforme o canto da tela.
class CPoint:
    def __init__(self, x, y):
        self.x = float(x) % 1.0
        self.y = float(y) % 1.0

class Square:
    def __init__(self, point: Point, size):
        self.pos = point
        self.size = float(size)

    def create_rect(self):
        left = self.pos.x - self.size / 2
        top = self.pos.y - self.size / 2
        return pygame.Rect(left, top, self.size, self.size)

    #Desenha o quadrado na tela.
    def draw(self, surface: pygame.Surface, color: pygame.Color):
        pygame.draw.rect(surface, color, self.create_rect())

def to_cartesian(raster_point: Point):
    x, y = raster_point

    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
    cart_x = (x - window_x_center) / window_x_center
    cart_y = (window_y_center - y) / window_y_center

    return cart_x, cart_y

def to_raster(caster_point: CPoint):
    x, y = caster_point
    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())

    raster_x = (window_x_center * x) + window_x_center
    raster_y = (window_y_center * y) + window_y_center

    return raster_x, raster_y

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    quadrado = Square(Point(0.0, 0.0), 25.5)

    mouse_pos = to_cartesian(pygame.mouse.get_pos())

    mouse_x_abs = (mouse_pos[0] * mouse_pos[0]) ** 0.5
    mouse_y_abs = (mouse_pos[1] * mouse_pos[1]) ** 0.5

    distance_color = 127.0 * (mouse_y_abs + mouse_x_abs)

    window.fill([distance_color, distance_color, distance_color])

    cor = pygame.Color(123, 123, 189)
    quadrado.draw(pygame.display.get_surface(), cor)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()