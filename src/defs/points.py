import pygame

class RPoint:
    """Ponto Raster baseado em coordenadas da tela do programa.
    (0, 0) seria o canto superior esquerdo da tela neste caso.
    """
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def to_position(self):
        """Converte RPoint, para Position."""
        import pygame

        window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
        return Position(self.x - window_x_center, -self.y + window_y_center)

    def get_vector(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y)

class CPoint:
    """Ponto Cartesiano, vai de −1,0 a 1,0 conforme o canto da tela.
    (1.0, 0.0) seria o centro do canto direito da tela.
    """
    def __init__(self, x: float | int, y: float | int):
        x = float(x)
        y = float(y)
        self.x = ((x + 1) % 2) - 1 #Formula complicada para limitar o valor entre -1,0 e 1,0.
        self.y = ((y + 1) % 2) - 1

    def to_raster(self):
        """Converte CPoint, para RPoint."""
        import pygame

        x = self.x
        y = self.y * -1
        window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
        raster_x = (window_x_center * x) + window_x_center
        raster_y = (window_y_center * y) + window_y_center
        return RPoint(raster_x, raster_y)

    def to_position(self):
        """Converte CPoint, para Position"""
        import pygame

        x = self.x
        y = self.y
        window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
        pos_x = (window_x_center * x)
        pos_y = (window_y_center * y)
        return Position(pos_x, pos_y)

    def get_vector(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y)

class Position:
    """Funciona do jeito convencional de coordenada.
    Diferente dos outros pontos, este é completamente independente da tela.
    Normalmente usado em conjunto com a camera.
    """
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)


    def to_raster(self) -> RPoint:
        """Converte Position, paa RPoint"""
        width, height = pygame.display.get_window_size()
        return RPoint(width / 2 - self.x, height / 2 + self.y)

    def to_raster_raw(self) -> tuple[float, float]:
        width, height = pygame.display.get_window_size()
        return width / 2 - self.x, height / 2 + self.y

    def get_vector(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y)

    def offset(self, x_offset: float, y_offset: float) -> tuple[float, float]:
        return self.x + x_offset, self.y + y_offset

def raster_to_cartesian(raster_point: RPoint | tuple[float, float] | tuple[int, int]) -> CPoint:
    """Converte RPoint, para CPoint."""
    import pygame

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


def cartesian_to_raster(caster_point: CPoint | tuple[float, float] | tuple[int, int]) -> RPoint:
    """Converte CPoint, para RPoint."""
    import pygame

    if isinstance(caster_point, tuple):
        x = float(caster_point[0])
        y = float(caster_point[1]) * -1
    else:
        x = caster_point.x
        y = caster_point.y * -1

    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
    raster_x = (window_x_center * x) + window_x_center
    raster_y = (window_y_center * y) + window_y_center
    return RPoint(raster_x, raster_y)

def to_position(point: RPoint | CPoint | tuple[float, float] | tuple[int, int]):
    """Converte RPoint ou CPoint em Position."""
    import pygame

    match point:
        case RPoint():
            return point.to_position()

        case CPoint():
            return point.to_position()

    window_x_center, window_y_center = map(lambda val: val / 2, pygame.display.get_window_size())
    return Position(point[0] - window_x_center, -point[1] + window_y_center)