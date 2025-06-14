import pygame
import src.mostrash as mostrash
from src.mostrash import CPoint, RPoint, Position
from src.mostrash import IntRef, FloatRef, BoolRef

import random

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    textos = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    sucesso = False
    escolha = False

    temp_numero = random.randint(1, 3)
    dengue_certa = temp_numero == 1

    escolha_texto = mostrash.Label(CPoint(0.0, -0.5), str(escolha), size = 16, color = mostrash.color_from_bool(sucesso))
    escolha_texto.add(textos)
    mostrash.Label(CPoint(0.0, 0.75), "Isso é o numero 1?", size = 48).add(textos)
    mostrash.Label(CPoint(0.0, 0.0), str(temp_numero), size = 32).add(textos)

    mostrash.Button(CPoint(-0.5, -0.5), 32, lambda: False, mostrash.DARK_RED).add(buttons)
    mostrash.Button(CPoint(0.5, -0.5), 32, lambda: True, mostrash.DARK_GREEN).add(buttons)

    running = BoolRef(True)

    mostrash.Button(CPoint(0.0, -0.75), 48, lambda: running.toggle(), mostrash.WHITE).add(buttons)

    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running.set(False)
        window.fill(mostrash.BLACK)

        mouse_pos = mostrash.to_position(pygame.mouse.get_pos())
        mouse_down = pygame.mouse.get_pressed()[0]

        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

        for text in textos:
            camera.draw(text)

        for button in buttons:
            if button.has_point(mouse_pos) and mouse_down:
                resultado = button.run_callback()
                if isinstance(resultado, bool):
                    escolha = resultado
                    escolha_texto.set_text(str(escolha)).set_color(mostrash.color_from_bool(escolha))

            camera.draw(button)

        pygame.display.flip()
        clock.tick(60)

    sucesso = escolha == dengue_certa

    return sucesso