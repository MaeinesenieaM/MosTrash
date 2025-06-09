import pygame
import src.mostrash as mostrash

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()

    running = True
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False

        window.fill([240, 240, 0])
        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

        pygame.display.flip()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT: running = False
        clock.tick(60)