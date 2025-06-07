import pygame

from src.defs.points import *
from src.defs.colors import *
from src.assets import Assets

class Entity:
    """EM PROGRESSO!
    Uma classe entidade para fornecer funções comuns que todos os objetos devem ter.
    """
    from pygame import Color, Rect

    def rects(self, color: Color = Color(175, 175, 175)) -> list[tuple[Rect, Color]]:
        """Formata os retângulos de um objeto junto som suas respectivas cores."""
        return []

class Square(Entity, pygame.sprite.Sprite):
    """
    Diferente de um Rect comum, Square é um objeto dinâmico que muda de acordo com seus dados;
    pode ser até considerado mais caro que um Simples Rect, mesmo sendo apenas um quadrado.
    """
    from pygame import Color, Rect

    def __init__(self, pos: Position | RPoint | CPoint, size: float | int):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        self.pos = pos
        self.size = float(size)

    def set_pos(self, pos: Position | RPoint | CPoint | tuple[float, float] | tuple[int, int]):
        """muda a posição do quadrado"""
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        elif isinstance(pos, tuple):
            pos = Position(float(pos[0]), float(pos[1]))
        self.pos = pos

    def create_rect(self, from_corner = False) -> Rect:
        """Retorna um Rect do Square.
        Se from_corner é True o Rect retornado tera seu ponto de origem no canto.
        """
        from pygame import Rect

        raster_pos = self.pos
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return Rect(x, y, self.size, self.size)

    def create_rect_raster(self, from_corner = False):
        """Retorna um Rect baseado em coordenada rasterizada."""
        from pygame import Rect

        raster_pos = self.pos.to_raster()
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return Rect(x, y, self.size, self.size)

    def rects(self, color: Color = Color(175, 175, 175)) -> list[tuple[Rect, Color]]:
        return [(self.create_rect(), color)]

class Button(Entity, pygame.sprite.Sprite):
    """
    Button é um objeto que funciona como um botão que guarda uma função específica dentro dele.
    Para incluir uma função no botão utilize set_callback().
    """
    from pygame import Color, Rect
    from collections.abc import Callable

    def __init__(
        self,
        pos: Position | RPoint | CPoint,
        size: float | int,
        callback: Callable[..., any] = None,
    ):
        from collections.abc import Callable
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        self.pos = pos
        self.size = float(size)
        self._callback: Callable[[], any] | None = callback

    def set_callback(self, callback: Callable[[], any]):
        """Guarda uma função no botão."""
        self._callback = callback

    def run_callback(self) -> any:
        """Caso o botão tenha uma função guardada, ira chamá-la e retornar seu resultado."""
        if self._callback: return self._callback()
        
    def has_point(self, pos: Position | RPoint | CPoint) -> bool:
        """Verifica se um ponto está dentro do botão."""
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()

        inner_size = self.size / 2
        inside_x = self.pos.x - inner_size < pos.x < self.pos.x + inner_size
        inside_y = self.pos.y - inner_size < pos.y < self.pos.y + inner_size

        return inside_x and inside_y

    def _get_inner_rect(self, from_corner = False) -> Rect:
        #raster_pos = self._pos.to_raster()
        x = self.pos.x
        y = -self.pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

    def _get_outer_rect(self, from_corner = False) -> Rect:
        #raster_pos = self._pos.to_raster()
        offset = self.size / 2
        x = self.pos.x
        y = -self.pos.y
        if not from_corner:
            x = x - (offset / 2 + self.size / 2)
            y = y - (offset / 2 + self.size / 2)
        return pygame.Rect(x, y, self.size + offset, self.size + offset)

    def rects(self, color: Color = Color(175, 175, 175)) -> list[tuple[Rect, Color]]:
        from pygame import Color
        return [(self._get_outer_rect(), color), (self._get_inner_rect(), Color(43, 164, 43))]

class Bitmap(Entity, pygame.sprite.Sprite):
    from os import PathLike

    def __init__(
        self,
        pos: Position | RPoint | CPoint,
        image_path: PathLike
    ):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()

        self.pos = pos
        self.image = pygame.image.load(image_path).convert_alpha()

class Label(Position, Entity, pygame.sprite.Sprite):
    from os import PathLike
    from pygame import Color

    def __init__(
        self,
        pos: Position | RPoint | CPoint,
        text: str,
        font: PathLike = Assets().get_font_path("fixedsys"),
        size: int = 16,
        color: Color = WHITE
    ):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            print(pos.y)
            pos = pos.to_position()
            print(pos.y)

        self.pos = pos
        self._text = text
        self.font = pygame.font.Font(font, size)
        self._color = color
        self.texture = self.font.render(self._text, False, self._color)

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str):
        self._text = text
        self._update_text()

    def set_color(self, color: Color):
        self._color = color
        self._update_text()

    def _update_text(self):
        self.texture = self.font.render(self._text, False, self._color)