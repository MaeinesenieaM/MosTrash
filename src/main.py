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

#Diferente de um Rect comum, Square é um objeto dinâmico que muda de acorde com seus dados
#Pode ser até considerado mais caro que um Simples Rect.
class Square:
    def __init__(self, point: Point, size):
        self.pos = point
        self.size = float(size)

    #Se from_corner é True o Rect retornado tera seu ponto de origem no centro.
    def create_rect(self, point: Point, from_corner = False):
        if isinstance(point, CPoint):
            point = to_raster(point)
        x = point.x
        y = point.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

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

quadrado = Square(Point(0.0, 0.0), 25.5)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = to_cartesian(pygame.mouse.get_pos())

    mouse_x_abs = (mouse_pos[0] * mouse_pos[0]) ** 0.5
    mouse_y_abs = (mouse_pos[1] * mouse_pos[1]) ** 0.5

    distance_color = 127.0 * (mouse_y_abs + mouse_x_abs)

    window.fill([distance_color, distance_color, distance_color])

    cor = pygame.Color(123, 123, 189)
    quadrado.size = quadrado.size + 1
    quadrado.draw(pygame.display.get_surface(), cor)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()