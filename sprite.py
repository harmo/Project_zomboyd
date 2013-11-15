#!/usr/bin/env python
import pygame


class BaseSprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()

        self.image_dict = {}

        #animation property
        self.max_frame = 2
        self.frame = 1
        self.stand_frame = 1
        self.current_frame = self.stand_frame
        self.animation_speed = 1
        self.animation_delay = 5
        self.temp = self.animation_speed
        self.direction = "down"
        self.is_walking = False

        #movement property
        self.unwalkable_entity_list = []
        self.unwalkable_layer = None
        self.is_collided = False
        self.speed = 5
        self.movement_x = self.speed  # might be change by camera module
        self.movement_y = self.speed  # might be change by camera module
        self.boundary = None

        #game property
        self.world = None         # can access to the world
        self.collidedObject = []  # collect of all collide object
        self.category = None      # the category of the sprite. hero, npc, ect...

    def load_sprite_sheet(self, spritesheet, charDIM=(32, 32), sheetStartPos = (0, 0), sheetDIM=(96, 128), alpha=False, directionList=["down", "left", "right", "up"]):
        tempSheet = pygame.image.load(spritesheet).convert()
        # Load only the start of animation
        temp_rect = pygame.Rect(sheetStartPos, (sheetDIM))
        temp_sheet = tempSheet.subsurface(temp_rect)
        temp_row = sheetDIM[1]/charDIM[1]
        temp_collumn = sheetDIM[0]/charDIM[0]

        for row in range(temp_row):
            temp_list = []
            for collumn in range(temp_collumn):
                temp_rect = pygame.Rect((charDIM[0]*collumn, charDIM[1]*row), (charDIM))
                temp_image = temp_sheet.subsurface(temp_rect)
                if alpha:
                    temp_image = temp_image.convert_alpha()
                else:
                    trans_color = temp_image.get_at((0, 0))
                    temp_image.set_colorkey(trans_color)
                temp_list.append(temp_image)

            self.image_dict[directionList[row]] = temp_list

        self.image = self.image_dict[self.direction][self.stand_frame]

        # TODO function: used in __init__ and here
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 240
        self.rect.inflate_ip(-5, 0)

    def speed_is(self, speed):
        self.speed = speed
        self.movement_x = speed
        self.movement_y = speed

    def walking_boundary_is(self, dimension_x, dimension_y):
        # define how big the sprite can walk. Use this to set world map size.
        self.boundary = (dimension_x, dimension_y)

    def set_pos(self, x, y):
        # Center position of the sprite.
        self.rect.center = (x, y)

    def move(self, direction):
        self.is_walking = True
        self.direction = direction
        self._do_animation()

        if not self.is_collided:
            if self.direction == "up":
                self.rect.centery -= self.movement_y
            elif self.direction == "down":
                self.rect.centery += self.movement_y
            if self.direction == "left":
                self.rect.centerx -= self.movement_x
            elif self.direction == "right":
                self.rect.centerx += self.movement_x
        else:
            self.is_collided = False

    def _do_animation(self):
        self.temp += self.animation_speed
        if self.temp >= self.animation_delay:
            self.temp = self.animation_speed
            self.image = self.image_dict[self.direction][self.current_frame]

            self.current_frame += self.frame
            if self.current_frame < 0:
                self.frame *= -1
                self.current_frame += 1
            elif self.current_frame > self.max_frame:
                self.frame *= -1
                self.current_frame += self.frame

    def _check_collision(self):
        if self.world:
            self.collidedEntitiesIndex = self.rect.collidelistall(self.world.entities)

            #listOfCollideEntites will have at least one entity which this entity
            #don't want to copy the world.entities list as above
            if len(self.collidedEntitiesIndex) > 1:
                if self in self.collidedEntitiesIndex:
                    print("I am collide with my self")
                #this entity is still collide with other entities
                self.is_collided = True
                if self.direction == "up":
                    self.rect.centery += self.movement_y
                elif self.direction == "down":
                    self.rect.centery -= self.movement_y
                if self.direction == "left":
                    self.rect.centerx += self.movement_x
                elif self.direction == "right":
                    self.rect.centerx -= self.movement_x

            #check collision of teritory
            listOfCollideEntities = self.rect.collidelistall(self.world.map.unwalkable)
            if listOfCollideEntities:
                self.is_collided = True
                if self.direction == "up":
                    self.rect.centery += self.movement_y
                elif self.direction == "down":
                    self.rect.centery -= self.movement_y
                if self.direction == "left":
                    self.rect.centerx += self.movement_x
                elif self.direction == "right":
                    self.rect.centerx -= self.movement_x

        if self.boundary is not None:   # boundary is not None
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > self.boundary[0]:
                self.rect.right = self.boundary[0]
            if self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > self.boundary[1]:
                self.rect.bottom = self.boundary[1]

    def _update_animation(self):
        if not self.is_walking:
            self.image = self.image_dict[self.direction][self.stand_frame]
        else:
            self.is_walking = False

    def check_event(self):
        pass

    def other_update(self):
        pass

    def update(self):
        self.check_event()
        self.other_update()
        self._check_collision()
        self._update_animation()


class Hero(BaseSprite):

    def __init__(self):
        BaseSprite.__init__(self)
        self.actionCollideRect = pygame.Rect(self.image.get_rect().inflate(20, 20))
        self.category = "player"

    def update(self):
        BaseSprite.update(self)
        self.actionCollideRect.center = self.rect.center

    def check_event(self):
        keys_pressed_is = pygame.key.get_pressed()
        if keys_pressed_is[pygame.K_RIGHT]:
            self.move("right")
        elif keys_pressed_is[pygame.K_LEFT]:
            self.move("left")
        if keys_pressed_is[pygame.K_UP]:
            self.move("up")
        elif keys_pressed_is[pygame.K_DOWN]:
            self.move("down")

        if keys_pressed_is[pygame.K_z]:
            collideEntityIndex = self.actionCollideRect.collidelistall(self.world.entities)
            if len(collideEntityIndex) > 1:
                for index in collideEntityIndex:
                    if not index == self.world.entities.index(self):
                        self.world.entities[index].action()
                        break
