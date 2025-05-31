from points import *

class Entity:
    from pygame import Color, Rect

    def rects(self, color: Color = Color(175, 175, 175)) -> list[tuple[Rect, Color]]:
        return []

#Diferente de um Rect comum, Square é um objeto dinâmico que muda de acordo com seus dados;
#pode ser até considerado mais caro que um Simples Rect.
class Square(Entity):
    from pygame import Color, Rect

    def __init__(self, pos: Position | RPoint | CPoint, size: float | int):
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        self._pos = pos
        self.size = float(size)

    def set_pos(self, pos: Position | RPoint | CPoint | tuple[float, float] | tuple[int, int]):
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        elif isinstance(pos, tuple):
            pos = Position(float(pos[0]), float(pos[1]))
        self._pos = pos

    #Se from_corner é True o Rect retornado tera seu ponto de origem no centro.
    def create_rect(self, from_corner = False):
        from pygame import Rect

        raster_pos = self._pos
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return Rect(x, y, self.size, self.size)

    def create_rect_raster(self, from_corner = False):
        from pygame import Rect

        raster_pos = self._pos.to_raster()
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return Rect(x, y, self.size, self.size)

    def rects(self, color: Color = Color(175, 175, 175)) -> list[tuple[Rect, Color]]:
        from pygame import Color
        return [(self.create_rect(), Color(175, 175, 175))]

class Button(Entity):
    from pygame import Color, Rect
    from collections.abc import Callable

    def __init__(self, pos: Position | RPoint | CPoint, size: float | int, callback: Callable[[], None] = None):
        from collections.abc import Callable

        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        self._pos = pos
        self.size = float(size)
        self._callback: Callable[[], None] | None = callback

    def set_callback(self, callback: Callable[[], None]):
        self._callback = callback

    def run_callback(self):
        if self._callback: self._callback()
        
    def has_point(self, pos: Position | RPoint | CPoint) -> bool:
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()

        inside_x = self._pos.x - self.size < pos.x < self._pos.x + self.size
        inside_y = self._pos.y - self.size < pos.y < self._pos.y + self.size

        return inside_x and inside_y

    def get_inner_rect(self, from_corner = False) -> Rect:
        import pygame

        raster_pos = self._pos.to_raster()
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

    def get_outer_rect(self, from_corner = False):
        import pygame

        raster_pos = self._pos.to_raster()
        offset = 5.0
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - (offset / 2 + self.size / 2)
            y = y - (offset / 2 + self.size / 2)
        return pygame.Rect(x, y, self.size + offset, self.size + offset)

    def rects(self, color: Color = Color(175, 175, 175)) -> list[tuple[Rect, Color]]:
        from pygame import Color
        return [(self.get_outer_rect(), color), (self.get_inner_rect(), Color(43, 164, 43))]