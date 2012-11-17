# CrossFire - by David Christian
# This source code is free software, and licensed under the GPL v3
# Please see the LICENSE.TXT file or http://www.gnu.org/licenses/gpl.html for more information
import pygame, os
from pygame.locals import *

class Projectile(pygame.sprite.Sprite):   
   def __init__(self, screen_width, screen_height, sprite_image):
      pygame.sprite.Sprite.__init__(self)
      self.screen_width = screen_width
      self.screen_height = screen_height
      self.vector_x = 0
      self.vector_y = -5
      self.active = False                                
      self.image = sprite_image
      self.image.set_colorkey((255,0,255))
      self.rect = self.image.get_rect(topleft = (0, 0))
   
   def update(self):
      # Check for key states
      keystate = pygame.key.get_pressed()
      
      if (self.active):
         self.rect.move_ip(self.vector_x, self.vector_y)
         
      if (self.rect.left < -12 or self.rect.top < -12 or self.rect.left > self.screen_width + 12 or self.rect.top > self.screen_height + 12):
         self.active = False
