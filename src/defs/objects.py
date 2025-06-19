from src.defs.points import *
from src.defs.colors import *
from src.assets import Assets

class Entity:
    """EM PROGRESSO!
    Uma classe entidade para fornecer funções comuns que todos os objetos devem ter.
    """
    from pygame import Color, Rect

    def rects(self) -> list[tuple[Rect, Color]]:
        """Formata os retângulos de um objeto junto som suas respectivas cores."""
        return []

class Bitmap(Entity, pygame.sprite.Sprite):
    from os import PathLike

    def __init__(
        self,
        pos: Position | RPoint | CPoint | tuple[int, int],
        image_path: PathLike
    ):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, tuple):pos = Position(pos[0], pos[1])

        self.pos = pos
        self.image = pygame.image.load(image_path).convert_alpha()

    def set_image(self, image_path: PathLike):
        self.image = pygame.image.load(image_path).convert_alpha()

class BitmapChain:
    from os import PathLike

    def __init__(
        self,
        pos: Position | RPoint | CPoint | tuple[int, int],
        offset_pos: Position | RPoint | CPoint | tuple[int, int],
        quantity: int,
        image_path: PathLike
    ):
        if isinstance(pos, tuple): pos = Position(pos[0], pos[1])
        if isinstance(offset_pos, tuple): offset_pos = Position(offset_pos[0], offset_pos[1])

        self.pos = pos
        self.offset_pos = offset_pos

        self.quantity = quantity
        self._image_path = image_path
        self._sprites: [Bitmap] = []

        for _ in range(self.quantity):
            self._sprites.append(Bitmap(self.pos + self.offset_pos * len(self._sprites), self._image_path))

    def get_sprites(self) -> list[Bitmap]:
        return self._sprites

    def __int__(self):
        return self.quantity

    def __sub__(self, other: int):
        return self.quantity - other

    def __add__(self, other: int):
        return self.quantity + other

    def __isub__(self, other: int):
        for _ in range(other):
            self._sprites.pop()

        self.quantity -= other
        return self

    def __iadd__(self, other: int):
        for _ in range(other):
            self._sprites.append(Bitmap(self.pos + self.offset_pos * len(self._sprites), self._image_path))

        self.quantity += other
        return self

    def __eq__(self, other: int):
        return self.quantity == other

    def __ne__(self, other: int):
        return self.quantity != other

    def __lt__(self, other: int):
        return self.quantity < other

    def __le__(self, other: int):
        return self.quantity <= other

    def __gt__(self, other: int):
        return self.quantity > other

    def __ge__(self, other: int):
        return self.quantity >= other

class Label(Position, Entity, pygame.sprite.Sprite):
    from os import PathLike
    from pygame import Color

    def __init__(
        self,
        pos: Position | RPoint | CPoint | tuple[int, int],
        text: str,
        font: PathLike = Assets().get_font_path("fixedsys"),
        size: int = 16,
        color: Color = WHITE
    ):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, tuple): pos = Position(pos[0], pos[1])

        self.pos = pos
        self._text = text
        self.font = pygame.font.Font(font, size)
        self._color = color
        self.image = self.font.render(self._text, False, self._color)

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str):
        self._text = text
        self._update_text()
        return self

    def set_color(self, color: Color):
        self._color = color
        self._update_text()
        return self

    def _update_text(self):
        self.image = self.font.render(self._text, False, self._color)

class Square(Entity, pygame.sprite.Sprite):
    """
    Diferente de um Rect comum, Square é um objeto dinâmico que muda de acordo com seus dados;
    pode ser até considerado mais caro que um Simples Rect, mesmo sendo apenas um quadrado.
    """
    from pygame import Color, Rect

    def __init__(self, pos: Position | RPoint | CPoint, size: float | int, color = WHITE):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, CPoint) or isinstance(pos, RPoint): pos = pos.to_position()

        self.pos = pos
        self.color = color
        self.size = float(size)

    def set_pos(self, pos: Position | RPoint | CPoint | tuple[float, float] | tuple[int, int]):
        """muda a posição do quadrado"""
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()
        elif isinstance(pos, tuple):
            pos = Position(float(pos[0]), float(pos[1]))
        self.pos = pos
        return self

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

    def create_rect_raster(self, from_corner = False) -> Rect:
        """Retorna um Rect baseado em coordenada rasterizada."""
        from pygame import Rect

        raster_pos = self.pos.to_raster()
        x = raster_pos.x
        y = -raster_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return Rect(x, y, self.size, self.size)

    def rects(self) -> list[tuple[Rect, Color]]:
        return [(self.create_rect(), self.color)]

class Button(Entity, pygame.sprite.Sprite):
    """
    Button é um objeto que funciona como um botão que guarda uma função específica dentro dele.
    Para incluir uma função no botão utilize set_callback().
    """
    from pygame import Color, Rect
    from typing import Callable

    def __init__(
        self,
        pos: Position | RPoint | CPoint | tuple[int, int],
        size: float | int,
        callback: Callable[..., any] = None,
        color = GRAY,
        bitmap: Bitmap = None
    ):
        from collections.abc import Callable
        pygame.sprite.Sprite.__init__(self)
        if isinstance(pos, RPoint):
            pos = pos.to_position()
        if isinstance(pos, tuple):
            pos = Position(pos[0], pos[1])

        self.pos = pos
        self.size = float(size)
        self.color = color
        self.bitmap = bitmap
        self._callback: Callable[[], any] | None = callback

    def set_callback(self, callback: Callable[[], any]):
        """Guarda uma função no botão."""
        self._callback = callback
        return self

    def run_callback(self) -> any:
        """Caso o botão tenha uma função guardada, ira chamá-la e retornar seu resultado."""
        if self._callback: return self._callback()
        
    def has_point(self, pos: Position | RPoint | CPoint) -> bool:
        """Verifica se um ponto está dentro do botão."""
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()

        if isinstance(self.pos, CPoint): temp_pos = self.pos.to_position()
        else: temp_pos = self.pos

        inner_size = self.size / 2
        inside_x = temp_pos.x - inner_size < pos.x < temp_pos.x + inner_size
        inside_y = temp_pos.y - inner_size < pos.y < temp_pos.y + inner_size

        return inside_x and inside_y

    def _get_inner_rect(self, from_corner = False) -> Rect:
        if isinstance(self.pos, CPoint): temp_pos = self.pos.to_position()
        else: temp_pos = self.pos
        x = temp_pos.x
        y = -temp_pos.y
        if not from_corner:
            x = x - self.size / 2
            y = y - self.size / 2
        return pygame.Rect(x, y, self.size, self.size)

    def _get_outer_rect(self, from_corner = False) -> Rect:
        if isinstance(self.pos, CPoint): temp_pos = self.pos.to_position()
        else: temp_pos = self.pos
        offset = self.size / 2
        x = temp_pos.x
        y = -temp_pos.y
        if not from_corner:
            x = x - (offset / 2 + self.size / 2)
            y = y - (offset / 2 + self.size / 2)
        return pygame.Rect(x, y, self.size + offset, self.size + offset)

    def rects(self) -> list[tuple[Rect, Color]]:
        from pygame import Color
        return [(self._get_outer_rect(), self.color), (self._get_inner_rect(), Color(43, 164, 43))]