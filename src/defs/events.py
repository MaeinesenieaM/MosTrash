import pygame

class InputHandler:
    """
    Essa classe é responsável por organizar os inputs do teclado,
    sem ela seria complicado usar o teclado.
    """
    def __init__(self):
        self.keys_pressed = []
        self.keys_released = []

    def update(self, events: list[pygame.event.Event]):
        """
        Analisa os eventos dados, atualiza sua memória, e retorna os eventos não usados.
        """
        self.keys_pressed.clear()
        self.keys_released.clear()

        handled_events = []

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self.keys_pressed.append(event.key)
                    handled_events.append(event)
                case pygame.KEYUP:
                    self.keys_released.append(event.key)
                    handled_events.append(event)

        for event in handled_events:
            events.remove(event)

class EventManager:
    """
    Organiza qualquer coisa relacionada a eventos do pygame.
    """
    def __init__(self):
        self.inputs = InputHandler()

    def pull_events(self) -> list:
        """
        Chama os eventos em queue e trata eles, retorna aqueles que não foram usados.
        """
        events = pygame.event.get()

        self.inputs.update(events)

        return events
