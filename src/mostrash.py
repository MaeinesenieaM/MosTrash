import pygame
import os
import importlib.util

from objects import *
from points import *

from typing import Callable

class InputHandler:
    def __init__(self):
        self.keys_pressed = []
        self.keys_released = []

    def update(self, events):
        self.keys_pressed.clear()
        self.keys_released.clear()

        handled_events = []

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self.keys_pressed.append(event.key)
                    handled_events.append(event)
                case pygame.KEYUP:
                    self.keys_released.append(event.key)
                    handled_events.append(event)

        for event in handled_events:
            events.remove(event)

class EventManager:
    def __init__(self):
        self.inputs = InputHandler()

    #Atualiza eventos próprios também
    def pull_events(self) -> list:
        events = pygame.event.get()

        self.inputs.update(events)

        return events

class Context:
    def __init__(self, width: int, height: int):
        if not pygame.get_init(): pygame.init()
        self._window = pygame.display.set_mode((width, height), flags = pygame.RESIZABLE)
        self._clock = pygame.time.Clock()
        self._camera = Camera(self._window)

    def get_window(self):
        return self._window

    def get_clock(self):
        return self._clock

    def get_camera(self):
        return self._camera

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

    def get_offset(self) -> (int, int):
        width_center = self.width / 2
        height_center = self.height / 2
        return -self.pos.x + width_center, self.pos.y + height_center

    def apply_offset(self, rect: pygame.Rect):
        offset_x, offset_y = self.get_offset()
        rect.move_ip(offset_x, offset_y)

    def draw_rect(self, rect: pygame.Rect, color: pygame.Color):
        offset_x, offset_y = self.get_offset()
        rect.move_ip(offset_x, offset_y)
        pygame.draw.rect(self._display, color, rect)

    def draw(self, obj: Entity, color: pygame.Color | None = None):
        if color is None:
            bodies = obj.rects()
        else:
            bodies = obj.rects(color)

        for body in bodies:
            self.draw_rect(body[0], body[1])

class Games:
    def __init__(self):
        self._games = load_games()

    def get_game(self, category: str, game: str) -> Callable[[Context], bool] | None:
        if not category in self._games: return None
        elif not game in self._games[category]: return None
        return self._games[category][game]["module"].start

class Assets:
    def __init__(self):
        self._assets = load_assets()

    def get_sound_path(self, name):
        if not name in self._assets["sounds"]: return None
        return self._assets["sounds"][name]["path"]

    def get_image_path(self, name):
        if not name in self._assets["images"]: return None
        return self._assets["images"][name]["path"]

_event_manager = EventManager()

def init(width: int, height: int) -> Context:
    return Context(width, height)

def load_games():
    games = {}

    path_main = os.path.dirname(__file__)
    path_games = os.path.join(path_main, "games")

    #Carrega os scripts de cada minigame.
    for categoria in os.listdir(path_games):
        if os.path.isfile(categoria): continue
        games[categoria] = {}
        for file in os.listdir(os.path.join(path_games, categoria)):
            if not file.endswith(".py"): continue
            path = os.path.join(path_games, categoria, file)
            name = file[:-3] #Remove .py do nome do arquivo

            spec = importlib.util.spec_from_file_location(file, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            games[categoria][name] = {"path": path, "module": module}

    return games

def load_assets():
    assets = {"sounds": {}, "images": {}}

    path_main = os.path.dirname(__file__)
    path_assets = os.path.join(path_main, "assets")

    path_sounds = os.path.join(path_assets, "sounds")
    path_images = os.path.join(path_assets, "images")

    for file in os.listdir(path_sounds):
        if not (file.endswith(".wav") or file.endswith(".ogg")): continue
        name = file[:-4] #Remove .py do nome do arquivo
        path = os.path.join(path_sounds, file)

        assets["sounds"][name] = {"path": path}

    for file in os.listdir(path_images):
        if not (file.endswith(".png") or file.endswith(".jpeg")): continue
        name = file[:-4] #Aki them um erro, eu resolvo depois.
        path = os.path.join(path_sounds, file)

        assets["images"][name] = {"path": path}

    return assets

#Recebe a chave de um input, como o do teclado, por exemplo.
def get_key(key: str) -> int:
    keycode = pygame.key.key_code(key.lower())
    return keycode

def pull_events():
    global _event_manager
    return _event_manager.pull_events()

def is_key_pressed(key: str) -> bool:
    keycode = get_key(key)
    return keycode in _event_manager.inputs.keys_pressed

def is_key_released(key: str) -> bool:
    keycode = get_key(key)
    return keycode in _event_manager.inputs.keys_released

#Recebe uma classe de Event que pode ser usada para ser enviada com o pygame.event.post()
def get_event(event_id: int) -> pygame.event.Event:
    return pygame.event.Event(event_id)