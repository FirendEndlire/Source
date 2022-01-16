import pygame
from settings import *
from collections import deque
from ray_casting import mapping, Button
from map import map_now
from random import randrange


class Sprites:
    def __init__(self):
        self.sprite_parameters = { # это все характеристи спрайтов, тоже сделаю поддержку своих, если смогу
            'monster': {
                'sprite': pygame.image.load(F'data/sprites/monster/base/0.png').convert_alpha(), 
                'viewing_angles': None,
                'shift': 0.0,
                'scale': (0.5, 1),
                'side': 50,
                'animation': [],
                'death_animation': deque([pygame.image.load(F'data/sprites/monster/death/{i}.png')
                                           .convert_alpha() for i in range(10)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'animation_dist': None,
                'animation_speed': 1,
                'blocked': True,
                'flag': 'npc',
                'obj_action': deque(
                    [pygame.image.load(F'data/sprites/monster/anim/{i}.png').convert_alpha() for i in range(1)]),
                'Dialog': None
            },
            'sprite_level_changer_1': {
                'sprite': pygame.image.load(F'data/sprites/levelchanger/Door.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.1,
                'scale': (0.5, 1),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'level_changer',
                'obj_action': [],
                'Dialog': None
            },
            'sprite_level_changer_3': {
                'sprite': pygame.image.load(F'data/sprites/levelchanger/cassete.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.1,
                'scale': (0.5, 1),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'level_changer',
                'obj_action': [],
                'Dialog': None
            },
            'sprite_level_changer_fake': {
                'sprite': pygame.image.load(F'data/sprites/levelchanger/cassete.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.1,
                'scale': (0.5, 1),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': None,
                'flag': 'decor',
                'obj_action': [],
                'Dialog': None
            },
            'sprite_level_changer_2': {
                'sprite': pygame.image.load(F'data/sprites/levelchanger/Danger.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.1,
                'scale': (0.5, 1),
                'side': 100,
                'animation': deque([pygame.image.load(f'data/sprites/levelchanger/Danger_anim/Danger-export{i + 1}.png').convert_alpha() for i in range(14)]),
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 800,
                'animation_speed': 2,
                'blocked': True,
                'flag': 'level_changer',
                'obj_action': [],
                'Dialog': None
            },
            'sprite_level_changer_4': {
                'sprite': pygame.image.load(F'data/sprites/levelchanger/Dream.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.1,
                'scale': (0.5, 1),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'level_changer',
                'obj_action': [],
                'Dialog': None
            },
            'sprite_level_changer_5': {
                'sprite': pygame.image.load(F'data/sprites/levelchanger/BrokenDream.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.1,
                'scale': (0.5, 1),
                'side': 100,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'level_changer',
                'obj_action': [],
                'Dialog': None
            },
            'seller': {
                'sprite': pygame.image.load('data/sprites/npc/LifeSaver.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': (0.5, 1),
                'side': 30,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': None,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'dialog_npc',
                'obj_action': [],
                'Dialog': seller_dialogue
            },
            'machine': {
                'sprite': pygame.image.load('data/sprites/npc/MachineSeller.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.6,
                'scale': (0.25, 0.5),
                'side': 30,
                'animation': [],
                'death_animation': [],
                'is_dead': 'immortal',
                'dead_shift': None,
                'animation_dist': 0,
                'animation_speed': 0,
                'blocked': True,
                'flag': 'dialog_npc',
                'obj_action': [],
                'Dialog': machine_dialogue
            },
        }

        self.list_of_objects = [ #список ВСЕХ обьектов на карте #TODO сделай чтобы по-нормальному хранить это все в папке с картой
            SpriteObject(self.sprite_parameters['monster'], (19, 2)),
            SpriteObject(self.sprite_parameters['monster'], (18, 3)),
            SpriteObject(self.sprite_parameters['monster'], (17, 4)),
            SpriteObject(self.sprite_parameters['monster'], (16, 5)),
            SpriteObject(self.sprite_parameters['seller'], (27, 9)),
            SpriteObject(self.sprite_parameters['machine'], (5, 2)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_1'], (9, 7)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_2'], (13.5, 7.5)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_3'], (27, 3)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (26, 3)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (26, 3.5)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (25.25, 3.5)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (23.25, 3.5)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (24.25, 3.5)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (27.25, 5.5)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_fake'], (29.25, 1.5)),

            SpriteObject(self.sprite_parameters['sprite_level_changer_4'], (44, 13)),
            SpriteObject(self.sprite_parameters['sprite_level_changer_5'], (55.5, 7.5)),
            
        ]

    @property
    def sprite_shot(self): # выпор того в кого попали оружием
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.count = 0
        self.ray_casting_walls = None
        self.sprites = None
        self.drawing = None
        self.pause = True
        self.Dialog = parameters['Dialog']
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        # ---------------------
        self.death_animation = parameters['death_animation'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # ---------------------
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.flag = parameters['flag']
        self.obj_action = parameters['obj_action'].copy()
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.side = parameters['side']
        self.dead_animation_count = 0
        self.animation_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.door_prev_pos = self.y if self.flag == 'dialog_npc' else self.x
        self.delete = False
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def is_on_fire(self):# проверка под прицелом ли нпс
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self): # позиция нпс
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player, sc, drawing=None, sprites=None,
                      ray_casting_walls=None, recurs=True):# отрисовка обьекта, как я понял

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag != 'dialog_npc':
            self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite),
                                   DOUBLE_HEIGHT if self.flag != 'dialog_npc' else HEIGHT)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            # logic for doors, npc, decor
            if self.flag == 'dialog_npc':
                if recurs:
                    if self.door_open_trigger:
                        self.dialog_teleport(sc, player, drawing, sprites, ray_casting_walls)
                    self.object = self.visible_sprite()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal':
                    sprite_object = self.dead_animation()
                    shift = half_sprite_height * self.dead_shift
                    sprite_height = int(sprite_height / 1.3)

                elif self.npc_action_trigger:
                    sprite_object = self.npc_in_action()
                else:
                    self.object = self.visible_sprite()
                    sprite_object = self.sprite_animation()


            # sprite scale and pos
            sprite_pos = (self.current_ray * SCALE - half_sprite_width, HALF_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def sprite_animation(self):
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object

    def visible_sprite(self):
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object

    def dead_animation(self):
        if len(self.death_animation):
            if self.dead_animation_count < self.animation_speed:
                self.dead_sprite = self.death_animation[0]
                self.dead_animation_count += 1
                
                
            else:
                self.dead_sprite = self.death_animation.popleft()
                self.dead_animation_count = 0
        return self.dead_sprite

    def npc_in_action(self):
        sprite_object = self.obj_action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.obj_action.rotate()
            self.animation_count = 0
        return sprite_object

    def dialog_teleport(self, sc, player, drawing=None, sprites=None, ray_casting_walls=None):
        if not drawing is None:
            self.drawing = drawing
            self.sprites = sprites
            self.ray_casting_walls = ray_casting_walls
        if self.flag == 'dialog_npc':
            if self.count == 0:
                self.say(self.Dialog, sc, player, self.drawing, self.sprites, self.ray_casting_walls)
                
            elif self.count % 2 == 0:
                self.say(final_dialogue, sc, player, self.drawing, self.sprites, self.ray_casting_walls, True)
            self.count += 1

    def say(self, dialog, sc, player, drawing, sprites, ray_casting_walls, rand=False):
        pygame.mouse.set_visible(True)
        i = 1
        if rand:
            dialog = dialog[randrange(0, 10)]
            button = Button(sc, f"{dialog}", (0, int(HEIGHT * 0.65)),
                            (WIDTH, int(HEIGHT * 0.35)), BLUE, WHITE)
        else:
            button = Button(sc, f"{dialog[0]}", (0, int(HEIGHT * 0.65)),
                            (WIDTH, int(HEIGHT * 0.35)), BLUE, WHITE)
        self.pause = False
        button.draw_button()
        pygame.display.flip()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:  # При надатии кнопки...
                    if button.get_button().collidepoint(event.pos):  # Если мышь на кнопке, кнопка нажатаy
                        if rand:
                            run = False
                        else:
                            if i < len(dialog):
                                button.set_text(dialog[i])
                                i += 1
                            else:
                                run = False
            walls, wall_shot = ray_casting_walls(player, drawing.textures)
            drawing.world(walls + [obj.object_locate(player, sc, drawing, sprites, ray_casting_walls, False) for obj in sprites.list_of_objects])
            button.draw_button()
            pygame.display.flip()
        self.door_open_trigger = False
        pygame.mouse.set_visible(False)
        self.pause = True
