#Ponto Raster baseado em coordenadas da tela do programa.
class RPoint:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def to_position(self):
        #Isto é um importe local, e não afeta em nada no desempenho.
        #Util para mostrar quais funções e classes usam a livraria.
        import pygame
        window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
        return Position(self.x - window_x_center, -self.y + window_y_center)

#Ponto Cartesiano, vai de −1,0 a 1,0 conforme o canto da tela.
class CPoint:
    def __init__(self, x: float | int, y: float | int):
        x = float(x)
        y = float(y)
        self.x = ((x + 1) % 2) - 1 #Formula complicada para limitar o valor entre -1,0 e 1,0.
        self.y = ((y + 1) % 2) - 1

    def to_raster(self):
        import pygame
        x = self.x
        y = self.y * -1
        window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
        raster_x = (window_x_center * x) + window_x_center
        raster_y = (window_y_center * y) + window_y_center
        return RPoint(raster_x, raster_y)

    def to_position(self):
        import pygame
        x = self.x
        y = self.y
        window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
        pos_x = (window_x_center * x)
        pos_y = (window_y_center * y)
        return Position(pos_x, pos_y)

#Funciona do jeito convencional de coordenada, sendo x = 0, y = 0 o centro.
class Position:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def to_raster(self) -> RPoint:
        return RPoint(self.x, -self.y)

#Diferente de um Rect comum, Square é um objeto dinâmico que muda de acordo com seus dados;
#pode ser até considerado mais caro que um Simples Rect.
class Square:
    import pygame
    def __init__(self, pos: Position | RPoint | CPoint, size: float | int):
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        self._pos_ = pos
        self.size = float(size)

    def set_pos(self, pos: Position | RPoint | CPoint | tuple[float, float] | tuple[int, int]):
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        elif isinstance(pos, tuple):
            pos = Position(float(pos[0]), float(pos[1]))
        self._pos_ = pos

    #Se from_corner é True o Rect retornado tera seu ponto de origem no centro.
    def create_rect(self, from_corner = False):
        import pygame
        raster_pos = self._pos_
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

    def create_rect_raster(self, from_corner = False):
        import pygame
        raster_pos = self._pos_.to_raster()
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

    #Desenha o quadrado na tela.
    def draw(self, surface: pygame.Surface, color: pygame.Color, from_corner = False):
        import pygame
        rect = self.create_rect_raster(from_corner)
        pygame.draw.rect(surface, color, rect)

#class Button:
#    def __init__(self, pos: Position | RPoint | CPoint):
#        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
#            pos = pos.to_position()
#        self._pos_ = pos
#