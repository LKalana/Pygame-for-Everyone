import pygame  # Import the pygame module
import os  # Import the os module

pygame.init()  # Initialize pygame

SCREEN_WIDTH = 800  # Define the screen width
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)  # Define the screen height based on the width

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the display mode
pygame.display.set_caption('Shooter')  # Set the window caption

clock = pygame.time.Clock()  # Create a pygame Clock object
FPS = 60  # Define the frames per second

GRAVITY = 0.75  # Define the gravity constant

moving_left = False  # Initialize a variable to control left movement
moving_right = False  # Initialize a variable to control right movement
shoot = False  # Initialize a variable to control shooting
grenade = False  # Initialize a variable to control grenade throwing
grenade_thrown = False  # Initialize a variable to track whether a grenade has been thrown

bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()  # Load the bullet image
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()  # Load the grenade image

BG = (144, 201, 120)  # Define the background color
RED = (255, 0, 0)  # Define the color red

def draw_bg():  # Define a function to draw the background
    screen.fill(BG)  # Fill the screen with the background color
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))  # Draw a red line on the screen

class Soldier(pygame.sprite.Sprite):  # Define a Soldier class
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):  # Constructor method
        pygame.sprite.Sprite.__init__(self)  # Call the superclass constructor
        self.alive = True  # Initialize a variable to track if the soldier is alive
        self.char_type = char_type  # Set the character type
        self.speed = speed  # Set the speed of the soldier
        self.ammo = ammo  # Set the ammo count
        self.start_ammo = ammo  # Set the starting ammo count
        self.shoot_cooldown = 0  # Initialize the shoot cooldown
        self.grenades = grenades  # Set the grenade count
        self.health = 100  # Set the health of the soldier
        self.max_health = self.health  # Set the maximum health
        self.direction = 1  # Set the direction of the soldier
        self.vel_y = 0  # Initialize the vertical velocity
        self.jump = False  # Initialize a variable to control jumping
        self.in_air = True  # Initialize a variable to track if the soldier is in the air
        self.flip = False  # Initialize a variable to control flipping
        self.animation_list = []  # Initialize a list to store animations
        self.frame_index = 0  # Initialize the frame index
        self.action = 0  # Initialize the action
        self.update_time = pygame.time.get_ticks()  # Get the current time

        animation_types = ['Idle', 'Run', 'Jump', 'Death']  # Define animation types
        for animation in animation_types:  # Iterate over animation types
            temp_list = []  # Initialize a temporary list
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))  # Count the number of frames
            for i in range(num_of_frames):  # Iterate over frames
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()  # Load the image
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # Scale the image
                temp_list.append(img)  # Append the image to the temporary list
            self.animation_list.append(temp_list)  # Append the temporary list to the animation list

        self.image = self.animation_list[self.action][self.frame_index]  # Set the image
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (x, y)  # Set the center of the rectangle

    def update(self):  # Define a method to update the soldier
        self.update_animation()  # Update the animation
        self.check_alive()  # Check if the soldier is alive
        if self.shoot_cooldown > 0:  # If the shoot cooldown is greater than 0
            self.shoot_cooldown -= 1  # Decrease the shoot cooldown

    def move(self, moving_left, moving_right):  # Define a method to move the soldier
        dx = 0  # Initialize the change in x-coordinate
        dy = 0  # Initialize the change in y-coordinate

        if moving_left:  # If moving left
            dx = -self.speed  # Set the change in x-coordinate to the negative speed
            self.flip = True  # Set flip to True
            self.direction = -1  # Set the direction to -1
        if moving_right:  # If moving right
            dx = self.speed  # Set the change in x-coordinate to the speed
            self.flip = False  # Set flip to False
            self.direction = 1  # Set the direction to 1

        if self.jump == True and self.in_air == False:  # If jumping and not in air
            self.vel_y = -11  # Set the vertical velocity
            self.jump = False  # Set jump to False
            self.in_air = True  # Set in_air to True

        self.vel_y += GRAVITY  # Add gravity to the vertical velocity
        if self.vel_y > 10:  # If vertical velocity is greater than 10
            self.vel_y  # Keep the vertical velocity the same
        dy += self.vel_y  # Add the vertical velocity to the change in y-coordinate

        if self.rect.bottom + dy > 300:  # If the bottom of the rectangle plus dy is greater than 300
            dy = 300 - self.rect.bottom  # Set dy to 300 minus the bottom of the rectangle
            self.in_air = False  # Set in_air to False

        self.rect.x += dx  # Add dx to the x-coordinate of the rectangle
        self.rect.y += dy  # Add dy to the y-coordinate of the rectangle

    def shoot(self):  # Define a method to shoot
        if self.shoot_cooldown == 0 and self.ammo > 0:  # If shoot cooldown is 0 and there is ammo
            self.shoot_cooldown = 20  # Set the shoot cooldown
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)  # Create a bullet object
            bullet_group.add(bullet)  # Add the bullet to the bullet group
            self.ammo -= 1  # Decrease the ammo count

    def update_animation(self):  # Define a method to update the animation
        ANIMATION_COOLDOWN = 100  # Define the animation cooldown
        self.image = self.animation_list[self.action][self.frame_index]  # Set the image
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:  # If time elapsed is greater than animation cooldown
            self.update_time = pygame.time.get_ticks()  # Set the update time
            self.frame_index += 1  # Increase the frame index
        if self.frame_index >= len(self.animation_list[self.action]):  # If frame index is greater than or equal to the length of the animation list
            if self.action == 3:  # If action is death
                self.frame_index = len(self.animation_list[self.action]) - 1  # Set the frame index to the last frame
            else:  # Otherwise
                self.frame_index = 0  # Reset the frame index

    def update_action(self, new_action):  # Define a method to update the action
        if new_action != self.action:  # If the new action is different from the current action
            self.action = new_action  # Set the action to the new action
            self.frame_index = 0  # Reset the frame index
            self.update_time = pygame.time.get_ticks()  # Set the update time

    def check_alive(self):  # Define a method to check if the soldier is alive
        if self.health <= 0:  # If health is less than or equal to 0
            self.health = 0  # Set health to 0
            self.speed = 0  # Set speed to 0
            self.alive = False  # Set alive to False
            self.update_action(3)  # Update the action to death

    def draw(self):  # Define a method to draw the soldier
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)  # Blit the image onto the screen

