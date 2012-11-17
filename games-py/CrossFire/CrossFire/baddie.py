# CrossFire - by David Christian
# This source code is free software, and licensed under the GPL v3
# Please see the LICENSE.TXT file or http://www.gnu.org/licenses/gpl.html for more information
import pygame, os, math, random
from pygame.locals import *

class Baddie(pygame.sprite.Sprite):

   def __init__(self, screen_width, screen_height, sprite_image):
      pygame.sprite.Sprite.__init__(self)
      self.screen_width = screen_width
      self.screen_height = screen_height                                 
      self.image = sprite_image
      self.image.set_colorkey((255,0,255))
      self.rect = self.image.get_rect(topleft = (0, 0))

      self.active = False
      self.vector_x = 0
      self.vector_y = 0

      self.anim_delay = 0
      self.anim_frame = 0
      self.anim_max_frame = 0
      self.movement_type = 0
      self.movement_timer = 0
      
   def update(self):
      if (self.active):
         # Move the drone towards it's destination
         self.rect.move_ip(self.vector_x, self.vector_y)         
   
         # Handle the animation
         self.anim_delay += 1
         if self.anim_delay > 6:
             self.anim_frame += 1
             self.anim_delay = 0
             if self.anim_frame > self.anim_max_frame:
                 self.anim_frame = 0

         # Now do the movmement_type specific stuff
         
         if self.movement_type == 1:            
            self.movement_timer += 1
            # Time to change direction?
            if self.movement_timer > 35:
               self.movement_timer = 0
               # Which direction?
               if self.rect.left < (self.screen_width / 4):
                  self.vector_x = random.randint(1,2)
               elif self.rect.left > (self.screen_width - (self.screen_width / 4)):
                  self.vector_x = random.randint(1,2)
               else:
                  self.vector_x = random.randint(0,1) - random.randint(1, 2)

         if self.movement_type == 2:            
            self.movement_timer += 1
            # Time to change direction?
            if self.movement_timer > 35:
               self.movement_timer = 0
               # Which direction?
               if self.rect.top < (self.screen_height / 4):
                  self.vector_y = random.randint(1, 2)
               elif self.rect.top > (self.screen_width - (self.screen_height / 4)):
                  self.vector_y = random.randint(1,2)
               else:
                  self.vector_y = random.randint(0,1) - random.randint(1, 2)

          # Offscreen?
         if self.vector_x < 0 and self.rect.left < -50:
            self.active = False
            
         if self.vector_x > 0 and self.rect.left > self.screen_width + 50:
            self.active = False

         if self.vector_y < 0 and self.rect.top < -50:
            self.active = False
         
         if self.vector_y > 0 and self.rect.top > self.screen_width + 50:
            self.active = False
         
