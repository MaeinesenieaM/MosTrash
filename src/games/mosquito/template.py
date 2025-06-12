import pygame
import src.mostrash as mostrash

def start(context: mostrash.Context):
    window = context.get_window()
    clock = context.get_clock()
    camera = context.get_camera()
    assets = context.get_assets()

    clown: mostrash.Bitmap = mostrash.Bitmap(mostrash.Position(), assets.get_image_path("clown"))
    mostrash.play_sound(assets.get_sound_path("clown"))

    running = True
    while running:
        for event in mostrash.pull_events():
            match event.type:
                case pygame.QUIT: running = False

        window.fill(mostrash.BLACK)
        if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

        camera.draw(clown)

        pygame.display.flip()
        clock.tick(60)

    return True