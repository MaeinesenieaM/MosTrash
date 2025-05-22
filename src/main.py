from mostrash import *

#A partir daqui é o código da demonstração.
pygame.init()

window = pygame.display.set_mode((600, 600), flags = pygame.RESIZABLE)
clock = pygame.time.Clock()

camera = Camera(window)

running = True
while running:
    camera.update()
    window.fill([0, 0, 0])
    window_surface = pygame.display.get_surface()

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: running = False

    if is_key_pressed("escape"): pygame.event.post(get_event(pygame.QUIT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()