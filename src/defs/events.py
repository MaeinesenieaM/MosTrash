import pygame
from typing import Callable

class Timer(pygame.sprite.Sprite):
    def __init__(
        self,
        milliseconds: int,
        clock: pygame.time.Clock,
        start: Callable[..., None] = None,
        perform: Callable[..., None] = None,
        end: Callable[..., None] = None
    ):
        pygame.sprite.Sprite.__init__(self)

        self._milliseconds = milliseconds
        self._clock = clock
        self._perform = perform
        self._end = end

        if start: start()

    def run_perform(self) -> None:
        """Caso o botão tenha uma função guardada, ira chamá-la e retornar seu resultado."""
        if self._perform: self._perform()

    def run_end(self) -> None:
        if self._end: self._end()

    def update(self):
        self._milliseconds -= self._clock.get_time()

        if self._milliseconds <= 0:
            self.run_end()
            self.kill()
            return

        self.run_perform()

class InputHandler:
    """
    Essa classe é responsável por organizar os inputs do teclado e mouse,
    sem ela seria complicado usar o teclado ou mouse.
    """
    def __init__(self):
        self.keys_pressed = []
        self.keys_released = []
        self.mouse_pressed = []
        self.mouse_released = []
        self.mouse_moved = []

    def update(self, events: list[pygame.event.Event]):
        """
        Analisa os eventos dados, atualiza sua memória, e retorna os eventos não usados.
        """
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse_pressed.clear()
        self.mouse_released.clear()
        self.mouse_moved.clear()

        handled_events = []

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self.keys_pressed.append(event.key)
                    handled_events.append(event)
                case pygame.KEYUP:
                    self.keys_released.append(event.key)
                    handled_events.append(event)
                case pygame.MOUSEBUTTONDOWN:
                    info = [event.pos, event.button, event.touch]
                    self.mouse_pressed.append(info)
                    handled_events.append(event)
                case pygame.MOUSEBUTTONUP:
                    info = [event.pos, event.button, event.touch]
                    self.mouse_released.append(info)
                    handled_events.append(event)
                case pygame.MOUSEMOTION:
                    info = [event.pos, event.rel, event.buttons, event.touch]
                    self.mouse_moved.append(info)
                    handled_events.append(event)

        for event in handled_events:
            events.remove(event)

class EventManager:
    """
    Organiza qualquer coisa relacionada a eventos do pygame.
    """
    def __init__(self):
        self.inputs = InputHandler()
        self.timers = pygame.sprite.Group()

    def pull_events(self) -> list:
        """
        Chama os eventos em queue e trata eles, retorna aqueles que não foram usados.
        """
        events = pygame.event.get()

        self.inputs.update(events)
        for timer in self.timers: timer.update()

        return events

    def add_timer(self, timer: Timer):
        timer.add(self.timers)