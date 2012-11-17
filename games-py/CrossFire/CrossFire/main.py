# CrossFire - by David Christian
# This source code is free software, and licensed under the GPL v3
# Please see the LICENSE.TXT file or http://www.gnu.org/licenses/gpl.html for more information

import pygame, random, os, pygame.mixer
from pygame.locals import *
from player import PlayerBottom
from player import PlayerSide
from projectile import Projectile
from star import Star
from baddie import Baddie
from particle import Particle

def main():

    def create_particles(number, x, y, image):
        for count in range(number):
            for particle_count in range(MAX_PARTICLES):
                if particles[particle_count].active == False:
                    particles[particle_count].active = True
                    particles[particle_count].image = image
                    particles[particle_count].rect.left = x
                    particles[particle_count].rect.top = y
                    # Bigger number == bigger range explosion
                    if number > 15:
                        particles[particle_count].move_count = random.randint(20, 30)
                    else:
                        particles[particle_count].move_count = random.randint(10, 17)
                        
                    if random.randint(0, 10) > 5:
                        particles[particle_count].vector_x = 0 - random.randint(0, 4) 
                        particles[particle_count].vector_y = 0 - random.randint(0, 4)
                    else:
                        particles[particle_count].vector_x = random.randint(0, 4) 
                        particles[particle_count].vector_y = random.randint(0, 4)
                    break
    
    # Some constants
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    FPS = 60
    STARS = 18
    PLAYER_BULLETS = 40

    MAX_BADDIES = 15    
    MAX_UFOS = 1
    MAX_BADDIE_BULLETS = 30

    MAX_PARTICLES = 200

    TITLE_SCREEN_MODE = 2
    GAME_MODE = 1

    high_score = 750000
    beaten_high_score = False
    
    # Some game control stuff
    attack_timer = 0
    attack_max = 70
    ufo_attack_timer = 0
    ufo_attack_max = 500
    max_baddie_speed = 2
    max_ufo_speed = 2
    show_smiley = False 
    
    game_wave = 1
    baddies_killed = 0
    wave_break = 100
    wave_target_kills = 50
    game_over = False
    game_over_timer = 500
    game_victory = False
    game_victory_particle_timer = 0
    game_mode = TITLE_SCREEN_MODE
    
    baddie_fire_timer = 0
    baddie_fire_max = 50

    title_freeplay_timer = 0
    title_freeplay_on = False

    title_menu_choice = 0
        
    # Init the pygame library and sort the display
    pygame.init() 
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("CrossFire")
    clock = pygame.time.Clock()

    # Show loading message...
    game_font = pygame.font.Font(os.path.join("data", "04b_25__.ttf"), 18)
    screen.fill((0,0,0))
    screen.blit(game_font.render("Loading....", 0, ((176, 0, 0))), (270, SCREEN_HEIGHT / 2 - 36))
    pygame.display.flip()
    
    # Sort the sound driver
    pygame.mixer.quit()
    sound = pygame.mixer.init()
    
    player_shoot_sound = pygame.mixer.Sound(os.path.join("data", "lazer1.wav"))
    ufo_sound = pygame.mixer.Sound(os.path.join("data", "ufo.wav"))
    ufo_sound.set_volume(0.35)
    baddie_shoot_sound = pygame.mixer.Sound(os.path.join("data", "shoot2.wav"))
    wave_sound = pygame.mixer.Sound(os.path.join("data", "newwave.wav"))
    baddie_splosion = pygame.mixer.Sound(os.path.join("data", "explode1.wav"))
    player_boom_1 = pygame.mixer.Sound(os.path.join("data", "damage.wav"))
    player_boom_2 = pygame.mixer.Sound(os.path.join("data", "player_dead.wav"))
    menu_move_sound = pygame.mixer.Sound(os.path.join("data", "menu_move.wav"))
    exit_sound = pygame.mixer.Sound(os.path.join("data", "exit.wav"))
    start_sound = pygame.mixer.Sound(os.path.join("data", "start.wav"))
    win_sound = pygame.mixer.Sound(os.path.join("data", "win.wav"))
    
    # Load the gfx in
    invader_image = pygame.image.load(os.path.join("data", "invader.png")).convert()
    redinvader_image = pygame.image.load(os.path.join("data", "redthing.png")).convert()
    drone_image = pygame.image.load(os.path.join("data", "thingy.png")).convert()
    ufo_image = pygame.image.load(os.path.join("data", "ufo.png")).convert()
    player_bullet_image = pygame.image.load(os.path.join("data", "bullet1.png")).convert()
    game_font = pygame.font.Font(os.path.join("data", "04b_25__.ttf"), 18)
    game_font_large = pygame.font.Font(os.path.join("data", "04b_25__.ttf"), 36)
    game_font_xl = pygame.font.Font(os.path.join("data", "04b_25__.ttf"), 46)
    baddie_bullet_image = pygame.image.load(os.path.join("data", "bullet2.png")).convert()
    player_health_image = pygame.Surface((8, 16))
    player_health_image.fill((176, 0, 0))

    # Create some particle images
    red_particle_image = pygame.Surface((8, 8))
    red_particle_image.fill((176, 0, 0))
    green_particle_image = pygame.Surface((8, 8))
    green_particle_image.fill((31, 92, 14))
    blue_particle_image = pygame.Surface((8, 8))
    blue_particle_image.fill((46, 102, 187))
    gray_particle_image = pygame.Surface((8, 8))
    gray_particle_image.fill((88, 88, 88))
    yellow_particle_image = pygame.Surface((8, 8))
    yellow_particle_image.fill((255, 206, 0))

    # Setup the player objects
    player_bottom = PlayerBottom(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 35)
    player_side = PlayerSide(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH -35, SCREEN_HEIGHT / 2)
    player_fire_rate = 5
    player_fire_delay_left = 0
    player_fire_delay_right = 0
    player_score = 0
    player_shield = 9
    player_flash_timer = 0
    player_flash_on = False
    
    # Prepare the player pointed projectiles!
    player_bullets = []
    for count in range(PLAYER_BULLETS):
        player_bullets.append(Projectile(SCREEN_WIDTH, SCREEN_HEIGHT, player_bullet_image))
        player_bullets[count].active = False

    # Baddie bullets
    baddie_bullets = []
    for count in range(MAX_BADDIE_BULLETS):
        baddie_bullets.append(Projectile(SCREEN_WIDTH, SCREEN_HEIGHT, baddie_bullet_image))
        baddie_bullets[count].active = False

    # Setup the starfield
    stars = []    
    for count in range(STARS / 3):
        stars.append(Star(SCREEN_WIDTH, SCREEN_HEIGHT, random.randint(0, SCREEN_WIDTH),  random.randint(0, SCREEN_HEIGHT) , 4, (175, 175, 175)))        
    for count in range(STARS / 3):
        stars.append(Star(SCREEN_WIDTH, SCREEN_HEIGHT, random.randint(0, SCREEN_WIDTH),  random.randint(0, SCREEN_HEIGHT) , 3, (88, 88, 88)))        
    for count in range(STARS / 3):
        stars.append(Star(SCREEN_WIDTH, SCREEN_HEIGHT, random.randint(0, SCREEN_WIDTH),  random.randint(0, SCREEN_HEIGHT) , 1, (88, 88, 88)))        

    # Prepare the various baddies (max of 9 each)
    invaders = []
    red_invaders = []
    drones = []
    
    for count in range(MAX_BADDIES):
        # Green invaders
        invaders.append(Baddie(SCREEN_WIDTH, SCREEN_HEIGHT, invader_image))
        invaders[count].rect.top = 0
        invaders[count].rect.left = 0
        invaders[count].vector_x = 0
        invaders[count].vector_y = 0
        invaders[count].active = False
        invaders[count].anim_max_frame = 3
        invaders[count].movement_type = 0 

        # Red invaders 
        red_invaders.append(Baddie(SCREEN_WIDTH, SCREEN_HEIGHT, redinvader_image))
        red_invaders[count].rect.top = 0
        red_invaders[count].rect.left = 0
        red_invaders[count].vector_x = 0
        red_invaders[count].vector_y = 0
        red_invaders[count].active = False
        red_invaders[count].anim_max_frame = 3
        red_invaders[count].movement_type =0 

        # Drone things
        drones.append(Baddie(SCREEN_WIDTH, SCREEN_HEIGHT, drone_image))
        drones[count].rect.top = 0
        drones[count].rect.left = 0
        drones[count].vector_x = 0
        drones[count].vector_y = 0
        drones[count].active = False
        drones[count].anim_max_frame = 3
        drones[count].movement_type = 1 

    ufos = []
    for count in range(MAX_UFOS):
        ufos.append(Baddie(SCREEN_WIDTH, SCREEN_HEIGHT, ufo_image))
        ufos[count].anim_max_frame = 9

    # Setup particles
    particles = []
    for count in range(MAX_PARTICLES):
        particles.append(Particle(SCREEN_WIDTH, SCREEN_HEIGHT, red_particle_image))
        particles[count].active = False
    
    # Here we go..... main loop time
    # ------------------------------
    main_loop = True    
    baddies_onscreen = False
    
    while main_loop:
        
        # Clear the screen (NOTE: This is not particularly efficient, but deadline is looming!)
        screen.fill((0,0,0)) 

        # Process the stars
        for count in range(STARS):
            stars[count].update()
            screen.blit(stars[count].image, stars[count].rect)

        # Are we in game or at the title screen?    
        if game_mode == TITLE_SCREEN_MODE:

            #####################
            # TITLE SCREEN MODE #
            #####################
            screen.blit(game_font_xl.render("CrossFire", 0, ((255, 206, 0))), (230, 100))

            # Toggle little 'insert coin' message. It was originally 'Freeplay Mode' but I liked 'insert coin' more :)
            title_freeplay_timer += 1
            if title_freeplay_timer > 30:
                title_freeplay_timer = 0
                if title_freeplay_on == True:
                    title_freeplay_on = False
                else:
                    title_freeplay_on = True
    
            if title_freeplay_on == True:
                screen.blit(game_font.render("Insert Coin", 0, ((175, 175, 175))), (280, 380))

            if title_menu_choice == 0:
                screen.blit(game_font.render("Start", 0, ((255, 206, 0))), (300, 225))
            else:
                screen.blit(game_font.render("Start", 0, ((176, 0, 0))), (300, 225))           
                
            if title_menu_choice == 1:
                screen.blit(game_font.render("Exit", 0, ((255, 206, 0))), (308, 250))
            else:
                screen.blit(game_font.render("Exit", 0, ((176, 0, 0))), (308, 250))

            screen.blit(game_font.render("Z and X to fire, cursor keys control both ships", 0, ((176, 0, 0))), (120, 450))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu_move_sound.play()
                        title_menu_choice -= 1
                        if title_menu_choice < 0:
                            title_menu_choice = 0

                    if event.key == pygame.K_DOWN:
                        title_menu_choice += 1
                        menu_move_sound.play()
                        if title_menu_choice > 1:
                            title_menu_choice = 1
                                                        
                    if event.key == pygame.K_ESCAPE:
                        main_loop = False
                   
                    if event.key == pygame.K_z or event.key == pygame.K_x or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if title_menu_choice == 0:
                            # Start new game... reset values to defaults
                            start_sound.play()
                            attack_timer = 0
                            attack_max = 90
                            ufo_attack_timer = 0
                            ufo_attack_max = 500
                            max_baddie_speed = 2
                            max_ufo_speed = 2
                            show_smiley = False                             
                            game_wave = 1
                            beaten_high_score = False
                            baddies_killed = 0
                            wave_break = 100
                            wave_target_kills = 30
                            game_over = False
                            game_over_timer = 500
                            game_mode = GAME_MODE
                            game_victory = False
                            game_victory_particle_timer = 0
                            baddie_fire_timer = 0
                            baddie_fire_max = 50
                            player_fire_rate = 5
                            player_fire_delay_left = 0
                            player_fire_delay_right = 0
                            player_score = 0
                            player_shield = 9
                            player_flash_timer = 0
                            player_flash_on = False

                            # Make sure all the baddies, bullets and particles are deactivated
                            for count in range(MAX_BADDIES):
                                invaders[count].active = False
                                red_invaders[count].active = False
                                drones[count].active = False

                            for count in range(PLAYER_BULLETS):
                                player_bullets[count].active = False

                            for count in range(MAX_UFOS):
                                ufos[count].active = False

                            for count in range(MAX_BADDIE_BULLETS):
                                baddie_bullets[count].active = False

                            for count in range(MAX_PARTICLES):
                                particles[count].active = False
                                                            
                        if title_menu_choice == 1:
                            exit_sound.play()
                            main_loop = False
        else:
            
            #############
            # GAME MODE #
            #############
            # Grab all of the events and search for ones we are interested in, such as keyboard presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_mode = TITLE_SCREEN_MODE
                    # Has bottom player fired?
                    if event.key == pygame.K_z and player_fire_delay_left > player_fire_rate and game_over == False:
                        # Pop off a few projectiles...                    
                        for count in range(PLAYER_BULLETS):
                            if (player_bullets[count].active == False): # Find a 'free' bullet for the bottom ship
                                player_bullets[count].active = True
                                player_bullets[count].rect.top = player_bottom.rect.top
                                player_bullets[count].rect.left = player_bottom.rect.left + 12
                                player_bullets[count].vector_x = 0
                                player_bullets[count].vector_y = -9
                                player_fire_delay_left = 0
                                player_shoot_sound.play()                                
                                break
                    # Has side player fired
                    if event.key == pygame.K_x and player_fire_delay_right > player_fire_rate and game_over == False:
                        for count in range(PLAYER_BULLETS):
                            if (player_bullets[count].active == False):
                                player_bullets[count].active = True
                                player_bullets[count].rect.top = player_side.rect.top + 12
                                player_bullets[count].rect.left = player_side.rect.left
                                player_bullets[count].vector_x = -9
                                player_bullets[count].vector_y = 0
                                player_fire_delay_right = 0
                                player_shoot_sound.play()                            
                                break
                            
                    if event.key == pygame.K_F9:
                        show_smiley = True                       
        
            if show_smiley:
                screen.blit(game_font_large.render("c:)", 0, ((255, 0, 0))), (SCREEN_WIDTH /2 , 10))
            
            # Manage baddie creation...
            attack_timer += 1
            ufo_attack_timer += 1
                    
            # Time for an attack?
            if attack_timer > attack_max and wave_break < 1 and baddies_killed < wave_target_kills and game_over == False:
                # Time for a new attack formation from the side... how many free baddies are there?
                attack_timer = 0            
                # Which baddie? Pick randomly... 0 = Green Invader, 1 = Drone, 2 = Red Invader                                        
                if game_wave > 2:                    
                    baddie_type = random.randint(0,2)
                else:
                    baddie_type = random.randint(0,1)
                    
                direction = random.randint(0, 1)
                if baddie_type == 0:
                    for count in range(MAX_BADDIES):  
                        if invaders[count].active == False:                                                    
                            if direction == 0: # from left
                                invaders[count].rect.left = -32
                                invaders[count].rect.top = random.randint(0, (SCREEN_HEIGHT - 64) / 32) * 32
                                invaders[count].vector_x = max_baddie_speed
                                invaders[count].vector_y = 0
                                invaders[count].active = True
                                break
                            else:
                                # from top
                                invaders[count].rect.left = random.randint(0, (SCREEN_WIDTH - 64) / 32) * 32
                                invaders[count].rect.top = -32
                                invaders[count].vector_x = 0
                                invaders[count].vector_y = max_baddie_speed
                                invaders[count].active = True
                                break
                elif baddie_type == 1:
                    for count in range(MAX_BADDIES):  
                        if drones[count].active == False:                                                                            
                            if direction == 0: # from left
                                drones[count].rect.left = -32
                                drones[count].rect.top = random.randint(0, (SCREEN_HEIGHT - 64) / 32) * 32
                                drones[count].vector_x = max_baddie_speed
                                drones[count].vector_y = 0
                                drones[count].active = True
                                drones[count].movement_type = 2
                                break
                            else:
                                # from top
                                drones[count].rect.left = random.randint(0, (SCREEN_WIDTH - 64) / 32) * 32
                                drones[count].rect.top = -32
                                drones[count].vector_x = 0
                                drones[count].vector_y = max_baddie_speed
                                drones[count].active = True
                                drones[count].movement_type = 1
                                break        
                elif baddie_type == 2:
                    for count in range(MAX_BADDIES):  
                        if red_invaders[count].active == False:                                                                            
                            if direction == 0: # from left
                                red_invaders[count].rect.left = -32
                                red_invaders[count].rect.top = random.randint(0, (SCREEN_HEIGHT - 64) / 32) * 32
                                red_invaders[count].vector_x = max_baddie_speed
                                red_invaders[count].vector_y = random.randint(0, 1) - random.randint(0, 1)
                                red_invaders[count].active = True
                                break
                            else:
                                # from top
                                red_invaders[count].rect.left = random.randint(0, (SCREEN_WIDTH - 64) / 32) * 32
                                red_invaders[count].rect.top = -32
                                red_invaders[count].vector_x = random.randint(0, 1) - random.randint(0, 1)
                                red_invaders[count].vector_y = max_baddie_speed
                                red_invaders[count].active = True
                                break
                            
            # Handle ufo attacks
            for count in range(MAX_UFOS):
                if ufos[count].active == False and ufo_attack_timer > ufo_attack_max and wave_break < 1 and game_over == False:
                    ufo_attack_timer = 0
                    ufo_sound.play()
                    # Pick a random direction
                    if random.randint(0, 10) > 4:
                        # Attack the side player
                        if random.randint(0, 10) > 4:
                            ufos[count].rect.top = -32
                            ufos[count].rect.left = SCREEN_WIDTH - 32
                            ufos[count].vector_y = max_ufo_speed
                            ufos[count].vector_x = 0
                            ufos[count].active = True
                        else:
                            ufos[count].rect.top = SCREEN_HEIGHT + 32
                            ufos[count].rect.left = SCREEN_WIDTH -32
                            ufos[count].vector_y = - max_ufo_speed
                            ufos[count].vector_x = 0
                            ufos[count].active = True
                    else:
                        # Attack the bottom player
                        if random.randint(0, 10) > 4:
                            ufos[count].rect.top = SCREEN_HEIGHT - 32
                            ufos[count].rect.left = -32
                            ufos[count].vector_x = max_ufo_speed
                            ufos[count].vector_y = 0
                            ufos[count].active = True            
                        else:
                            ufos[count].rect.top = SCREEN_HEIGHT -32
                            ufos[count].rect.left = SCREEN_WIDTH + 32                        
                            ufos[count].vector_x = 0 - max_ufo_speed
                            ufos[count].vector_y = 0
                            ufos[count].active = True                                        
                        
            # Process particles
            for count in range(MAX_PARTICLES):
                if particles[count].active == True:
                    particles[count].update()
                    screen.blit(particles[count].image, particles[count].rect)
                    
            # Process the player objects
            player_bottom.update()
            player_side.update()
        
            # Is player recovering from damage?
            if player_flash_timer > 0:
                player_flash_timer -= 1
                if player_flash_on == True:
                    player_flash_on = False
                else:
                    player_flash_on = True
            else:
                player_flash_on = False
                
            if player_flash_on == False and game_over == False:
                screen.blit(player_bottom.image, player_bottom.rect)
                screen.blit(player_side.image, player_side.rect)
            
            # Handle all of the player projectiles
            for count in range(PLAYER_BULLETS):
                if (player_bullets[count].active):
                    player_bullets[count].update()
                    screen.blit(player_bullets[count].image, player_bullets[count].rect)            

            # Handle all of the baddie projectiles
            for count in range(MAX_BADDIE_BULLETS):
                if (baddie_bullets[count].active == True):
                    baddie_bullets[count].update()            
                    screen.blit(baddie_bullets[count].image, baddie_bullets[count].rect)            
            
            # Slight delay for players fire rate
            player_fire_delay_left += 1
            player_fire_delay_right += 1                                

            # Move and draw the invaders
            for count in range(MAX_BADDIES):            
                if invaders[count].active:
                    invaders[count].update()
                    screen.blit(invaders[count].image, invaders[count].rect, (32 * invaders[count].anim_frame, 0, 32, 32))
                    # Has invader collided with a player bullet?
                    for collision_count in range(PLAYER_BULLETS):
                        if player_bullets[collision_count].active == True:
                            # Have to use a bit of jiggery pokery on the collision because the sprite.rect won't work as it is (too wide due to animation frames)
                            if player_bullets[collision_count].rect.colliderect((invaders[count].rect.left, invaders[count].rect.top, 32, 32)):        
                                invaders[count].active = False
                                player_score += 2000;
                                player_bullets[collision_count].active = False
                                baddies_killed += 1
                                baddie_splosion.play()
                                create_particles(15, invaders[count].rect.left + 8, invaders[count].rect.top + 8, green_particle_image)
                                
            # Move and draw the red invaders
            for count in range(MAX_BADDIES):            
                if red_invaders[count].active:
                    red_invaders[count].update()
                    screen.blit(red_invaders[count].image, red_invaders[count].rect, (32 * red_invaders[count].anim_frame, 0, 32, 32))
                    # Has invader collided with a player bullet?
                    for collision_count in range(PLAYER_BULLETS):
                        if player_bullets[collision_count].active == True:
                            # Have to use a bit of jiggery pokery on the collision because the sprite.rect won't work as it is (too wide due to animation frames)
                            if player_bullets[collision_count].rect.colliderect((red_invaders[count].rect.left, red_invaders[count].rect.top, 32, 32)):        
                                red_invaders[count].active = False
                                player_score += 4750;
                                player_bullets[collision_count].active = False
                                baddies_killed += 1   
                                baddie_splosion.play()
                                create_particles(15, red_invaders[count].rect.left + 8, red_invaders[count].rect.top + 8, red_particle_image)
                                
            # Time for red invaders to shoot?
            baddie_fire_timer += 1
            if baddie_fire_timer > baddie_fire_max and game_over == False:
                baddie_fire_timer = 0
                for count in range(MAX_BADDIES):
                    if red_invaders[count].active == True and red_invaders[count].rect.top < SCREEN_HEIGHT - 50 and red_invaders[count].rect.top > 50:
                        baddie_shoot_sound.play()
                        bullets = 0
                        for bullet_count in range(MAX_BADDIE_BULLETS):
                            if baddie_bullets[bullet_count].active == False:
                                if random.randint(0,10) > 4:
                                    baddie_bullets[bullet_count].active = True
                                    baddie_bullets[bullet_count].rect.top = red_invaders[count].rect.top + 8
                                    baddie_bullets[bullet_count].rect.left = red_invaders[count].rect.left + 12
                                    baddie_bullets[bullet_count].vector_x = 7
                                    baddie_bullets[bullet_count].vector_y = 0 
                                    break
                                else:
                                    baddie_bullets[bullet_count].active = True
                                    baddie_bullets[bullet_count].rect.top = red_invaders[count].rect.top +16
                                    baddie_bullets[bullet_count].rect.left = red_invaders[count].rect.left + 8
                                    baddie_bullets[bullet_count].vector_x = 0
                                    baddie_bullets[bullet_count].vector_y = 7
                                    break
                            
            # Move and draw the ufo
            for count in range(MAX_UFOS):
                if ufos[count].active == True:
                    ufos[count].update()
                    screen.blit(ufos[count].image, ufos[count].rect, (32 * ufos[count].anim_frame, 0, 32, 32))
                    # Has invader collided with a ufo?
                    for collision_count in range(PLAYER_BULLETS):
                        if player_bullets[collision_count].active == True:                        
                            if player_bullets[collision_count].rect.colliderect((ufos[count].rect.left, ufos[count].rect.top, 32, 32)):        
                                ufos[count].active = False
                                player_score += 3250
                                player_bullets[collision_count].active = False
                                baddies_killed += 1
                                baddie_splosion.play()
                                create_particles(15, ufos[count].rect.left + 8, ufos[count].rect.top + 8, gray_particle_image)

            # Move and draw the drones
            for count in range(MAX_BADDIES):            
                if drones[count].active:
                    drones[count].update()
                    screen.blit(drones[count].image, drones[count].rect, (32 * drones[count].anim_frame, 0, 32, 32))
                    # Has invader collided with a player bullet?
                    for collision_count in range(PLAYER_BULLETS):
                        if player_bullets[collision_count].active == True:
                            # Have to use a bit of jiggery pokery on the collision because the sprite.rect won't work as it is (too wide due to animation frames)
                            if player_bullets[collision_count].rect.colliderect((drones[count].rect.left, drones[count].rect.top, 32, 32)):        
                                drones[count].active = False
                                player_score += 2500;
                                player_bullets[collision_count].active = False
                                baddies_killed += 1
                                baddie_splosion.play()
                                create_particles(15, drones[count].rect.left + 8, drones[count].rect.top + 8, blue_particle_image)

            # Check for baddie to player collisions
            if player_flash_timer < 1 and game_over == False:
                player_hit = False
                for collision_count in range(MAX_BADDIES):
                    # Have any invaders collided with player?
                    if invaders[collision_count].active == True:
                        if player_side.rect.colliderect((invaders[collision_count].rect.left + 5, invaders[collision_count].rect.top + 5, 24, 24)):        
                            invaders[collision_count].active = False
                            create_particles(15, invaders[collision_count].rect.left + 8, invaders[collision_count].rect.top + 8, green_particle_image)
                            player_hit = True
                        if player_bottom.rect.colliderect((invaders[collision_count].rect.left + 5, invaders[collision_count].rect.top + 5, 24, 24)):        
                            invaders[collision_count].active = False
                            create_particles(15, invaders[collision_count].rect.left + 8, invaders[collision_count].rect.top + 8, green_particle_image)
                            player_hit = True
                            
                    # Have any drones collided with player?
                    if red_invaders[collision_count].active == True:
                        if player_side.rect.colliderect((red_invaders[collision_count].rect.left + 5, red_invaders[collision_count].rect.top + 5, 24, 24)):        
                            red_invaders[collision_count].active = False
                            create_particles(15, red_invaders[collision_count].rect.left + 8, red_invaders[collision_count].rect.top + 8, red_particle_image)
                            player_hit = True
                        if player_bottom.rect.colliderect((red_invaders[collision_count].rect.left + 5, red_invaders[collision_count].rect.top + 5, 24, 24)):        
                            red_invaders[collision_count].active = False
                            create_particles(15, red_invaders[collision_count].rect.left + 8, red_invaders[collision_count].rect.top + 8, red_particle_image)
                            player_hit = True
                            
                    # Have any drones collided with player?
                    if drones[collision_count].active == True:
                        if player_side.rect.colliderect((drones[collision_count].rect.left + 5, drones[collision_count].rect.top + 5, 24, 24)):        
                            drones[collision_count].active = False                    
                            create_particles(15, drones[collision_count].rect.left + 8, drones[collision_count].rect.top + 8, blue_particle_image)
                            player_hit = True
                        if player_bottom.rect.colliderect((drones[collision_count].rect.left + 5, drones[collision_count].rect.top + 5, 24, 24)):        
                            drones[collision_count].active = False
                            create_particles(15, drones[collision_count].rect.left + 8, drones[collision_count].rect.top + 8, blue_particle_image)
                            player_hit = True

                # Have any ufos collided with player?
                for collision_count in range (MAX_UFOS):
                    if ufos[collision_count].active == True:
                        if player_side.rect.colliderect((ufos[collision_count].rect.left + 5, ufos[collision_count].rect.top + 5, 24, 24)):        
                            ufos[collision_count].active = 0
                            create_particles(15, ufos[collision_count].rect.left + 8, ufos[collision_count].rect.top + 8, gray_particle_image)
                            player_hit = True
                        if player_bottom.rect.colliderect((ufos[collision_count].rect.left + 5, ufos[collision_count].rect.top + 5, 24, 24)):        
                            ufos[collision_count].active = 0
                            create_particles(15, ufos[collision_count].rect.left + 8, ufos[collision_count].rect.top + 8, gray_particle_image)
                            player_hit = True

                # Have any enemy bullets collided with player?
                for collision_count in range (MAX_BADDIE_BULLETS):
                    if baddie_bullets[collision_count].active == True:
                        if player_side.rect.colliderect((baddie_bullets[collision_count].rect.left, baddie_bullets[collision_count].rect.top, 8, 8)):        
                            baddie_bullets[collision_count].active = 0
                            player_hit = True
                        if player_bottom.rect.colliderect((baddie_bullets[collision_count].rect.left, baddie_bullets[collision_count].rect.top, 8, 8)):        
                            baddie_bullets[collision_count].active = 0
                            player_hit = True

                # Has player been hit by anything nasty?
                if player_hit == True and game_over == False:          
                    player_shield -= 1
                    create_particles(5, 85 + ((player_shield) * 11), 32, red_particle_image)                    
                    player_flash_timer = 50
                    player_boom_1.play()                
                        
                    if player_shield == 0:
                        player_boom_2.play()
                        create_particles(20, player_bottom.rect.left + 8, player_bottom.rect.top + 8, red_particle_image)
                        create_particles(20, player_bottom.rect.left + 8, player_bottom.rect.top + 8, yellow_particle_image)
                        create_particles(20, player_side.rect.left + 8, player_side.rect.top + 8, red_particle_image)
                        create_particles(20, player_side.rect.left + 8, player_side.rect.top + 8, yellow_particle_image)
                        game_over = True

            # Display hud stuff
            screen.blit(game_font.render("Score: " + str(player_score), 0, ((255, 206, 0))), (10, 10))
            screen.blit(game_font.render("High Score: " + str(high_score), 0, ((255, 206, 0))), (460, 10))

            # Beaten high score?
            if player_score > high_score:
                high_score = player_score
                # Make a little fuss of the player :)
                if beaten_high_score == False:
                    beaten_high_score = True
                    for count in range(5):
                        create_particles(5, 460 + (count * 15), 15, yellow_particle_image)                        
                
            if wave_break > 0:
                wave_break -= 1
                if game_over == False:
                    screen.blit(game_font_large.render("Wave " + str(game_wave) + " of 9", 0, ((255, 206, 0))), (240, SCREEN_HEIGHT / 2 - 36))        

            for count in range(player_shield):
                screen.blit(game_font.render("Shields:", 0, ((255, 206, 0))), (10, 30))
                screen.blit(player_health_image, (85 + (count * 11), 32))
            
            if game_over == True:
                # Loss or victory?
                if game_victory == False:
                    screen.blit(game_font_large.render("GAME OVER", 0, ((176, 0, 0))), (260, SCREEN_HEIGHT / 2 - 36))
                else:
                    screen.blit(game_font_large.render("YOU ARE AWESOME!!!", 0, ((255, 206, 0))), (160, SCREEN_HEIGHT / 2 - 36))
                    game_victory_particle_timer += 1
                    if game_victory_particle_timer > 10:
                        create_particles(30, random.randint(160, 450), random.randint(160, 300), red_particle_image)                       
                        
                game_over_timer -= 1
                if game_over_timer == 0:
                    game_mode = TITLE_SCREEN_MODE
                    
            # Time for a new wave? Only start new wave display when all baddies are dead
            baddies_onscreen = False
            for count in range(MAX_BADDIES):
                if invaders[count].active == True:
                    baddies_onscreen = True
                    break
                if red_invaders[count].active == True:
                    baddies_onscreen = True
                    break
                if drones[count].active == True:
                    baddies_onscreen = True
                    break
                
            for count in range(MAX_UFOS):
                if ufos[count].active == True:
                    baddies_onscreen = True

            if baddies_killed > wave_target_kills and baddies_onscreen == False and game_over == False:
                wave_break = 300
                wave_target_kills += 10
                game_wave += 1
                if game_wave == 10:
                    game_over = True
                    game_victory = True
                    game_over_timer = 700
                    win_sound.play()
                    
                baddies_killed = 0
                
                # Make the next round a bit harder :)
                if attack_max > 30:
                    attack_max -= 10
                if ufo_attack_max > 0:
                    ufo_attack_max -= 50
                if game_wave > 6:
                    baddie_fire_rate = 10
                wave_sound.play()

        # Show the newly rendered screen                
        pygame.display.flip()
        # Limit game speed
        clock.tick(FPS)
        
    # This is not strictly needed, but is included so that IDLE will play nice :)
    pygame.quit()
