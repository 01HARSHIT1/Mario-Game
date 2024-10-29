import random                                                # importing random library
import numpy                                                 # importing numpy Library
import pandas                                                # importing pandas Library
import matplotlib                                            # importing matplotlib Library
import pygame                                                # importing pygame library
from pygame.locals import *                                  # Using pygame library
from pygame import mixer                                     # Using pygame library
import pickle                                                # importing pickle
from os import path                                          # Setting path

pygame.mixer.pre_init(44100, -16, 2, 512)                    # Setting position before other objects
mixer.init()                                                 # initing the given position
pygame.init()                                                # Now initing the object

clock = pygame.time.Clock()                                  # Setting real time for game reference
fps = 60                                                     # Setting game speed

screen_width = 1000                                          # Setting pannel width
screen_height = 1128                                         # Setting pannel height

screen = pygame.display.set_mode((screen_width, screen_height)) # Setting given height and width
pygame.display.set_caption('Platformer')                        # Making base for the project


#define font
font = pygame.font.SysFont('Bauhaus 93', 70)             # Declare the font
font_score = pygame.font.SysFont('Bauhaus 93', 30)       # Declare the font


#define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 3
max_levels = 7
score = 0


#define colours
white = (255, 255, 255)
blue = (0, 0, 255)


#load images
sun_img = pygame.image.load('1.png')                                  # using images by file handling by giving file path
bg_img = pygame.image.load('2.png')                                   # using images by file handling by giving file path
restart_img = pygame.image.load('restart_btn.png')                    # using images by file handling by giving file path
start_img = pygame.image.load('start_btn.png')                        # using images by file handling by giving file path
exit_img = pygame.image.load('exit_btn.png')                          # using images by file handling by giving file path

#load sounds
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('game_over.wav')
game_over_fx.set_volume(0.5)


def draw_text(text, font, text_col, x, y):                      # Creating function for text and image details used in project
	img = font.render(text, True, text_col)                     # Creating function for text and image details used in project
	screen.blit(img, (x, y))                                    # Giving object in function created


#function to reset level
def reset_level(level):                                         # Creating function to setting all object at Starting Position
	player.reset(100, screen_height - 130)                      # Setting objects at start
	blob_group.empty()                                          # Setting objects at start
	platform_group.empty()                                      # Setting objects at start
	coin_group.empty()                                          # Setting objects at start
	lava_group.empty()                                          # Setting objects at start
	exit_group.empty()                                          # Setting objects at start

	#load in level data and create world
	if path.exists(f'level{level}_data'):                       # Using file handling to give levels information in the program
		pickle_in = open(f'level{level}_data', 'rb')            # Using file handling to give levels information in the program and open in rb mode
		world_data = pickle.load(pickle_in)
	world = World(world_data)


	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)              # Setting Game object details
	coin_group.add(score_coin)                                     # Setting Game object details
	return world                                                   # Returning to main game


# Setting class object details used like images 
class Button():                                                    # Creating class button 
	def __init__(self, x, y, image):                               # Giving function to the image as required in game
		self.image = image                                         # Setting image propereties like size
		self.rect = self.image.get_rect()                          # Setting image propereties like size
		self.rect.x = x                                            # Setting image propereties like size
		self.rect.y = y                                            # Setting image propereties like size
		self.clicked = False                                       # Setting image propereties like size

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):                                          # Setting game setting and its work on click
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:     # Setting game setting and its work on click
				action = True                                                    # Setting game setting and its work on click
				self.clicked = True                                              # Setting game setting and its work on click

		if pygame.mouse.get_pressed()[0] == 0:                                   # Setting game setting and its work on click
			self.clicked = False                                                 # Setting game setting and its work on click


		#draw button
		screen.blit(self.image, self.rect)

		return action


# Creating Player object  
class Player():                                                 # Setting for player object in the project
	def __init__(self, x, y):                                   # Setting for player object in the project
		self.reset(x, y)                                        # Setting for player object in the project


# Creating function for the restart
	def update(self, game_over):                                # Setting function on restart and positing object back to start time
		dx = 0                                                  # Setting function on restart and positing object back to start time
		dy = 0                                                  # Setting function on restart and positing object back to start time
		walk_cooldown = 5                                       # Setting function on restart and positing object back to start time
		col_thresh = 20                                         # Setting function on restart and positing object back to start time



