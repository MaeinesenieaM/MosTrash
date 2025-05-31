import mostrash
import pygame

from src.objects import Position

#A partir daqui é o código da demonstração.

#Inicia mostrash
context = mostrash.init(600, 600)

window = context.get_window()
clock = context.get_clock()
camera = context.get_camera()

games = mostrash.Games()

#butão de exemplo.
button = mostrash.Button(Position(0, 0), 32, lambda: games.get_game("teste", "green")(context))

running = True
while running:
    mostrash.update_input_controller()
    camera.update()
    window.fill([0, 0, 0])

    mouse_pos = mostrash.to_position(pygame.mouse.get_pos())
    camera.draw(button)

    if button.has_point(mouse_pos): button.run_callback()

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: running = False

    if mostrash.is_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()