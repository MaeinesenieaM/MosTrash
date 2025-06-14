import pygame
import src.mostrash as mostrash

#Aki será um minigame de limpeza onde vão ter várias cenas que o jogar precisa limpar antes que o tempo acabe.

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    running = True
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False

        window.fill(mostrash.BLACK)
        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

        pygame.display.flip()
        clock.tick(60)

    return True