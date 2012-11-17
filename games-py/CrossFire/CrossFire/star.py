# CrossFire - by David Christian
# This source code is free software, and licensed under the GPL v3
# Please see the LICENSE.TXT file or http://www.gnu.org/licenses/gpl.html for more information
import pygame, os, random
from pygame.locals import *

class Star(pygame.sprite.Sprite):   
   def __init__(self, screen_width, screen_height, start_x, start_y, speed, star_col):
      pygame.sprite.Sprite.__init__(self)
      self.screen_width = screen_width
      self.screen_height = screen_height
      self.vector_x = -speed
      self.vector_y = 0                                    
      self.image = pygame.Surface((3, 3))
      self.image.fill(star_col)
      self.rect = self.image.get_rect(topleft = (start_x, start_y))
   
   def update(self):
      self.rect.move_ip(self.vector_x, self.vector_y)
         
      if (self.rect.left < -12):
         self.rect.left = self.screen_width + 12
         self.rect.top = random.randint(0, self.screen_height)
      
