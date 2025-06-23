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
            self.dirty_image.get_smallest_side(),
            lambda: self.set_dirty(False)
        )

    def set_dirty(self, dirty: bool):
        self.dirty = dirty

    def is_dirty(self) -> bool:
        return self.dirty

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

def set_trash(trash_group: pygame.sprite.Group, assets: mostrash.Assets):
    Lixo(
        mostrash.Position(-120, 85),
        assets.get_image_path("flor_vermelho_sujo"),
        assets.get_image_path("flor_vermelho_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(0, 80),
        assets.get_image_path("flor_azul_sujo"),
        assets.get_image_path("flor_azul_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(124, 83),
        assets.get_image_path("flor_amarelo_sujo"),
        assets.get_image_path("flor_amarelo_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(-260, -190),
        assets.get_image_path("balde_roxo_sujo"),
        assets.get_image_path("balde_roxo_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(-172, -195),
        assets.get_image_path("balde_azul_sujo"),
        assets.get_image_path("balde_azul_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(-83, -187),
        assets.get_image_path("balde_verde_sujo"),
        assets.get_image_path("balde_verde_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(90, -200),
        assets.get_image_path("garrafa_vermelho_sujo"),
        assets.get_image_path("garrafa_vermelho_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(175, -210),
        assets.get_image_path("garrafa_verde_sujo"),
        assets.get_image_path("garrafa_verde_limpo")
    ).add(trash_group)
    Lixo(
        mostrash.Position(255, -205),
        assets.get_image_path("garrafa_azul_sujo"),
        assets.get_image_path("garrafa_azul_limpo")
    ).add(trash_group)


def start(context: mostrash.Context):
    #Extração de informação do contexto
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    #Carregando a imagem de fundo.
    background = mostrash.Bitmap(mostrash.CPoint(), assets.get_image_path("limpeza_scene"))

    #Definição de grupos
    lixos = pygame.sprite.Group()
    miscs = pygame.sprite.Group()
    set_trash(lixos, assets)

    objetivo = mostrash.Label(
        mostrash.CPoint(0.0, 0.85),
        f"?/{len(lixos)}",
        size = 32,
        color = mostrash.YELLOW
    )

    running = mostrash.BoolRef(True)
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False

        if mostrash.has_key_released("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))
        if mostrash.has_mouse_released(1):
            for lixo in lixos:
                if lixo.has_point(mostrash.get_mouse_pos()): lixo.clean()

        clean_quantity = sum(1 for lixo in lixos if lixo.is_dirty())
        objetivo.set_text(f"{len(lixos) - clean_quantity}/{len(lixos)}")

        #Se todos os lixos do jogo foram limpos.
        if clean_quantity == 0:
            sucesso = mostrash.Bitmap(mostrash.CPoint(), assets.get_image_path("sucesso_verdade"))
            sucesso.add(miscs)

            def end_game():
                sucesso.kill()
                running.toggle()

            #Esse timer está aki para dar um delay no fim do jogo, assim que ele acabar, o jogo termina.
            mostrash.create_timer(
                1500,
                clock,
                end = end_game
            )

        #Logica para desenhar na tela.
        window.fill(mostrash.BLACK)
        camera.draw(background)

        for lixo in lixos:
            camera.draw(lixo.get_image())
        for misc in miscs:
            camera.draw(misc)

        camera.draw(objetivo)

        pygame.display.flip()
        clock.tick(60)

    return True