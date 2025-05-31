def start(context: mostrash.Context):
    import pygame
    import src.mostrash as mostrash
    class Coisa:
        def __init__(self):
            self.outra_coisa = "coisa"
    Coisa()
    window = context.get_window()
    mostrash.update_input_controller()
    window.fill([0, 240, 0])