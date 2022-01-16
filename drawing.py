#Здесь запрогана отрисовка всего окружения
import imp
from msilib.schema import Class
import pygame
from settings import *
from ray_casting import ray_casting, Button
from map import mini_map
from collections import deque
from random import  randrange
import sys
from map import map_now

class Drawing: # класс отрисовки всего
    def __init__(self, sc, sc_map, player, clock):
        self.sc = sc
        
        self.sc_map = sc_map
        self.player = player
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.Font(F'data/font/font.ttf', 144)
        
        self.textures = {1: pygame.image.load(F'data/textures/1.png').convert(), # текстурки для стен карты
                        2: pygame.image.load(F'data/textures/2.png').convert(),
                        3: pygame.image.load(F'data/textures/3-1.png').convert(), # текстурки для стен карты
                        4: pygame.image.load(F'data/textures/3-2.png').convert(),
                        5: pygame.image.load(F'data/textures/4.png').convert(), # текстурки для стен карты
                        6: pygame.image.load(F'data/textures/5.png').convert(),
                        'S1': pygame.image.load(F'data/textures/sky1.png').convert(),
                        'S2': pygame.image.load(F'data/textures/sky2.png').convert(),
                        'S3': pygame.image.load(F'data/textures/sky3.png').convert(),
                        'S4': pygame.image.load(F'data/textures/sky4.png').convert(),
                        'S5': pygame.image.load(F'data/textures/sky5.png').convert(),
                        }
        
        # (переменные)меню, запуск, рисунок меню 
        self.menu_trigger = True
        self.menu_picture = pygame.image.load(F'data/textures/bg.png').convert()
        # настройки оружия 
        self.weapon_base_sprite = pygame.image.load(F'data/weapons/shotgun/base/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(F'data/weapons/shotgun/shot/{i}.png').convert_alpha()
                                            for i in range(17)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (HALF_WIDTH - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 2
        self.shot_animation_count = 0
        self.shot_animation_trigger = True
        self.shot_sound = pygame.mixer.Sound(F'data/sound/shotgun.mp3')
        # параметры выстрела(тоже для 2 сделаем)
        self.sfx = deque([pygame.image.load(F'data/weapons/sfx/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def background(self, angle): # тут рисуется небо и пол
        if map_now[0] == "shop":
            now = "S1"
            now_floor = DARKBLUE
        elif map_now[0] == "arena":
            now = "S2"
            now_floor = SKYBLUE
        elif map_now[0] == "limb":
            now = "S3"
            now_floor = VIOLET
        elif map_now[0] == "labyrinth":
            now = "S4"
            now_floor = PINK
        elif map_now[0] == "cave":
            now = "S5"
            now_floor = DARKGRAY
        else:
            now = "S5"
            now_floor = DARKGRAY
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures[now], (sky_offset, 0))
        self.sc.blit(self.textures[now], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures[now], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, now_floor, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects): 
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def fps(self, clock): #счетчик фпс
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, DARKORANGE)
        self.sc.blit(render, FPS_POS)
        
    def player_weapon(self, shots): #оружие игрока
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_projection = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.weapon_shot_animation[0]
            self.sc.blit(shot_sprite, self.weapon_pos)
            self.shot_animation_count += 1
            if self.shot_animation_count == self.shot_animation_speed:
                self.weapon_shot_animation.rotate(-1)
                self.shot_animation_count = 0
                self.shot_length_count += 1
                self.shot_animation_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_animation_trigger = True
        else:
            self.sc.blit(self.weapon_base_sprite, self.weapon_pos)

    def bullet_sfx(self): #взрыв от попадания
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.sc.blit(sfx, (HALF_WIDTH - sfx_rect.w // 2, HALF_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    

    def menu(self):  # начальное меню
        label_font = pygame.font.Font('data/font/font1.otf', 250)
        label_font_2 = pygame.font.Font('data/font/font1.otf', 150)
        x = 0
        f = False
        startButton = Button(self.sc, "СТАРТ", (350, 325), (500, 100), BLACK, SKYBLUE, 0, 128)
        gratButton = Button(self.sc, "РАЗРАБОТЧИКИ", (350, 450), (500, 100), BLACK, SKYBLUE, 0, 128)
        outButton = Button(self.sc, "ВЫХОД", (350, 575), (500, 100), BLACK, SKYBLUE, 0, 128)
        menuButton = Button(self.sc, "В МЕНЮ", (50, 600), (300, 100), SKYBLUE, BLACK, 0, 128)
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('data/music/menu.mp3')
        pygame.mixer.music.play(10)
        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if f:
                self.sc.fill((0, 0, 0))
                font = pygame.font.Font('data/font/font2.ttf', 30)
                font_2 = pygame.font.Font('data/font/font1.otf', 30)
                label_1 = font.render('Состав команды: 50% Тимошин Вадим, 50% Власюк Демьян', 1, SKYBLUE)
                label_2 = font.render('Создание смысла происходящему: Тимошин Вадим,  Власюк Демьян', 1, SKYBLUE)
                label_3 = font.render('Подготовил текстурки:  Власюк Демьян', 1, SKYBLUE)
                label_4 = font.render('Кодили: Мы', 1, SKYBLUE)
                label_5 = font.render('Написал музыку: Павел Штеменко', 1, SKYBLUE)
                self.sc.blit(label_1, (80, 10))
                self.sc.blit(label_2, (80, 110))
                self.sc.blit(label_3, (80, 210))
                self.sc.blit(label_4, (80, 310))
                self.sc.blit(label_5, (80, 410))
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                menuButton.draw_button()
                if menuButton.get_button().collidepoint(mouse_pos):
                    menuButton.resize((40, 590), (320, 120))
                    if mouse_click[0]:
                        f = False
                else:
                    menuButton.resize((50, 600), (300, 100))
            else:
                self.sc.blit(self.menu_picture, (0, 0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
                x += 1
                pygame.draw.rect(self.sc, BLACK, (110, 28, 1010, 280), 0, 50)
                label = label_font.render('DEMO', 1, SKYBLUE)
                label_2 = label_font_2.render('GAME', 1, SKYBLUE)
                self.sc.blit(label, (370, 10))
                self.sc.blit(label_2, (470, 160))
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                startButton.draw_button()
                gratButton.draw_button()
                outButton.draw_button()
                if startButton.get_button().collidepoint(mouse_pos):
                    startButton.resize((340, 315), (520, 120))
                    if mouse_click[0]:
                        self.menu_trigger = False
                else:
                    startButton.resize((350, 325), (500, 100))
                if gratButton.get_button().collidepoint(mouse_pos):
                    gratButton.resize((340, 440), (520, 120))
                    if mouse_click[0]:
                        f = True
                else:
                    gratButton.resize((350, 450), (500, 100))
                if outButton.get_button().collidepoint(mouse_pos):
                    outButton.resize((340, 565), (520, 120))
                    if mouse_click[0]:
                        pygame.quit()
                        sys.exit()
                else:
                    outButton.resize((350, 575), (500, 100))
            pygame.display.flip()
            self.clock.tick(30)
    def credits(self, time):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        x = 0
        font = pygame.font.Font('data/font/font2.ttf', 50)
        font_2 = pygame.font.Font('data/font/font2.ttf', 12)          
        

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('data/music/menu.mp3')
        pygame.mixer.music.play(10)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                exit()

            self.sc.blit(self.menu_picture, (0, 0), (x % WIDTH, HALF_HEIGHT, WIDTH, HEIGHT))
            x += 1

            pygame.draw.rect(self.sc, BLACK, (110, 50, 1010, 700), 0, 50)

            label1 = font.render('Спасибо за прохождение нашей ', 1, SKYBLUE)
            label2 = font_2.render("суперпупердупермегаультрагиперомегаальфагаммамикробананабстракткрутойкотыклассныеэтовообщектоточитает", 1, SKYBLUE)
            label3 = font.render('игры!', 1, SKYBLUE)
            label4 = font.render(f'Ты прошел игру за {time} ', 1, SKYBLUE)

            self.sc.blit(label1, (225, 50))
            self.sc.blit(label2, (250, 110))
            self.sc.blit(label3, (550, 125))
            self.sc.blit(label4, (400, 300))
            

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            
            
            pygame.display.flip()
            self.clock.tick(30)
        
