import pygame
import random
import src.mostrash as mostrash

from os import PathLike


#Aki será um minigame de limpeza onde vão ter várias cenas que o jogar precisa limpar antes que o tempo acabe.
class Lixo(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: mostrash.Position,
        dirty_image_path: PathLike,
        clean_image_path: PathLike
    ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.dirty: bool = True
        self.dirty_image = mostrash.Bitmap(self.pos, dirty_image_path)
        self.clean_image = mostrash.Bitmap(self.pos, clean_image_path)

        self.button = mostrash.Button(
            self.pos,
            self.dirty_image.get_biggest_side(),
            lambda: self.set_dirty(False)
        )

    def set_dirty(self, dirty: bool):
        self.dirty = dirty

    def clean(self):
        self.button.run_callback()

    def has_point(self, point: mostrash.Position):
        return self.button.has_point(point)

    def get_image(self):
        match self.dirty:
            case True:
                return self.dirty_image
            case False:
                return self.clean_image

def random_cpoint() -> mostrash.CPoint:
    x = -1.0 + 2 * random.random()
    y = -1.0 + 2 * random.random()
    return mostrash.CPoint(x, y)

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    background = mostrash.Bitmap(mostrash.CPoint(), assets.get_image_path("limpeza_scene"))

    lixos = pygame.sprite.Group()

    Lixo(
        mostrash.Position(60, 60),
        assets.get_image_path("balde_verde_sujo"),
        assets.get_image_path("balde_azul_limpo")
    ).add(lixos)

    Lixo(
        mostrash.Position(-90, 20),
        assets.get_image_path("garrafa_vermelho_sujo"),
        assets.get_image_path("garrafa_azul_limpo")
    ).add(lixos)

    Lixo(
        mostrash.Position(0, 85),
        assets.get_image_path("eorr"),
        assets.get_image_path("flor_azul_limpo")
    ).add(lixos)

    running = True
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False

        if mostrash.has_key_released("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))
        if mostrash.has_mouse_released(1):
            for lixo in lixos:
                if lixo.has_point(mostrash.get_mouse_pos()): lixo.clean()

        window.fill(mostrash.BLACK)
        camera.draw(background)

        for lixo in lixos:
            camera.draw(lixo.get_image())

        pygame.display.flip()
        clock.tick(60)

    return True