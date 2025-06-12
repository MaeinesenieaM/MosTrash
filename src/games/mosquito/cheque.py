import pygame
import src.mostrash as mostrash
from src.mostrash import CPoint, RPoint, Position

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    textos = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    sucesso = False

    sucesso_texto = mostrash.Label(CPoint(0.0, -0.5), str(sucesso), size = 16, color = mostrash.color_from_bool(sucesso))
    sucesso_texto.add(textos)
    mostrash.Label(CPoint(0.0, 0.0), "socorro", size = 48).add(textos)

    mostrash.Button(CPoint(-0.5, -0.5), 32, lambda: False, mostrash.DARK_RED).add(buttons)
    mostrash.Button(CPoint(0.5, -0.5), 32, lambda: True, mostrash.DARK_GREEN).add(buttons)

    running = True
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False
        window.fill(mostrash.BLACK)

        mouse_pos = mostrash.to_position(pygame.mouse.get_pos())
        mouse_down = pygame.mouse.get_pressed()[0]

        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

        for text in textos:
            camera.draw(text)
        for button in buttons:
            if button.has_point(mouse_pos) and mouse_down:
                sucesso = button.run_callback()
                sucesso_texto.set_text(str(sucesso)).set_color(mostrash.color_from_bool(sucesso))
            camera.draw(button)

        pygame.display.flip()
        clock.tick(60)

    return sucesso