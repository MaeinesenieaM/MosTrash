from mostrash import *
import os
import importlib.util

def carregar_games():
    games = {}

    path_main = os.path.dirname(__file__)
    path_games = os.path.join(path_main, "games")

    #Carrega os scripts de cada minigame.
    for categoria in os.listdir(path_games):
        if os.path.isfile(categoria): continue
        games[categoria] = {}
        for file in os.listdir(os.path.join(path_games, categoria)):
            if not file.endswith(".py"): continue
            path = os.path.join(path_games, categoria, file)
            name = file[:-3] #Remove .py do nome do arquivo

            spec = importlib.util.spec_from_file_location(file, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            games[categoria][name] = {"path": path, "module": module}

    return games

#A partir daqui é o código da demonstração.
pygame.init()

window = pygame.display.set_mode((600, 600), flags = pygame.RESIZABLE)
clock = pygame.time.Clock()

camera = Camera(window)

running = True
while running:
    update_input_controller()
    camera.update()
    window.fill([0, 0, 0])
    window_surface = pygame.display.get_surface()

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: running = False

    if is_key_pressed("escape"): pygame.event.post(get_event(pygame.QUIT))

    #"categorias" so esta aki como exemplo.
    games = carregar_games()

    games["yes"]["socorro"]["module"].start(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()