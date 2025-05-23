import pygame
from objects import *

#Aki é o arquivo principal onde podemos conectar modulos e criar outras funções globais.
class World:
    def __init__(self):
        self.entities = {}

    def insert_object(self, obj):
        obj_name = obj.__class__.__name__
        self.entities.setdefault(obj_name, []).append(obj)

class Camera:
    def __init__(self, display: pygame.surface.Surface):
        self.width = float(display.get_width())
        self.height = float(display.get_height())
        self._display = display
        self.pos = Position(0.0, 0.0)

    def update(self):
        self.width = float(self._display.get_width())
        self.height = float(self._display.get_height())

    def get_pos_tuple(self) -> (int, int):
        return self.pos.x, self.pos.y

    def apply_offset(self, rect: pygame.Rect):
        offset_x, offset_y = self.get_offset()
        rect.move_ip(offset_x, offset_y)

    def draw_rect(self,  color: pygame.Color, rect: pygame.Rect):
        offset_x, offset_y = self.get_offset()
        rect.move_ip(offset_x, offset_y)
        pygame.draw.rect(self._display, color, rect)

    def get_offset(self) -> (int, int):
        width_center = self.width / 2
        height_center = self.height / 2
        return -self.pos.x + width_center, self.pos.y + height_center

class Input:
    def __init__(self):
        self.keyboard_keys = []

_input_controller = Input()

def update_input_controller():
    _input_controller.keyboard_keys = pygame.key.get_pressed()

#Recebe a chave de um input, como o do teclado, por exemplo.
def get_key(key: str) -> int:
    return pygame.key.key_code(key)

#Recebe uma classe de Event que pode ser usada para ser enviada com o pygame.event.post()
def get_event(event_id: int) -> pygame.event.Event:
    return pygame.event.Event(event_id)

def is_key_pressed(key: str) -> bool:
    return _input_controller.keyboard_keys[get_key(key)]

def to_cartesian(raster_point: RPoint | tuple[float, float] | tuple[int, int]) -> CPoint:
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

def to_raster(caster_point: CPoint | tuple[float, float]) -> RPoint:
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