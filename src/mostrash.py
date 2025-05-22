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

#Recebe a chave de um input, como o do teclado, por exemplo.
def get_key(key: str) -> int:
    return pygame.key.key_code(key)

#Recebe uma classe de Event que pode ser usada para ser enviada com o pygame.event.post()
def get_event(event_id: int) -> pygame.event.Event:
    return pygame.event.Event(event_id)

def is_key_pressed(key: str) -> bool:
    keys = pygame.key.get_pressed()
    return keys[get_key(key)]