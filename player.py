# тут все про игрока
from unittest import main
from settings import *
import pygame
import math
from map import map_now
from map import collision_walls
class Player:
    def __init__(self, sprites):
        self.x, self.y = player_pos
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.004
        # коллизия игрока
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        # стреляет щас или нет
        self.shot = False

    @property#позиция 
    def pos(self):
        return (self.x, self.y)

    @property
    def collision_list(self):# тут у нас список коллизии со стенками и обьектами
        return collision_walls + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]

    def detect_collision(self, dx, dy):# находим коллизию
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy
# далее управление игроком(часть вырезать)
    #TODO Дэши добавь
    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)
            
        
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shot:
                    self.shot = True
            
            
    def change_level(self):
        
        if map_now[0] == "shop":
            map_now[0] = "arena"
            self.x = 1550
            self.y = 750
            pygame.mixer.music.load("data/music/arena.mp3")
            pygame.mixer.music.play(10)
        elif map_now[0] == "arena":
            map_now[0] = "limb"
            self.x = 2750
            self.y = 850
            pygame.mixer.music.load("data/music/LivesMerchant.mp3")
            pygame.mixer.music.play(10)
        elif map_now[0] == "limb":
            map_now[0] = "labyrinth"
            self.x = 3350
            self.y = 150
            pygame.mixer.music.load("data/music/labyrinth.mp3")
            pygame.mixer.music.play(10)
        elif map_now[0] == "labyrinth":
            map_now[0] = "cave"
            self.x = 4850
            self.y = 750
            pygame.mixer.music.load("data/music/BrokenDream.mp3")
            pygame.mixer.music.play(10)
        elif map_now[0] == "cave":
            map_now[0] = "title"
            self.x = 1250
            self.y = 150
            pygame.mixer.music.load("data/music/arena.mp3")
            pygame.mixer.music.play(10)
       
        print(map_now[0])
    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity

