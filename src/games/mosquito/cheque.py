import pygame
import src.mostrash as mostrash
from src.mostrash import CPoint, RPoint, Position
from src.mostrash import IntRef, FloatRef, BoolRef

import random

#Basicamente um Papers Please de mosquito simples, só que nenhum mosquito será perdoado.
def rolar_mosquito(largura: int):
    return random.randint(0, largura - 1)

class Mosquito:
    def __init__(self, real: bool, image: mostrash.Bitmap | None = None):
        self.image: mostrash.Bitmap | None = image
        self.real = real

    def get_image(self):
        return self.image
#Eu sei que as funções abaixo são preguiçosas, mas eu real não tenho tempo.
def mosquito_cheque(mosquito: list, estado: bool):
    return mosquito[1] is estado

def pegar_imagem(mosquito: list, index: int):
    pass
def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    textos = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    sucesso = False

    vida = 3
    tentativa = 0
    mosquito_index = 0

    vida_texto = mostrash.Label(CPoint(0.0, -0.5), str(vida), size = 32)
    vida_texto.add(textos)

    mosquitos: list[Mosquito] = [
        Mosquito(True, mostrash.Bitmap(Position(0.0, 0.0), assets.get_image_path("carinha_feliz"))),
        Mosquito(False, mostrash.Bitmap(Position(0.0, 0.0), assets.get_image_path("carinha_triste")))
    ]

    #escolha_texto = mostrash.Label(CPoint(0.0, -0.5), str(escolha), size = 16, color = mostrash.color_from_bool(sucesso))
    #escolha_texto.add(textos)

    mostrash.Label(CPoint(0.0, 0.75), "Isso é o mosquito dengue?", size = 48).add(textos)

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
        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))
        if mostrash.has_mouse_released(1):
            for button in buttons:
                if button.has_point(mouse_pos):
                    escolha = button.run_callback()

        if escolha is not None:
            if escolha: tentativa += 1
            else:
                vida -= 1
                vida_texto.set_text(str(vida))

            mosquito_index = rolar_mosquito(len(mosquitos))
            escolha = None

        print(vida)

        if vida <= 0:
            sucesso = False
            running = False
            continue

        if tentativa >= 3:
            sucesso = True
            running = False
            continue

        #Apartir daqui está as funções para desenhar na janela.
        window.fill(mostrash.BLACK)

        for text in textos:
            camera.draw(text)
        for button in buttons:
            camera.draw(button)

        camera.draw(mosquitos[mosquito_index].image)

        pygame.display.flip()
        clock.tick(60)

    return sucesso