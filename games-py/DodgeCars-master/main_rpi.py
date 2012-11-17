############################################################################################
###                                                                                      ###
### PyGame with three lanes of cars coming at you and you have to dodge them! Have fun!  ###
###                                                                                      ###
### Author: SUHAS SG                                                                     ###
### jargnar@gmail.com                                                                    ###
###                                                                                      ###
### suhased.wordpress.com                                                                ###
### twitter: @jargnar                                                                    ### 
### facebook: facebook.com/jargnar                                                       ###
###                                                                                      ###
###                                                                                      ###
### Disclaimer: The kelvinized font and the small car pictures                           ###
### is not mine and I found it on the internet.                                          ###
### All the other images are mine.                                                       ###
###                                                                                      ###
### Do Enjoy the game!                                                                   ###
### You need to have Python and PyGame installed to run it.                              ###
###                                                                                      ###
### Run it by typing "python dodgecars.py" in the terminal                               ###
###                                                                                      ###
###                                                                                      ###
############################################################################################

import pygame,sys,random
from collections import deque

#global init
pygame.init()
size = 800,600
textcolor = 233,230,20
speed = -3
up = right = True 
down = left = False
screen = pygame.display.set_mode(size)
bg = pygame.image.load("res/bg.png")
bgrect = bg.get_rect()
pygame.key.set_repeat(65,65)
	
class Car:
    	'Doc: Class Car represents the physical car that you control'
    	def __init__(self,lane):
        	self.img = pygame.image.load("res/car.png")
        	self.rect = self.img.get_rect()
		if lane == 1:
			self.rect = self.rect.move(730,195)
		elif lane == 2:
			self.rect = self.rect.move(730,270)
		elif lane == 3:
			self.rect = self.rect.move(730,355)
    	
	def left(self):
        	return self.rect.left
    	
	def right(self):
        	return self.rect.right
    	
	def top(self):
        	return self.rect.top
    	
	def bottom(self):
        	return self.rect.bottom
    	
	def move(self,x,y):
        	self.rect = self.rect.move(x,y)
    	
	def render(self):
        	screen.blit(self.img,self.rect)

	def get_rectangle(self):
		return self.rect


class Dodger:
	'Doc: Your car which will be dodging cars that belong to the class Car'
	def __init__(self):
		self.img = pygame.image.load("res/car3.png")
		self.rect = self.img.get_rect()
		self.rect = self.rect.move(30,270)
		self.lane = 2
	
	def left(self):
		return self.rect.left
	
	def right(self):
		return self.rect.right
	
	def top(self):
		return self.rect.top
	
	def bottom(self):
		return self.rect.bottom
	
	#some automata and states logic went here o_O
	def move(self,key):
	
		if key == up  and self.lane == 1:
			#self.rect = self.rect.move(0,0)
			self.lane = 1
		
		elif key == up and self.lane == 2:
			self.rect = self.rect.move(0,-75)
			self.lane = 1
		
		elif key == up and self.lane == 3:
			self.rect = self.rect.move(0,-85)
			self.lane = 2
		
		elif key == down and self.lane == 1:
			self.rect = self.rect.move(0,75)
			self.lane = 2
		
		elif key == down and self.lane == 2:
			self.rect = self.rect.move(0,85)
			self.lane = 3
		
		elif key == down and self.lane == 3:
			#self.rect = self.rect.move(0,0)
			self.lane = 3

	def render(self):
		screen.blit(self.img,self.rect)
	
	def shift(self, d):
		
		if d == right:
			if self.rect.right < 750:
				self.rect = self.rect.move(10,0)
		elif d == left:
			if self.rect.left > 20:
				self.rect = self.rect.move(-10,0)
	
	def jump(self):
		self.rect = self.rect.move(0,-25)
		
	def unjump(self):
		self.rect = self.rect.move(0,25)
	
	def get_lane(self):
		return self.lane

	
#play again? :)
def re_play():
	gover = pygame.image.load("res/gover.png")
	grect = gover.get_rect()

	#Play again please :D
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		screen.fill((55,200,44))
		screen.blit(gover,grect)
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_SPACE]: break
		pygame.display.flip()
	begin()


