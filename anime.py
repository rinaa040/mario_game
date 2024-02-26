import random
import pygame
import sys
import os

# def create_level(u):
#     filename = f"field{u}.txt"
#     game_map = []
#     map_w = random.randrange(10, 20)
#     land_type = ["#", "."]
#     for i in range(map_w):
#         line = []
#         map_h = random.randrange(6, 20)
#         for j in range(map_h):
#             line += random.choice(land_type)
#         game_map.append(line)
#     game_map[random.randint(0, 10)][random.randint(0, 10)] = "@"
#
#
#
#     with open(filename, 'w') as mapFile:
#         for i in range(len(game_map)):
#             game_map[i] = ''.join(game_map[i])
#             mapFile.write(game_map[i] + '\n')
#
#
# for i in range(4):
#     create_level(i)

lvl = None
for line in sys.stdin:
    lvl = line.rstrip("\n")
if lvl:
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

fps = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move_up(self):
        self.pos_y -= 1
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)
        if self.rect.collidelist(collided_list) != -1:
            self.pos_y += 1
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def move_down(self):
        self.pos_y += 1
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)
        if self.rect.collidelist(collided_list) != -1:
            self.pos_y -= 1
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def move_left(self):
        self.pos_x -= 1
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)
        if self.rect.collidelist(collided_list) != -1:
            self.pos_x += 1
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def move_right(self):
        self.pos_x += 1
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)
        if self.rect.collidelist(collided_list) != -1:
            self.pos_x -= 1
            self.rect = self.image.get_rect().move(
                tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    collided = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                collided.append(Tile('wall', x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                px = x
                py = y
    new_player = Player(px, py)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, collided


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player, level_x, level_y, collided_list = generate_level(load_level(lvl))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon3.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


start_screen()
camera = Camera()
running = True

# generate_level(load_level('field.txt'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            if event.key == pygame.K_DOWN:
                player.move_down()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_LEFT:
                player.move_left()
    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick()
    pygame.display.flip()
pygame.quit()
