import mostrash
import pygame

#A partir daqui é o código da demonstração.

#Inicia mostrash
context: mostrash.Context = mostrash.init(600, 600)

window = context.get_window()
clock = context.get_clock()
camera = context.get_camera()

games = mostrash.Games()
assets = mostrash.Assets()
print(assets.get_sound_path("CLOWN"))

#butão de exemplo.
buttonR = mostrash.Button(
    mostrash.CPoint(-0.5, 0),
    32,
    lambda: games.get_game("teste", "red")(context)
)

buttonG = mostrash.Button(
    mostrash.CPoint(0, 0),
    32,
    lambda: games.get_game("teste", "green")(context)
)

buttonB = mostrash.Button(
    mostrash.CPoint(0.5, 0),
    32,
    lambda: games.get_game("teste", "blue")(context)
)

running = True
while running:
    for event in mostrash.pull_events():
        match event.type:
            case pygame.QUIT: running = False

    camera.update()
    window.fill([12, 12, 12])

    mouse_pos = mostrash.to_position(pygame.mouse.get_pos())
    mouse_down = pygame.mouse.get_pressed()[0]

    camera.draw(buttonR, pygame.Color(125, 0, 0))
    camera.draw(buttonG, pygame.Color(0, 125, 0))
    camera.draw(buttonB, pygame.Color(0, 0, 125))

    if buttonR.has_point(mouse_pos) and pygame.mouse.get_pressed()[0]: buttonR.run_callback()
    if buttonG.has_point(mouse_pos) and pygame.mouse.get_pressed()[0]: buttonG.run_callback()
    if buttonB.has_point(mouse_pos) and pygame.mouse.get_pressed()[0]: buttonB.run_callback()

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.

    if mostrash.is_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()