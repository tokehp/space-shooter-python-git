# Arcade-style space shooter inspired by Galaga and Spacer Invaders.
# Made for the purpose of teaching git version control to beginners.

import pygame as pg
import random as r


### Setup ###
pg.init()
clock = pg.time.Clock()

screen = pg.display.set_mode((2000,1000))
pg.display.set_caption("Space Shooter")

# Spaceship character
ship_images = []
for i in range(3):
    img = pg.image.load(f"images/ship_{i}.png")
    ship_images.append(img)
ship_x = 1000 
ship_y = 900
ship_w = ship_images[0].get_rect().size[0]
ship_h = ship_images[0].get_rect().size[1]

# Alien character
alien_images = []
for i in range(2):
    img = pg.image.load(f"images/alien_{i}.png")
    alien_images.append(img)

aliens = []
for i in range(20):
        for _ in range(3):
            n = r.randint(0,40)
            alien1 = {'x': n*50 , 'y': i*-20}
            aliens.append(alien1)

alien_w = alien_images[0].get_rect().size[0]
alien_h = alien_images[0].get_rect().size[1]

# Projectiles 
space_pressed = False
projectiles = []
projectile_w = 12
projectile_h = 16
bullets = 0

# Keypress status
left_pressed = False
right_pressed = False

# Sound: weapon / laser 
# https://sfxr.me/#34T6Pm25W5VunHtL14gUxhLx6MqNduzaeRPcUbqtT4RN55w6nP9NipaUrx5ZBBvohWwXgMrd5BS2e7HwRwEVyzmKM3FV8LiU7Gh5ob2VvvMi6ftqdhbVB54ZM 
sound_laser = pg.mixer.Sound("sounds/laser.wav")

# Font for scoreboard
# https://fonts.google.com/specimen/Press+Start+2P/about
font_scoreboard = pg.font.Font("fonts/PressStart2P-Regular.ttf", 20)


### Game loop ###
running = True
tick = 0
score = 0
while running:

    ## Event loop  (handle keypresses etc.) ##
    events = pg.event.get()
    for event in events:

        # Close window (pressing [x], Alt+F4 etc.)
        if event.type == pg.QUIT:
            running = False
        
        # Keypresses
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                running = False

            elif event.key == pg.K_LEFT:
                left_pressed = True

            elif event.key == pg.K_RIGHT:
                right_pressed = True

            elif event.key == pg.K_SPACE:
                space_pressed = True

        # Keyreleases
        elif event.type == pg.KEYUP:

            if event.key == pg.K_LEFT:
                left_pressed = False 

            elif event.key == pg.K_RIGHT:
                right_pressed = False 

            elif event.key == pg.K_SPACE:
                space_pressed = False
    

    ## Updating (movement, collisions, etc.) ##

    # Alien
    for alien in aliens:
        alien['y'] += 1

    # Spaceship
    if left_pressed:
        ship_x -= 16

    if right_pressed:
        ship_x += 16

    # Projectile movement
    # Reverse iteration needed to handle each projectile correctly
    # in cases where a projectile is removed.
    for projectile in reversed(projectiles):
        projectile['y'] -= 16 

        # Remove projectiles leavning the top of the screen
        if projectile['y'] < 0:
            bullets -= 1
            projectiles.remove(projectile)

    # Alien / projectile collision 
    # Test each projectile against each alien
    for projectile in reversed(projectiles):
        projectile_count = 0
        for alien in aliens:

            # Horizontal (x) overlap
            if (alien['x'] < projectile['x'] + projectile_w and 
                projectile['x'] < alien['x']+alien_w):
                
                # Vertical (y) overlap 
                if (projectile['y'] < alien['y'] + alien_h and 
                    alien['y'] < projectile['y'] + projectile_h):
                    
                    # Alien is hit
                    projectiles.remove(projectile)
                    alien["y"] -= 400
                    score += 1
                    break
                    # No further aliens can be hit by this projectile 
                    # so skip to the next projectile 
                    

    # Firing (spawning new projectiles)
    if space_pressed and bullets <= 2:
        bullets += 2
        sound_laser.play()

        projectile = {'x': ship_x + ship_w/2 - projectile_w/2, 
                      'y': ship_y}
        projectiles.append(projectile)


    ## Drawing ##
    screen.fill((0,0,0)) 

    # 3 images --> tick % 3
    # 100% animation speed: tick % 3
    # 25% animation speed: int(tick/4) % 3
    r = int(tick/4) % 3 
    screen.blit(ship_images[r], (ship_x, ship_y))

    # Alien
    r = int(tick/8) % 2
    for alien in aliens:
        screen.blit(alien_images[r], (alien['x'], alien['y']))

    # Projectiles
    for projectile in projectiles:
        rect = (projectile['x'], projectile['y'], projectile_w, projectile_h)
        pg.draw.rect(screen, (255, 0, 0), rect) 

    # Scoreboard
    text = font_scoreboard.render(f"{score:04d}", True, (255,255,255))
    screen.blit(text, (10,560))

    # Update window with newly drawn pixels
    pg.display.flip()

    # Limit/fix frame rate (fps)
    clock.tick(60)
    tick += 1