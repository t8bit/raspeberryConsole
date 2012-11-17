# CrossFire - by David Christian
# This source code is free software, and licensed under the GPL v3
# Please see the LICENSE.TXT file or http://www.gnu.org/licenses/gpl.html for more information
import pygame, os
from pygame.locals import *

class PlayerBottom(pygame.sprite.Sprite):

   def __init__(self, screen_width, screen_height, start_x, start_y):
      pygame.sprite.Sprite.__init__(self)
      self.screen_width = screen_width
      self.screen_height = screen_height
      self.image = pygame.image.load(os.path.join("data", "playerup.png")).convert()                                  
      self.image.set_colorkey((255,0,255))
      self.rect = self.image.get_rect(topleft = (start_x, start_y))
      
   def update(self):
      # Check for key states
      keystate = pygame.key.get_pressed()
      
      if keystate[K_LEFT]:
         self.rect.move_ip(-7, 0)
      if keystate[K_RIGHT]:
         self.rect.move_ip(7, 0)      
      
      SCREENRECT = Rect(0, 0, self.screen_width, self.screen_height)
      self.rect.clamp_ip(SCREENRECT)


class PlayerSide(pygame.sprite.Sprite):

   def __init__(self, screen_width, screen_height, start_x, start_y):
      pygame.sprite.Sprite.__init__(self)
      self.screen_width = screen_width
      self.screen_height = screen_height
      self.image = pygame.image.load(os.path.join("data", "playerside.png")).convert() #ALWAYS CALL CONVERT - SPEEDS THINGS UP FOR SDL
      self.image.set_colorkey((255,0,255))
      self.rect = self.image.get_rect(topleft = (start_x, start_y))
      
   def update(self):
      # Check for key states
      keystate = pygame.key.get_pressed()
            
      if keystate[K_UP]:
         self.rect.move_ip(0, -7)
      if keystate[K_DOWN]:
         self.rect.move_ip(0, 7)
      
      SCREENRECT = Rect(0, 0, self.screen_width, self.screen_height)
      self.rect.clamp_ip(SCREENRECT)