# Setting condition for game restart
		if game_over == 0:                                     # Setting game properties and function
			#get keypresses                
			key = pygame.key.get_pressed()                     # Setting game properties and function
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False: # Setting game properties and function
				jump_fx.play()                                 # Setting game properties and function
				self.vel_y = -15                               # Setting game properties and function
				self.jumped = True                             # Setting game properties and function
			if key[pygame.K_SPACE] == False:                   # Setting game properties and function
				self.jumped = False                            # Setting game properties and function
			if key[pygame.K_LEFT]:                             # Setting game properties and function
				dx -= 5                                        # Setting game properties and function
				self.counter += 1                              # Setting game properties and function
				self.direction = -1                            # Setting game properties and function
			if key[pygame.K_RIGHT]:                            # Setting game properties and function
				dx += 5                                        # Setting game properties and function
				self.counter += 1                              # Setting game properties and function
				self.direction = 1                             # Setting game properties and function
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:          # Setting game properties and function
				self.counter = 0                               # Setting game properties and function
				self.index = 0                                 # Setting game properties and function
				if self.direction == 1:                        # Setting game properties and function
					self.image = self.images_right[self.index] # Setting game properties and function
				if self.direction == -1:                       # Setting game properties and function
					self.image = self.images_left[self.index]  # Setting game properties and function


			#handle animation
			if self.counter > walk_cooldown:                           # Setting the motion and movement of player and object inside the game
				self.counter = 0	                                   # Setting the motion and movement of player and object inside the game
				self.index += 1                                        # Setting the motion and movement of player and object inside the game
				if self.index >= len(self.images_right):               # Setting the motion and movement of player and object inside the game
					self.index = 0                                     # Setting the motion and movement of player and object inside the game
				if self.direction == 1:                                # Setting the motion and movement of player and object inside the game
					self.image = self.images_right[self.index]         # Setting the motion and movement of player and object inside the game
				if self.direction == -1:                               # Setting the motion and movement of player and object inside the game
					self.image = self.images_left[self.index]          # Setting the motion and movement of player and object inside the game


			#add gravity
			self.vel_y += 1                                     # Giving condition on the object for their work and game functioning
			if self.vel_y > 10:                                 # Giving condition on the object for their work and game functioning
				self.vel_y = 10                                 # Giving condition on the object for their work and game functioning
			dy += self.vel_y                                    # Giving condition on the object for their work and game functioning

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy


# Resetting game screen
		elif game_over == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over


# Creating function to reset the game to its initing position and the game is over and restart option has run
	def reset(self, x, y):                                                    # Setting object back to start
		self.images_right = []                                                # Setting object back to start
		self.images_left = []                                                 # Setting object back to start
		self.index = 0                                                        # Setting object back to start
		self.counter = 0                                                      # Setting object back to start
		for num in range(1, 5):                                               # Setting object back to start
			img_right = pygame.image.load(f'guy{num}.png')                    # Setting object back to start
			img_right = pygame.transform.scale(img_right, (40, 80))           # Setting object back to start
			img_left = pygame.transform.flip(img_right, True, False)          # Setting object back to start
			self.images_right.append(img_right)                               # Setting object back to start
			self.images_left.append(img_left)                                 # Setting object back to start
		self.dead_image = pygame.image.load('ghost.png')                      # Setting object back to start
		self.image = self.images_right[self.index]                            # Setting object back to start
		self.rect = self.image.get_rect()                                     # Setting object back to start
		self.rect.x = x                                                       # Setting object back to start
		self.rect.y = y                                                       # Setting object back to start
		self.width = self.image.get_width()                                   # Setting object back to start
		self.height = self.image.get_height()                                 # Setting object back to start
		self.vel_y = 0                                                        # Setting object back to start
		self.jumped = False                                                   # Setting object back to start
		self.direction = 0                                                    # Setting object back to start
		self.in_air = True                                                    # Setting object back to start



