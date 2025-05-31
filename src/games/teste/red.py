def start(context: mostrash.Context):
    import pygame
    import src.mostrash as mostrash
    class Coisa:
        def __init__(self):
            self.outra_coisa = "coisa"
    Coisa()
    mostrash.update_input_controller()
    window = context.get_window()
    window.fill([240, 0, 0])