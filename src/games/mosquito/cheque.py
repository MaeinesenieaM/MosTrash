import pygame
import src.mostrash as mostrash

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    textos = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    mostrash.Label(mostrash.CPoint(0.0, 0.0), "socorro", size = 48).add(textos)

    running = True
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False

        window.fill(mostrash.BLACK)
        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

        for obj in textos:
            camera.draw(obj)
        for obj in buttons:
            camera.draw(obj)

        pygame.display.flip()
        clock.tick(60)

    return True