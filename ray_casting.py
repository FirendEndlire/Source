# дичь с рэйкастингом, я это даже коментить не буду,
import pygame
from settings import *
from map import world_map, WORLD_WIDTH, WORLD_HEIGHT
#from numba import njit

class Button:
    def __init__(self, screen, text, pos, size, color_circuil, color_text, border=0, border_radius=0):  # Все нужное
        self.screen = screen  # Где рисуем
        self.pos_x, self.pos_y = pos  # Где именно рисуем
        self.width, self.height = size  # Размер
        self.color_circuil = color_circuil  # Цвет кнопки или контура
        self.color_text = color_text  # Цвет кнопки
        self.border = border  # Контур или заливка и размер
        self.font = pygame.font.Font(None, int(self.height * 0.55))  # Нужный размер
        self.t = text
        self.text = self.font.render(self.t, False, self.color_text)  # Поверхность
        self.border_radius = border_radius
        self.button = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)  # Сама кнопка

    def set_text(self, text):  # Можно изминить текст на кнопке
        self.t = text

    def set_border(self, border):  # Можно изминить текст на кнопке
        self.border = border

    def set_circuil(self, circuil):  # Можно изминить текст на кнопке
        self.color_circuil = circuil

    def set_color(self, color):  # Можно изминить текст на кнопке
        self.color_text = color

    def resize(self, pos, size):
        self.pos_x, self.pos_y = pos
        self.width, self.height = size
        self.button = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def draw_button(self):  # Нарисовать кнопку и текст на ней
        self.text = self.font.render(self.t, True, self.color_text)
        pygame.draw.rect(self.screen, self.color_circuil, self.button, self.border, self.border_radius)
        self.screen.blit(self.text,
                         (self.pos_x + (self.width // 2 - self.text.get_width() // 2), self.pos_y + self.height // 5))

    def get_button(self):  # Это для проверки совмещения с мышью
        return self.button

#@njit(fastmath=True, cache=True)
def mapping(a, b):
    return int(a // TILE) * TILE, int(b // TILE) * TILE

#@njit(fastmath=True, cache=True) не включать
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    texture_v, texture_h = 1, 1
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = math.cos(cur_angle)
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = int(PROJ_COEFF / depth)

        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += DELTA_ANGLE
    return casted_walls

def ray_casting_walls(player, textures):
    casted_walls = ray_casting(player.pos, player.angle, world_map)
    wall_shot = casted_walls[CENTER_RAY][0], casted_walls[CENTER_RAY][2]
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > HEIGHT:
            coeff = proj_height / HEIGHT
            texture_height = TEXTURE_HEIGHT / coeff
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                                       HALF_TEXTURE_HEIGHT - texture_height // 2,
                                                       TEXTURE_SCALE, texture_height)
            wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
            wall_pos = (ray * SCALE, 0)
        else:
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

        walls.append((depth, wall_column, wall_pos))
    return walls, wall_shot
