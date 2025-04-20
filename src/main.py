import pygame

class Point:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

#Ponto Cartesiano, vai de −1,0 a 1,0 conforme o canto da tela.
class CPoint:
    def __init__(self, x: float | int, y: float | int):
        x = float(x)
        y = float(y)
        self.x = ((x + 1) % 2) - 1 #Formula complicada para limitar o valor entre -1,0 e 1,0.
        self.y = ((y + 1) % 2) - 1

#Diferente de um Rect comum, Square é um objeto dinâmico que muda de acordo com seus dados;
#pode ser até considerado mais caro que um Simples Rect.
class Square:
    def __init__(self, point: Point | CPoint, size):
        if isinstance(point, CPoint):
            point = to_raster(point)
        self._pos_ = point
        self.size = float(size)

    def set_pos(self, point: Point | CPoint | tuple[float, float] | tuple[int, int]):
        if isinstance(point, CPoint):
            point = to_raster(point)
        elif isinstance(point, tuple):
            point = Point(float(point[0]), float(point[1]))
        self._pos_ = point

    #Se from_corner é True o Rect retornado tera seu ponto de origem no centro.
    def create_rect(self, from_corner = False):
        x = self._pos_.x
        y = self._pos_.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

    #Desenha o quadrado na tela.
    def draw(self, surface: pygame.Surface, color: pygame.Color, from_corner = False):
        pygame.draw.rect(surface, color, self.create_rect(from_corner))

def to_cartesian(raster_point: Point | tuple[float, float] | tuple[int, int]):
    if isinstance(raster_point, tuple):
        x = float(raster_point[0])
        y = float(raster_point[1])
    else:
        x = raster_point.x
        y = raster_point.y

    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
    cart_x = (x - window_x_center) / window_x_center
    cart_y = (window_y_center - y) / window_y_center
    return CPoint(cart_x, cart_y)

def to_raster(caster_point: CPoint | tuple[float, float]):
    if isinstance(caster_point, tuple):
        x = float(caster_point[0])
        y = float(caster_point[1]) * -1
    else:
        x = caster_point.x
        y = caster_point.y * -1

    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
    raster_x = (window_x_center * x) + window_x_center
    raster_y = (window_y_center * y) + window_y_center
    return Point(raster_x, raster_y)

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