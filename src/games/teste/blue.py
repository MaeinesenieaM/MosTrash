import pygame
import src.mostrash as mostrash

class Coisa:
    def __init__(self):
        self.outra_coisa = "coisa"
def start(context: mostrash.Context):

    Coisa()
    mostrash.update_input_controller()

    window = context.get_window()
    clock = context.get_clock()

    while not mostrash.is_key_pressed("escape"):
        window.fill([0, 0, 240])
        pygame.display.flip()
        mostrash.update_input_controller()
        clock.tick(60)