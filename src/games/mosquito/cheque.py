from os import PathLike

import pygame
import src.mostrash as mostrash
from src.defs.objects import Bitmap
from src.mostrash import CPoint, RPoint, Position
from src.mostrash import IntRef, FloatRef, BoolRef

import random

#Basicamente um Papers Please de mosquito simples, só que nenhum mosquito será perdoado.

class Mosquito:
    def __init__(self, real: bool, image: mostrash.Bitmap | None = None):
        self.image: mostrash.Bitmap | None = image
        self.real = real

    def get_image(self):
        return self.image

#Eu sei que as funções abaixo são preguiçosas, mas eu real não tenho tempo.
def rolar_mosquito(largura: int):
    return random.randint(0, largura - 1)

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    #background = mostrash.Bitmap(CPoint(), assets.get_image_path("background"))

    textos = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    sucesso_img = pygame.sprite.Group()
    miscs = pygame.sprite.Group()

    sucesso = False

    vida = mostrash.BitmapChain(
        CPoint(-0.8, 0.8),
        CPoint(0.15, 0),
        5,
        assets.get_image_path("heart")
    )
    tentativa = 0
    tentativa_final = 5
    mosquito_index = 0

    objetivo = mostrash.Label(
        mostrash.CPoint(0.0, 0.85),
        f"{tentativa}/{tentativa_final}",
        size = 32,
        color = mostrash.YELLOW
    )
    objetivo.add(miscs)

    mosquitos: list[Mosquito] = [
        Mosquito(False, mostrash.Bitmap(Position(0.0, 0.0), assets.get_image_path("carinha_feliz"))),
        Mosquito(False, mostrash.Bitmap(Position(0.0, 0.0), assets.get_image_path("carinha_triste"))),
        Mosquito(False, mostrash.Bitmap(Position(0.0, 0.0), assets.get_image_path("sol"))),
        Mosquito(True, mostrash.Bitmap(Position(0.0, 0.0), assets.get_image_path("dengue")))

    ]

    #escolha_texto = mostrash.Label(CPoint(0.0, -0.5), str(escolha), size = 16, color = mostrash.color_from_bool(sucesso))
    #escolha_texto.add(textos)

    mostrash.Label(CPoint(0.0, -0.25), "Isso é o mosquito dengue?", size = 32).add(textos)

    mostrash.Button(
        CPoint(-0.5, -0.5),
        32,
        lambda: mosquitos[mosquito_index].real == False,
        mostrash.DARK_RED
    ).add(buttons)
    mostrash.Button(
        CPoint(0.5, -0.5),
        32,
        lambda: mosquitos[mosquito_index].real == True,
        mostrash.DARK_GREEN
    ).add(buttons)

    running = BoolRef(True)

    mostrash.Button(CPoint(0.0, -0.75), 48, lambda: running.toggle(), mostrash.WHITE).add(buttons)

    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running.set(False)

        mouse_pos = mostrash.get_mouse_pos()

        escolha: bool | None = None

        #Checka pelos Inputs do usuário.
        if mostrash.has_key_released("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))
        if mostrash.has_mouse_released(1):
            for button in buttons:
                if button.has_point(mouse_pos):
                    escolha = button.run_callback()

        if escolha is not None:
            if escolha: #Caso tenha feito a decisão certa
                tentativa += 1
                correto = Bitmap(CPoint(0.0, 0.0), assets.get_image_path("sucesso_verdade"))
                correto.add(sucesso_img)
                mostrash.create_timer(
                    500,
                    clock,
                    end = lambda: sucesso_img.empty()
                )

            else:
                vida -= 1
                tentativa = max(0, tentativa - 1) #Para não virar negativo.
                errado = Bitmap(CPoint(0.0, 0.0), assets.get_image_path("sucesso_falso"))
                errado.add(sucesso_img)
                mostrash.create_timer(
                    500,
                    clock,
                    end = lambda: sucesso_img.empty()
                )


            mosquito_index = rolar_mosquito(len(mosquitos))
            escolha = None

        objetivo.set_text(f"{tentativa}/{tentativa_final}")

        if vida <= 0:
            sucesso = False
            running = False
            continue

        if tentativa >= tentativa_final:
            sucesso = True
            running = False
            continue

        #Apartir daqui está as funções para desenhar na janela.
        window.fill(mostrash.BLACK)

        #camera.draw(background)
        camera.draw(mosquitos[mosquito_index].image)

        for sprite in vida.get_sprites():
            camera.draw(sprite)
        for text in textos:
            camera.draw(text)
        for button in buttons:
            camera.draw(button)
        for sucesso in sucesso_img:
            camera.draw(sucesso)
        for misc in miscs:
            camera.draw(misc)



        pygame.display.flip()
        clock.tick(60)

    return sucesso