class Bullet(pygame.sprite.Sprite):  # Define a Bullet class
    def __init__(self, x, y, direction):  # Constructor method
        pygame.sprite.Sprite.__init__(self)  # Call the superclass constructor
        self.speed = 10  # Set the speed of the bullet
        self.image = bullet_img  # Set the image of the bullet
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (x, y)  # Set the center of the rectangle
        self.direction = direction  # Set the direction of the bullet

    def update(self):  # Define a method to update the bullet
        self.rect.x += (self.direction * self.speed)  # Move the bullet horizontally
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:  # If the bullet goes off-screen
            self.kill()  # Remove the bullet

        if pygame.sprite.spritecollide(player, bullet_group, False):  # If the player is hit by a bullet
            if player.alive:  # If the player is alive
                player.health -= 5  # Decrease the player's health
                self.kill()  # Remove the bullet
        if pygame.sprite.spritecollide(enemy, bullet_group, False):  # If the enemy is hit by a bullet
            if enemy.alive:  # If the enemy is alive
                enemy.health -= 25  # Decrease the enemy's health
                self.kill()  # Remove the bullet

class Grenade(pygame.sprite.Sprite):  # Define a Grenade class
    def __init__(self, x, y, direction):  # Constructor method
        pygame.sprite.Sprite.__init__(self)  # Call the superclass constructor
        self.timer = 100  # Set the timer for the grenade
        self.vel_y = -11  # Set the vertical velocity of the grenade
        self.speed = 7  # Set the speed of the grenade
        self.image = grenade_img  # Set the image of the grenade
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.center = (x, y)  # Set the center of the rectangle
        self.direction = direction  # Set the direction of the grenade

    def update(self):  # Define a method to update the grenade
        self.vel_y += GRAVITY  # Add gravity to the vertical velocity
        dx = self.direction * self.speed  # Set the change in x-coordinate
        dy = self.vel_y  # Set the change in y-coordinate

        if self.rect.bottom + dy > 300:  # If the bottom of the rectangle plus dy is greater than 300
            dy = 300 - self.rect.bottom  # Set dy to 300 minus the bottom of the rectangle
            self.speed = 0  # Set the speed to 0

        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:  # If the left or right of the rectangle plus dx is out of bounds
            self.direction *= -1  # Reverse the direction
            dx = self.direction * self.speed  # Set the change in x-coordinate

        self.rect.x += dx  # Add dx to the x-coordinate of the rectangle
        self.rect.y += dy  # Add dy to the y-coordinate of the rectangle

