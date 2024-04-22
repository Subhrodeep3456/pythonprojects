#Space Dodge
#Steps involved 
#1. Creating window
#2. add bg image 
#3. Moving character
#4. Adding player boundaries
#5. Keep track of time
#6. Render text
#7. add projectiles
#8. Moving projectile and collision
#9. Drawing projectiles
#10. Lost game text

import pygame 
import time 
import random 
pygame.font.init() #initialise font (pygame req)


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0,0)) #Special function to draw surfaces
    
    time_text = FONT.render(f"TIme : {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10,10))
    
    pygame.draw.rect(WIN, "red", player) #drawing
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    
    pygame.display.update() #applies

def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) 
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000 #projectiles
    star_count = 0
    
    stars = []
    hit = False
    
    while run: #while run is true (keypresses and stuff)
        star_count += clock.tick(60) #60 fps
        elapsed_time = time.time() - start_time #No of seconds since game starts
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x  = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
                
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Corner X button or collision
                run = False
                break
        
        keys = pygame.key.get_pressed() #user inputted keys
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0 : #LEft arrow key (K_LEFT)
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL 
            
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
            
        
        if hit:
            lost_text = FONT.render("You Lost", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000) #4 seconds
            break

        
        draw(player, elapsed_time, stars) #function called
            
    pygame.quit() #Quits pygame
    

if __name__ == "__main__": #directly running file instead of importing
    main()











