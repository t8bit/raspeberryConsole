import pygame, os
from pygame.locals import *

class Particle(pygame.sprite.Sprite):   
   def __init__(self, screen_width, screen_height, sprite_image):
      pygame.sprite.Sprite.__init__(self)
      self.screen_width = screen_width
      self.screen_height = screen_height
      self.vector_x = 0
      self.vector_y = 0
      self.active = False      
      self.image = sprite_image
      self.image.set_colorkey((255,0,255))
      self.rect = self.image.get_rect(topleft = (0, 0))
      self.move_count = 0
      
   def update(self):
      if (self.active):
         self.rect.move_ip(self.vector_x, self.vector_y)
         self.move_count -= 1
         if self.move_count == 0:
            self.active = False
         
      if (self.rect.left < -12 or self.rect.top < -12 or self.rect.left > self.screen_width + 12 or self.rect.top > self.screen_height + 12):
         self.active = False
