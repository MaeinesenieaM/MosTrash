import mostrash
import pygame

from src.defs.points import CPoint

#A partir daqui é o código da demonstração.

#Inicia mostrash
context: mostrash.Context = mostrash.init(700, 600)

window = context.get_window()
clock = context.get_clock()
camera = context.get_camera()
assets = context.get_assets()

games = mostrash.Games()

image = mostrash.Bitmap(mostrash.Position(0.0, 0.0), assets.get_image_path("boom"))
contagem = mostrash.Label(mostrash.CPoint(0.0, 0.9), "funciona!", size = 32, color = mostrash.WHITE)

mostrash.play_sound(assets.get_sound_path("explosion"))

count = 0
running = True

#Este grupo guarda os objetos para a interface debug dos jogos.
games_buttons = pygame.sprite.Group()

#Este código abaixo basicamente cria objetos como botões e textos relacionados a quantos games e categorias
#está em "games" e guarda eles em games_button para serem usados depois.
categories_spacing = 2.0 / games.get_category_count()
for category_index, category in enumerate(games.get_categories_names()):
    game_count = games.get_games_count(category)
    if game_count == 0: continue

    pos_y = -1.0 + (categories_spacing / 2) + (categories_spacing * category_index)
    games_spacing = 2.0 / game_count

    mostrash.Label(CPoint(0.0, pos_y + 0.2), category, size = 48, color = mostrash.WHITE).add(games_buttons)
    for game_index, game_name in enumerate(games.get_games_names(category)):
        pos_x = -1.0 + (games_spacing / 2) + (games_spacing * game_index)
        final_pos = CPoint(pos_x, pos_y)
        game_function = lambda c = category, n = game_name: games.get_game(c, n)(context)

        mostrash.Button(final_pos, 32, game_function).add(games_buttons)
        mostrash.Label(final_pos.clone_from_offset(y_offset = -0.1), game_name).add(games_buttons)

sucesso = False

while running:
    for event in mostrash.pull_events():
        match event.type:
            case pygame.QUIT: running = False

    camera.update()

    window.fill(mostrash.BLACK)

    mouse_pos = mostrash.to_position(pygame.mouse.get_pos())
    mouse_down = pygame.mouse.get_pressed()[0]

    count += 1

    contagem.set_text(str(count))

    camera.draw(image) #Desenha a imagem
    camera.draw(contagem) #Desenha o Texto

    for obj in games_buttons.sprites():
        if isinstance(obj, mostrash.Button):
            if obj.has_point(mouse_pos) and mostrash.has_mouse_released(1):
                sucesso = obj.run_callback()
                sucesso_img = None
                if not sucesso: sucesso_img = mostrash.Bitmap(mostrash.Position(0.0, 0.0), assets.get_image_path("carinha_triste"))
                else: sucesso_img = mostrash.Bitmap(mostrash.Position(0.0, 0.0), assets.get_image_path("carinha_feliz"))

                sucesso_img.add(games_buttons)

        camera.draw(obj)

    offset_x, offset_y = camera.get_offset()

    if mostrash.has_key_pressed("escape"): pygame.event.post(mostrash.get_event(pygame.QUIT))

    #camera.pos.y += 0.005
    pygame.display.flip()
    clock.tick(60)

pygame.quit()