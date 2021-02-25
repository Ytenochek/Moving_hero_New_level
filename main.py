import pygame
import sys
import os

FPS = 60
SIZE = WIDTH, HEIGHT = 400, 400


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(colorkey)
    return image


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, x, y):
        self.pos_x -= x
        self.pos_y -= y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * self.pos_x + 15
        self.rect.y = tile_height * self.pos_y + 5

    def set_level(self, level):
        self.level = level

    def move(self, x, y, level):
        if level[self.pos_y + y][self.pos_x + x] == "#":
            return False, x, y
        return True, x, y

    def get_pos(self):
        return self.pos_x, self.pos_y


def start_screen():
    intro_text = ["Перемещение героя", "",
                  "на торе"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 20)
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
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    new_player.set_level(level)
    return new_player, x, y, level


def regenerate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
    return x, y, level


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    running = True
    start_screen()
    player, level_x, level_y, level = generate_level(load_level('map.txt'))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                res = False
                if event.key == pygame.K_UP:
                    res, *p = player.move(0, -1, level)
                elif event.key == pygame.K_DOWN:
                    res, *p = player.move(0, 1, level)
                elif event.key == pygame.K_LEFT:
                    res, *p = player.move(-1, 0, level)
                elif event.key == pygame.K_RIGHT:
                    res, *p = player.move(1, 0, level)
                if res:
                    if p[1] > 0:
                        level = level[1:] + [level[0]]
                    elif p[1] < 0:
                        level = [level[-1]] + level[0: -1]
                    if p[0] > 0:
                        for i in range(len(level)):
                            level[i] = level[i][1:] + level[i][0]
                    elif p[0] < 0:
                        for i in range(len(level)):
                            level[i] = level[i][-1] + level[i][:-1]
                    tiles_group.empty()
                    level_x, level_y, level = regenerate_level(level)
                    for tile in tiles_group:
                        tile.move(*p)

        screen.fill('black')

        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
    terminate()
