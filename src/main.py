import mostrash
import pygame

#A partir daqui é o código da demonstração.

#Inicia mostrash
mostrash.init(600, 600)

window = mostrash.get_window()
clock = mostrash.get_clock()
camera = mostrash.get_camera()

running = True
while running:
    mostrash.update_input_controller()
    camera.update()
    window.fill([0, 0, 0])
    window_surface = pygame.display.get_surface()

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: running = False

    if mostrash.is_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

    #"categorias" so esta aki como exemplo.
    games = mostrash.carregar_games()

    games["teste"]["blue"]["module"].start(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()