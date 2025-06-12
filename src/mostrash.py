import importlib.util
import os

from src.defs.objects import *
from src.defs.points import *
from src.defs.events import *
from src.defs.colors import *
from src.assets import *

from typing import Callable

_event_manager = EventManager()

class Context:
    """
    A Classe Context é a classe mais importante de mostrash, ela carrega todos os dados
    necessários que todos os modulos precisam para funcionar.
    """
    def __init__(self, width: int, height: int):
        if not pygame.get_init(): pygame.init()
        self._window = pygame.display.set_mode((width, height), flags = pygame.RESIZABLE)
        self._clock = pygame.time.Clock()
        self._camera = Camera(self._window)
        self._assets = Assets()

    def get_window(self):
        return self._window

    def get_clock(self):
        return self._clock

    def get_camera(self):
        return self._camera

    def get_assets(self):
        return self._assets

class Camera:
    """
    A Camera funciona como os olhos do motor grafico, é fortemente recomendado
    usar ela para desenhar objetos, já que é por ela que suas coordenadas são tratadas.
    Porem não é o obrigatório o uso dela se for usar outros metodos de desenhar
    """
    def __init__(self, display: pygame.surface.Surface):
        self.width = float(display.get_width())
        self.height = float(display.get_height())
        self._display = display
        self.pos = Position(0.0, 0.0)

    def update(self):
        """Atualiza o tamanho da camera conforme a tela."""
        self.width = float(self._display.get_width())
        self.height = float(self._display.get_height())

    def get_offset(self) -> tuple[float, float]:
        return self.pos.x, self.pos.y

    def get_raster_offset(self) -> tuple[float, float]:
        return self.pos.to_raster_raw()

    def apply_offset(self, pos: Position) -> tuple[float, float]:
        offset_x, offset_y = self.get_offset()
        pos_x, pos_y = pos.get_tuple()
        return Position(pos_x + offset_x, pos_y + offset_y).to_raster_raw()

    def draw_rect(self, rect: pygame.Rect, color: pygame.Color):
        offset_x, offset_y = self.get_raster_offset()
        rect.move_ip(offset_x, offset_y)
        pygame.draw.rect(self._display, color, rect)

    def draw(self, obj: Entity):
        match obj:
            case Bitmap(image=img, pos=pos) | Label(image=img, pos=pos):
                #Esta linha calcula o ponto de origem para renderizar a imagem centralizada.
                center_pos = [a - (b / 2) for a, b in zip(self.apply_offset(pos), img.get_size())]
                self._display.blit(img, center_pos)
                return

        bodies = obj.rects()
        for body in bodies:
            self.draw_rect(body[0], body[1])

class Games:
    """
    Guardas os modulos em games de forma que possibilita a chamada de sua função principal.
    NÃO RECOMENDADO O USO DENTRO DOS MINI-GAMES!
    """
    def __init__(self):
        self._games = load_games()

    def get_category(self, category: str)-> dict | None:
        if not category in self._games: return None
        return self._games[category]

    def get_categories_names(self) -> list[str]:
        return list(self._games.keys())

    def get_game(self, category: str, game: str) -> Callable[[Context], bool] | None:
        """Caso encontre o jogo em games, retorna sua função start(),
        caso contrario retornara None."""
        if not category in self._games: return None
        elif not game in self._games[category]: return None
        return self._games[category][game]["module"].start

    def get_games_names(self, category: str | None = None) -> list[str] | None:
        match category:
            case None:
                names: list[str] = []
                for name in self.get_categories_names():
                    names.extend(self.get_category(name).keys())
                return names
            case _:
                listed_category = self.get_category(category)
                match listed_category:
                    case None:
                        print(f"ERROR! Categoria: [{category}] inexistente!")
                        return None
                    case _:
                        return list(listed_category.keys())

    def get_category_count(self) -> int:
        return len(self._games)

    def get_games_count(self, category: str | None = None) -> int:
        match category:
            case None:
                return sum(len(category) for category in self._games.values())
            case _:
                listed_category = self.get_category(category)
                match listed_category:
                    case None:
                        print(f"ERROR! Categoria: [{category}] inexistente!")
                        return 0
                    case _:
                        return len(listed_category)


class World:
    """ESSA CLASSE ESTÁ INCOMPLETA E INUTILIZÁVEL NÃO USE ELA!"""
    def __init__(self):
        self.entities = {}

    def insert_object(self, obj):
        obj_name = obj.__class__.__name__
        self.entities.setdefault(obj_name, []).append(obj)

def init(width: int, height: int) -> Context:
    """Inicia o motor do jogo e retorna seu Contexto."""
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

def get_key(key: str) -> int:
    keycode = pygame.key.key_code(key.lower())
    return keycode

def pull_events():
    global _event_manager
    return _event_manager.pull_events()

def has_key_pressed(key: str) -> bool:
    """Verifica se uma tecla foi pressionada"""
    keycode = get_key(key)
    return keycode in _event_manager.inputs.keys_pressed

def has_key_released(key: str) -> bool:
    """Verifica se uma tecla foi solta"""
    keycode = get_key(key)
    return keycode in _event_manager.inputs.keys_released

def get_event(event_id: int) -> pygame.event.Event:
    """Recebe uma classe de Event que pode ser usada para ser enviada com o pygame.event.post()"""
    return pygame.event.Event(event_id)

def play_sound(sound_path: os.PathLike):
    #Eu tenho certeza que isso calça um problema de memória, mas eu não tenho paciência para elaborar
    #algo mais inteligente.
    pygame.mixer.Sound(sound_path).play()

def color_from_bool(state: bool) -> pygame.Color:
    if state: return pygame.Color(DARK_GREEN)
    else: return pygame.Color(DARK_RED)