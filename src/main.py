import mostrash
import pygame

from src.objects import Position

#A partir daqui é o código da demonstração.

#Inicia mostrash
mostrash.init(600, 600)

window = mostrash.get_window()
clock = mostrash.get_clock()
camera = mostrash.get_camera()

button = mostrash.Button(Position(0, 0), 20, lambda: print("what"))
games = mostrash.carregar_games()

running = True
while running:
    mostrash.update_input_controller()
    camera.update()
    window.fill([0, 0, 0])
    window_surface = pygame.display.get_surface()

    mouse_pos = mostrash.to_position(pygame.mouse.get_pos())
    camera.draw(button)

    if button.has_point(mouse_pos): button.run_callback()



    print(f"{mouse_pos.x} : {mouse_pos.y}")

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: running = False

    if mostrash.is_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

    #"categorias" so esta aki como exemplo.


    #for categoria, games in games.items():
    #    for name, _ in games.items():
    #        print(f"{categoria}: {name}")


    pygame.display.flip()
    clock.tick(60)

pygame.quit()