bullet_group = pygame.sprite.Group()  # Create a group for bullets
grenade_group = pygame.sprite.Group()  # Create a group for grenades

player = Soldier('player', 200, 200, 3, 5, 20, 5)  # Create a player object
enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0)  # Create an enemy object

run = True  # Initialize the run variable
while run:  # Main game loop
    clock.tick(FPS)  # Limit the frame rate

    draw_bg()  # Draw the background

    player.update()  # Update the player
    player.draw()  # Draw the player

    enemy.update()  # Update the enemy
    enemy.draw()  # Draw the enemy

    bullet_group.update()  # Update the bullets
    grenade_group.update()  # Update the grenades
    bullet_group.draw(screen)  # Draw the bullets
    grenade_group.draw(screen)  # Draw the grenades

    if player.alive:  # If the player is alive
        if shoot:  # If shooting
            player.shoot()  # Player shoots
        elif grenade and grenade_thrown == False and player.grenades > 0:  # If throwing grenade
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)  # Create a grenade object
            grenade_group.add(grenade)  # Add the grenade to the grenade group
            player.grenades -= 1  # Decrease the grenade count
            grenade_thrown = True  # Set grenade_thrown to True
        if player.in_air:  # If the player is in the air
            player.update_action(2)  # Update the action to jumping
        elif moving_left or moving_right:  # If moving left or right
            player.update_action(1)  # Update the action to running
        else:  # Otherwise
            player.update_action(0)  # Update the action to idle
        player.move(moving_left, moving_right)  # Move the player

    for event in pygame.event.get():  # Event loop
        if event.type == pygame.QUIT:  # If quitting
            run = False  # Exit the loop
        if event.type == pygame.KEYDOWN:  # If a key is pressed
            if event.key == pygame.K_a:  # If the key is 'a'
                moving_left = True  # Set moving_left to True
            if event.key == pygame.K_d:  # If the key is 'd'
                moving_right = True  # Set moving_right to True
            if event.key == pygame.K_SPACE:  # If the key is space
                shoot = True  # Set shoot to True
            if event.key == pygame.K_q:  # If the key is 'q'
                grenade = True  # Set grenade to True
            if event.key == pygame.K_w and player.alive:  # If the key is 'w' and the player is alive
                player.jump = True  # Set jump to True
            if event.key == pygame.K_ESCAPE:  # If the key is escape
                run = False  # Exit the loop

        if event.type == pygame.KEYUP:  # If a key is released
            if event.key == pygame.K_a:  # If the key is 'a'
                moving_left = False  # Set moving_left to False
            if event.key == pygame.K_d:  # If the key is 'd'
                moving_right = False  # Set moving_right to False
            if event.key == pygame.K_SPACE:  # If the key is space
                shoot = False  # Set shoot to False
            if event.key == pygame.K_q:  # If the key is 'q'
                grenade = False  # Set grenade to False
                grenade_thrown = False  # Set grenade_thrown to False

    pygame.display.update()  # Update the display

pygame.quit()  # Quit pygame