#oops gameover condition
def gameover(x,y):
	tempscreen = pygame.image.load("res/gameover.jpeg")
	trect = tempscreen.get_rect()
	boom = pygame.image.load("res/crash.png")
	brect = boom.get_rect()
	brect = brect.move(x,y)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		screen.blit(tempscreen,trect)
		screen.blit(boom,brect)
		
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_RETURN]:break
		pygame.display.flip()

	re_play()


#Lets BEGIN :D
def begin():
	
	#queues of cars in different lanes
	car1 = deque()
	car2 = deque()
	car3 = deque()
	
	#your car
	dodger = Dodger()

	score = 0
	timer = 32

	myfont = pygame.font.Font("res/Kelvinized.ttf",18)	
	
	#the game loop
	while 1:
        	for event in pygame.event.get():
            		if event.type == pygame.QUIT: sys.exit()
        
		screen.blit(bg,bgrect)
		
		#scoreboard
		if pygame.time.get_ticks()%200: score = score + 1
		scoreline = "DISTANCE: "+str(score)
		scoreboard = myfont.render(scoreline,1,textcolor)
		screen.blit(scoreboard,scoreboard.get_rect())
		 
		#car AI
		if pygame.time.get_ticks() % (100*random.randint(2,6)) == 0:
			car1.append(Car(1))
		if pygame.time.get_ticks() % (100*random.randint(3,5)) == 0:
			car2.append(Car(2))
		if pygame.time.get_ticks() % (100*random.randint(1,5)) == 0:
			car3.append(Car(3))

        	#move and render cars in diff lanes
		for car in car1:
            		car.move(speed,0)
            		car.render()
		for car in car2:
			car.move(speed,0)
			car.render()
		for car in car3:
			car.move(speed-1,0)
			car.render()
			
		moved = 0

		#User Input
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_UP:
					dodger.move(up)
			
				elif event.key == pygame.K_DOWN:
					dodger.move(down)
				
				elif event.key == pygame.K_RIGHT:
					dodger.shift(right)
	
				elif event.key == pygame.K_LEFT:
					dodger.shift(left)
				
				#elif event.key == pygame.K_SPACE:
				#	dodger.jump()
				#	moved = 1
					
		
		dodger.render()

		#Collision Detection
		for car in car1:
			if dodger.get_lane()==1:
				if car.left() < dodger.left() < car.right():
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])
				
				if car.left() in range(dodger.right()-2,dodger.right()+2,1): 
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])
		
				if car.right() == dodger.left()+1:
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])
		
		for car in car2:
			if dodger.get_lane()==2:
		 		if car.left() < dodger.left() < car.right():
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])

				if car.left() in range(dodger.right()-2,dodger.right()+2,1):
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])

                        	if car.right() == dodger.left()+1:
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])
		
		for car in car3:
			if dodger.get_lane()==3:
		 		if car.left() < dodger.left() < car.right():
					pygame.image.save(screen,"res/gameover.jpeg")
					x = car.get_rectangle()
					gameover(x[0],x[1])

				if car.left() in range(dodger.right()-2,dodger.right()+2,1):
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])

                        	if car.right() == dodger.left()+1:
                                	pygame.image.save(screen,"res/gameover.jpeg")
                                	x = car.get_rectangle()
                                	gameover(x[0],x[1])

		#if moved == 1:
                        #dodger.unjump()

		#memory cleanup
		if car1:
			if car1[0].right() < 0: car1.popleft()
		if car2:
			if car2[0].right() < 0: car2.popleft()
		if car3:
			if car3[0].right() < 0: car3.popleft()
	
		pygame.display.flip()

def main():

	#draw the welcome screen
	welcome = pygame.image.load("res/welcome.png")
	wrect = welcome.get_rect()
	wrect = wrect.move(40,40)

	#wait till the user presses "enter" key
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	
		screen.fill((55,200,44))
 		screen.blit(welcome,wrect)
		pressed = pygame.key.get_pressed()
		
		if pressed[pygame.K_RETURN]: break
	
		pygame.display.flip()
	
	#BEGIN THE GAME :D
	begin()

if __name__ == "__main__":
	main()
