import pygame
import random
import os
from fuelBall import FuelBall
from player import Player
from enemy import Enemy
from explosion import Explosion
from fuel import Fuel

# Initialize pygame
pygame.init()

# Set up the font for the score
font = pygame.font.SysFont('comicsansms', 36)

# Set up the starting time and score
start_time = pygame.time.get_ticks()
score = 0

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
FONT_COLOR = (255, 255, 255)
# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Traffic Rider")

# Set up the clock
clock = pygame.time.Clock()

# Set up the background
background = pygame.image.load("assets/road.png").convert()
background_height = background.get_rect().height
background_y1 = 0
background_y2 = -background_height


# Set up the groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Set up the player
player = Player()
all_sprites.add(player)

# Set up the game loop
running = True
road_movement = 5
# init fuel
fuel = Fuel(660, 320)
all_sprites.add(fuel)

# create a sprite group for the fuel balls
fuel_balls = pygame.sprite.Group()



def score_function(time):
    # Calculate the score based on the time passed
    score = int(time * 10)
    return score

# check for collisions between the player and the fuel balls


def check_collisions(player, fuel_balls):
    for fuel_ball in fuel_balls:
        if pygame.sprite.collide_rect(player, fuel_ball):
            fuel_balls.remove(fuel_ball)
            fuel += player.max_fuel * 0.1
            if player.fuel > player.max_fuel:
                player.fuel = player.max_fuel

# spawn a fuel ball at a random position on the road


def spawn_fuel_ball():
    # get the y position of the enemy closest to the bottom of the screen
    closest_enemy = min(enemies, key=lambda enemy: enemy.rect.y)
    enemy_y = closest_enemy.rect.y + closest_enemy.rect.height
    
    # create a fuel ball with a random x position and the y position of the enemy
    x = random.randint(160, 510)
    fuel_ball = FuelBall(x, -32)
    fuel_balls.add(fuel_ball)

MENU_OPTIONS = ["Start Game", "Close Game"]
MENU_X = WINDOW_WIDTH // 2
MENU_Y = WINDOW_HEIGHT // 2
MENU_SPACING = 50

def draw_menu():
    for i, option in enumerate(MENU_OPTIONS):
        text = font.render(option, True, (255, 255, 255))
        text_rect = text.get_rect(center=(MENU_X, MENU_Y + i * MENU_SPACING))
        screen.blit(text, text_rect)

# Function to read the record file and return the results as a string
def read_record():
    if os.path.exists("record.txt"):
        with open("record.txt", "r") as f:
            record = f.read()
    else:
        record = "No record found"
    return record


# call spawn_fuel_ball every 500 milliseconds
pygame.time.set_timer(pygame.USEREVENT+1, 500)
gamestate = "MENU"


while running:
    if gamestate == "MENU":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a menu option was clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, option in enumerate(MENU_OPTIONS):
                    text_rect = font.render(option, True, (255, 255, 255)).get_rect(center=(MENU_X, MENU_Y + i * MENU_SPACING))
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        # Call the corresponding function
                        if option == "Start Game":
                            print("start game")
                            gamestate = "GAME"
                        elif option == "Close Game":
                            pygame.quit()
        screen.fill((0, 0, 0))
        draw_menu()
        pygame.display.flip()
    elif gamestate == "GAME":
    # Handle events
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT+1:
                spawn_fuel_ball()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed < 0:
                    player.stop()
                elif event.key == pygame.K_RIGHT and player.speed > 0:
                    player.stop()
        # Spawn enemies
        if len(enemies) < 4:
            x = random.randrange(150, 525)
            topOrNot = random.randrange(1, 2)
            speed = random.randrange(2, 6)
            y = -32
            if x > 340:
                speed *= -1
                speed -= road_movement
                y = 732
            elif x < 335:
                speed += road_movement

            enemy = Enemy(x, y, speed)

            if pygame.sprite.spritecollide(enemy, enemies, False):
                if y > 0:
                    enemy.rect.y += 32
                else:
                    enemy.rect.y -= 32

            all_sprites.add(enemy)
            enemies.add(enemy)

        # calculate score
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
        print('working')
        score = int(score_function(elapsed_time))
        # Update sprites
        player.update()
        fuel.update(300)
        for enemy in enemies:
            enemy.update(enemies)

        # Check for collisions
        if pygame.sprite.spritecollide(player, enemies, False):
            explosion = Explosion(player.rect.centerx - 16,
                            player.rect.centery - 16)
            explosion.update()
            explosion.draw(screen)
            gamestate = "MENU"
            for enemy in enemies:
                enemy.kill()
            fuel.refill(100)    
            enemies.empty()
            fuel_balls.empty()
            # Save the record
            with open("record.txt", "a") as f:
                f.write(str(score) + "\n")
        for fuel_ball in fuel_balls:
            if pygame.sprite.collide_rect(player, fuel_ball):
                fuel_balls.remove(fuel_ball)
                fuel.refill(40)

        if fuel.is_empty:
            explosion.draw(screen)
            gamestate = "MENU"
            for enemy in enemies:
                enemy.kill()
            fuel.refill(100)
            enemies.empty()
            fuel_balls.empty()
            # Save the record
            with open("record.txt", "a") as f:
                f.write(str(score) + "\n")
    # Scroll the background down
        background_y1 += road_movement
        background_y2 += road_movement
        if background_y1 >= background_height:
            background_y1 = -background_height + 10
        if background_y2 >= background_height:
            background_y2 = -background_height + 10

        # Draw background and sprites
        screen.fill((0, 0, 0))
        screen.blit(background, (0, background_y1))
        screen.blit(background, (0, background_y2))
        score_surface = font.render('Score: ' + str(score), True, (255, 255, 255))
        screen.blit(score_surface, (screen.get_width() -
                    score_surface.get_width() - 10, 10))
        all_sprites.draw(screen)

        # in the game loop, update and draw the fuel balls
        fuel_balls.update(road_movement)
        fuel_balls.draw(screen)

        # Update the display
        pygame.display.flip()

        # Set the FPS
        clock.tick(60)

# Quit pygame
pygame.quit()