# Creating the main world object for the game project
class World():                                    
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('3.png')
		grass_img = pygame.image.load('4.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1
			row_count += 1

# Creating self function for the player
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


# Creating function for giving setting to other game object as enemy 
class Enemy(pygame.sprite.Sprite):                                            # Initing the enemy object function 
	def __init__(self, x, y):                                                 # Giving properties to the object and its function
		pygame.sprite.Sprite.__init__(self)                                   # Giving properties to the object and its function
		self.image = pygame.image.load('blob.png')                            # Giving properties to the object and its function
		self.rect = self.image.get_rect()                                     # Giving properties to the object and its function
		self.rect.x = x                                                       # Giving properties to the object and its function
		self.rect.y = y                                                       # Giving properties to the object and its function
		self.move_direction = 1                                               # Giving properties to the object and its function
		self.move_counter = 0                                                 # Giving properties to the object and its function

# Creating the update function
	def update(self):                                                         # initing the self update function on player
		self.rect.x += self.move_direction                                    # initing the self update function on player
		self.move_counter += 1                                                # initing the self update function on player
		if abs(self.move_counter) > 50:                                       # initing the self update function on player
			self.move_direction *= -1                                         # initing the self update function on player
			self.move_counter *= -1                                           # initing the self update function on player


# Creating class for game object and images used as sprite in the program
class Platform(pygame.sprite.Sprite):                                               # Setting game platform and providing its function to it
	def __init__(self, x, y, move_x, move_y):                                       # Setting game platform and providing its function to it
		pygame.sprite.Sprite.__init__(self)                                         # Setting game platform and providing its function to it
		img = pygame.image.load('platform.png')                                     # Setting game platform and providing its function to it
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))       # Setting game platform and providing its function to it
		self.rect = self.image.get_rect()                                           # Setting game platform and providing its function to it
		self.rect.x = x                                                             # Setting game platform and providing its function to it
		self.rect.y = y                                                             # Setting game platform and providing its function to it
		self.move_counter = 0                                                       # Setting game platform and providing its function to it
		self.move_direction = 1                                                     # Setting game platform and providing its function to it
		self.move_x = move_x                                                        # Setting game platform and providing its function to it
		self.move_y = move_y                                                        # Setting game platform and providing its function to it


# Creating update function
	def update(self):                                                          # Update the game object for each time 
		self.rect.x += self.move_direction * self.move_x                       # Update the game object for each time 
		self.rect.y += self.move_direction * self.move_y                       # Update the game object for each time 
		self.move_counter += 1                                                 # Update the game object for each time 
		if abs(self.move_counter) > 50:                                        # Update the game object for each time 
			self.move_direction *= -1                                          # Update the game object for each time 
			self.move_counter *= -1                                            # Update the game object for each time 




# Creating enemy object 
class Lava(pygame.sprite.Sprite):                                               # Creating enemy object as obstacle for player
	def __init__(self, x, y):                                                   # Initing the enemy object
		pygame.sprite.Sprite.__init__(self)                                     # Setting properties for the object
		img = pygame.image.load('lava.png')                                     # Setting properties for the object
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))   # Setting properties for the object
		self.rect = self.image.get_rect()                                       # Setting properties for the object
		self.rect.x = x                                                         # Setting properties for the object
		self.rect.y = y                                                         # Setting properties for the object


# Creating coin object for player
class Coin(pygame.sprite.Sprite):                                               # Creating coin object as fun for player
	def __init__(self, x, y):                                                   # Initing the enemy object
		pygame.sprite.Sprite.__init__(self)                                     # Setting properties for the object
		img = pygame.image.load('coin.png')                                     # Setting properties for the object
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2)) # Setting properties for the object
		self.rect = self.image.get_rect()                                       # Setting properties for the object
		self.rect.center = (x, y)                                               # Setting properties for the object


# Creating exit for the game to end for that level
class Exit(pygame.sprite.Sprite):                                               # Creating exit objec for the player to wim the level
	def __init__(self, x, y):                                                   # Initing the exit object
		pygame.sprite.Sprite.__init__(self)                                     # Setting properties for the exit object and function
		img = pygame.image.load('exit.png')                                     # Setting properties for the exit object and function
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5))) # Setting properties for the exit object and function
		self.rect = self.image.get_rect()                                       # Setting properties for the exit object and function
		self.rect.x = x                                                         # Setting properties for the exit object and function
		self.rect.y = y                                                         # Setting properties for the exit object and function


# Creating player for the user
player = Player(100, screen_height - 130)                                       # Setting player setting for the game

blob_group = pygame.sprite.Group()                                              # Setting player setting for the game
platform_group = pygame.sprite.Group()                                          # Setting player setting for the game
lava_group = pygame.sprite.Group()                                              # Setting player setting for the game
coin_group = pygame.sprite.Group()                                              # Setting player setting for the game
exit_group = pygame.sprite.Group()                                              # Setting player setting for the game

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world= World(world_data)


#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)


run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100))

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		#if player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= max_levels:
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
				if restart_button.draw():
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()