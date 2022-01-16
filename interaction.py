# Здесь у нас записаны действия, как игрока, так и обьектов
from os import kill
from settings import *
from map import world_map, map_now
from ray_casting import mapping
import math
import pygame
import player


#from numba import njit
#@njit(fastmath=True, cache=True)

def ray_casting_npc_player(npc_x, npc_y, world_map, player_pos):# зрение нпс
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    # verticals
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        x += dx * TILE

    # horizontals
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        y += dy * TILE
    return True


class Interaction: #класс действий
            
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.pain_sound = pygame.mixer.Sound(F'data/sound/dead.mp3')
        

    
            
    def interaction_objects(self, plyr): #засчет выстрела
        
        if self.player.shot and self.drawing.shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_casting_npc_player(obj.x, obj.y,
                                                  world_map, self.player.pos):
                            if obj.flag == 'npc':
                                self.pain_sound.play()
                                
                                
                            
                            obj.is_dead = True
                            
                            obj.blocked = None
                            self.drawing.shot_animation_trigger = False
                    if obj.flag == 'dialog_npc' and obj.distance_to_sprite < TILE:
                        obj.door_open_trigger = True
                    if obj.flag == "level_changer" and obj.distance_to_sprite < TILE * 2:
                        player.Player.change_level(plyr)
                        
                    break

    def npc_action(self): #ии нпс(действие если видит игрока)
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_casting_npc_player(obj.x, obj.y,
                                          world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj): #движение нпс
        if abs(obj.distance_to_sprite) > TILE and map_now[0] == "arena":
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def clear_world(self):#очистка инфы о нпс если их убили?
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]

    
    def play_music(self): #играть музычку
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        
        
        pygame.mixer.music.load("data/music/abstract.mp3")
        pygame.mixer.music.play(10)
        

       
        
            
        
