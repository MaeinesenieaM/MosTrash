import pygame.mouse
import pygame

import mostrash
from mostrash import Position, RPoint, CPoint, Square

class Boneco:
    def __init__(self, pos: Position | RPoint | CPoint, size: float):
        if isinstance(pos, CPoint) or isinstance(pos, RPoint):
            pos = pos.to_position()

        self.pos = pos
        self.size = size
        self.speed = pygame.Vector2(0.0, 0.0)
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self.friction = 0.2

    #Atualiza o objeto Dummy de acordo com suas propriedades, como calcular
    #a posição de acordo com sua velocidade.
    def update(self):
        #Atualizamos a posição conforme a velocidade.
        self.speed += self.acceleration
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        #Apartir daqui são os cálculos para desaceleração com forme a fricção do objeto.

        #Aki calculamos a distância dos vetores da velocidade e aceleração,
        # pense como se eles fossem setas e estamos apenas medindo o quão LONGO
        # eles são.
        speed_length = self.speed.length()
        acceleration_length = self.acceleration.length()

        if speed_length > 0.0:
            friction_force = self.speed * -self.friction
            self.speed += friction_force
            if speed_length < self.friction:
                self.speed = pygame.Vector2(0.0, 0.0)

        if acceleration_length > 0.0:
            acceleration_friction = self.acceleration * -(self.friction / 2.0)
            self.acceleration += acceleration_friction
            if acceleration_length < self.friction:
                self.acceleration = pygame.Vector2(0.0, 0.0)

    def get_body(self):
        return Square(self.pos, self.size)

    def draw(self, surface: pygame.Surface, color: pygame.Color):
        self.get_body().draw(surface, color)

#A partir daqui é o código da demonstração.
mostrash.init(600, 600)

window = mostrash.get_window()
clock = mostrash.get_clock()
camera = mostrash.get_camera()

quadrado = Square(CPoint(0.0, 0.0), 0.0)
quadrado_mouse = Square(Position(0, 0), 10)

boneco = Boneco(Position(0.0, 0.0), 20.0)

running = True
while running:
    boneco.update()
    camera.update()
    window.fill([0, 0, 0])
    window_surface = pygame.display.get_surface()

    offset_x, offset_y = camera.get_offset()
    #Checa por eventos.
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: running = False

    mostrash.update_input_controller()
    get_key = lambda name: pygame.key.key_code(name)
    get_event = lambda key_id: pygame.event.Event(key_id)

    if mostrash.is_key_pressed("escape"): pygame.event.post(get_event(pygame.QUIT))

    velocidade = 0.05

    if mostrash.is_key_pressed("w") | mostrash.is_key_pressed("up"): boneco.acceleration.y += boneco.friction + 0.05
    if mostrash.is_key_pressed("s") | mostrash.is_key_pressed("down"): boneco.acceleration.y -= boneco.friction + 0.05
    if mostrash.is_key_pressed("a") | mostrash.is_key_pressed("left"): boneco.acceleration.x -= boneco.friction + 0.05
    if mostrash.is_key_pressed("d") | mostrash.is_key_pressed("right"): boneco.acceleration.x += boneco.friction + 0.05

    mouse_cart_pos = mostrash.to_position(pygame.mouse.get_pos())

    mouse_x_abs = (mouse_cart_pos.x * mouse_cart_pos.x) ** 0.5
    mouse_y_abs = (mouse_cart_pos.y * mouse_cart_pos.y) ** 0.5

    distance_color = 127.0 * (mouse_y_abs + mouse_x_abs)

    window.fill([distance_color, distance_color, distance_color])

    quadrado.size = quadrado.size + 0.2

    camera.draw_rect(quadrado.create_rect(from_corner = False), pygame.Color(20, 20, 20))
    camera.draw_rect(boneco.get_body().create_rect(), pygame.Color(85, 174, 58))
    quadrado_mouse.set_pos(pygame.mouse.get_pos())
    quadrado_mouse.draw(window, pygame.Color(198, 20, 20))
    #camera.draw_rect(pygame.Color(198, 20, 20), quadrado_mouse.create_rect())

    camera.pos.y += 0.2
    camera.pos.x += 0.1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()