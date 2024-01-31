# Import Pygame and OS modules.
import pygame
import os

# Initialize Pygame module.
pygame.init()

# Set the Screen width and height.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Set up the Game Window.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Rename the Game Window.
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75

#define player action variables
moving_left = False    # Movement Left Flag.
moving_right = False	# Movement Right Flag.
shoot = False 			# Shoot Flag.

# Loading the Bullet image.
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()


#define colours
BG = (0, 0, 0)
RED = (255, 0, 0)


# Function to draw the Background.
def draw_bg():
	screen.fill(BG)
	# Drawing a Line.
	# line(surface, color, start_pos(x,y), end_pos(x,y)).
	pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


# Class for Soldier.
# pygame.sprite.Sprite --> Simple base class for visible game objects.
class Soldier(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed, ammo):
		pygame.sprite.Sprite.__init__(self)
		# Use for check Player is alive or not.
		self.alive = True
		# Use select the Sprite. Enemy or Player.
		self.char_type = char_type
		# Use for set the Soldier movement speed.
		self.speed = speed
		# Use for count Bullets/Ammo.
		self.ammo = ammo
		self.start_ammo = ammo
		# Use to set the timegap from one Bullet to another.
		self.shoot_cooldown = 0
		# Use for check Soldier's health.
		self.health = 100
		# Maximum health of the Soldier.
		self.max_health = self.health
		# Use for detecting Soldier's direction.
		self.direction = 1
		# Use for calculate the velocity of Y axis.abs
		self.vel_y = 0
		# Jump Flag.
		self.jump = False
		# Flag for check Soldier in the Air or not.
		self.in_air = True
		# Flag for detecting image is flipped or not.
		self.flip = False
		# List to store Soldier actions and their animations.
		self.animation_list = []
		# Use to check number of frames/images in an action/animation.
		self.frame_index = 0
		# Use to check/select the action.
		self.action = 0
		# Use to update the game clock.
		self.update_time = pygame.time.get_ticks()
		
		# Define different animation types for the player character
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		# Loop through each animation type.
		for animation in animation_types:
			# Create an empty list to store the frames of the current animation.
			temp_list = []
			# Count the number of frames in the current animation folder.
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			# Loop through each frame in the current animation.
			for i in range(num_of_frames):
				# Load the image for the current frame and convert it to alpha format.
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
				# Scale the image based on the provided scale factor.
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				# Add the scaled image to the temporary list.
				temp_list.append(img)
			# Add the list of frames for the current animation to the player's animation list.
			self.animation_list.append(temp_list)
		# Set the initial image for the player to the first frame of the first animation.
		self.image = self.animation_list[self.action][self.frame_index]
		# Create a rectangle to represent the player's position on the screen based on the current image.
		self.rect = self.image.get_rect()
		# Set the center of the rectangle to the specified initial position (x, y).
		self.rect.center = (x, y)

	# Define a method to update the player character.
	def update(self):
		# Call the method to update the player's animation.
		self.update_animation()
		# Call the method to check if the player is still alive.
		self.check_alive()
		# Update the shooting cooldown
    	# If the cooldown is greater than 0, decrement it
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1


	def move(self, moving_left, moving_right):
		#reset movement variables
		dx = 0
		dy = 0

		# Assign movement variables if moving left or right.
		# dx is the change in the x-coordinate (horizontal movement).
		# dy is the change in the y-coordinate (vertical movement).
		
		# Check if the player is moving left
		if moving_left:
			# Set dx to a negative value to move the player to the left.
			dx = -self.speed
			# Set the flip attribute to True to flip the player's image horizontally (facing left).
			self.flip = True
			# Set the direction attribute to -1 to indicate the player is moving left.
			self.direction = -1
		
		# Check if the player is moving right
		if moving_right:
			# Set dx to a positive value to move the player to the right.
			dx = self.speed
			# Set the flip attribute to False to keep the player's image unflipped (facing right).
			self.flip = False
			# Set the direction attribute to 1 to indicate the player is moving right.
			self.direction = 1

		#jump
		# Check if the player is initiating a jump and is not already in the air.
		if self.jump == True and self.in_air == False:
			# Set the vertical velocity (self.vel_y) to a negative value to move upward.
			self.vel_y = -13
			# Reset the jump flag to prevent continuous jumping.
			self.jump = False
			# Set the in_air flag to True to indicate that the player is now in the air.
			self.in_air = True

		# Apply gravity to the vertical velocity
		self.vel_y += GRAVITY
		# Ensure the vertical velocity does not exceed a certain limit.
		if self.vel_y > 10:
			self.vel_y
		# Update the vertical position (dy) based on the vertical velocity.
		dy += self.vel_y

		# Check collision with the floor.
		if self.rect.bottom + dy > 300:
			# Adjust dy to prevent the player from going below the floor.
			dy = 300 - self.rect.bottom
			# Reset the in_air flag to False, indicating that the player is on the floor.
			self.in_air = False

		# Update the horizontal and vertical positions of the player's rectangle.
		self.rect.x += dx
		self.rect.y += dy

	# Define a method to handle shooting.
	def shoot(self):
		# Check if the shooting cooldown is zero and there is available ammo.
		if self.shoot_cooldown == 0 and self.ammo > 0:
			# Set the shooting cooldown to 20 frames.
			self.shoot_cooldown = 20
			# Calculate the initial position of the bullet.
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			# Add the bullet to the bullet group.
			bullet_group.add(bullet)
			#reduce ammo.
			self.ammo -= 1

	# Define a method to update the player character's animation.
	def update_animation(self):
		# Set the cooldown period for updating the animation (in milliseconds).
		ANIMATION_COOLDOWN = 100
		# Update the player's image based on the current frame of the current action.
		self.image = self.animation_list[self.action][self.frame_index]
		# Check if enough time has passed since the last update.
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			# Record the current time for the next update comparison.
			self.update_time = pygame.time.get_ticks()
			# Increment the frame index to display the next frame in the animation.
			self.frame_index += 1
		# Check if the animation has reached the end; if so, reset back to the start.
		if self.frame_index >= len(self.animation_list[self.action]):
			# Special case for the 'Death' animation to stay on the last frame.
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				# Reset the frame index to the beginning of the animation
				self.frame_index = 0

	# Define a method to update the player character's action.
	def update_action(self, new_action):
		# Check if the new action is different from the previous one.
		if new_action != self.action:
			# Set the player's current action to the new action.
			self.action = new_action
			# Reset the frame index to the beginning of the animation.
			self.frame_index = 0
			# Update the time of the last animation update to the current time.
			self.update_time = pygame.time.get_ticks()


	# Define a method to check if the player character is alive.
	def check_alive(self):
		# Check if the player's health has fallen to zero or below.
		if self.health <= 0:
			# Set the player's health to zero to ensure it doesn't go below.
			self.health = 0
			# Set the player's speed to zero, effectively stopping movement.
			self.speed = 0
			# Set the alive flag to False, indicating that the player is no longer alive.
			self.alive = False
			# Update the player's action to the 'Death' animation.
			self.update_action(3)

	# Define a method to draw the player character on the screen.
	def draw(self):
		# Use the blit method to draw the player's image on the screen
    	# pygame.transform.flip is used to flip the image horizontally if self.flip is True
    	# The image is drawn at the position defined by self.rect.
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Define a class for the Bullets in the game.
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		# Call the constructor of the parent class (pygame.sprite.Sprite).
		pygame.sprite.Sprite.__init__(self)
		self.Bvel_y = 0
		# Set the speed of the Bullet.
		self.speed = 10
		# Set the image of the Bullet to a predefined Bullet image (bullet_img).
		self.image = bullet_img
		# Get the rectangular bounding box of the Bullet image.
		self.rect = self.image.get_rect()
		# Set the center of the Bullet's rectangle to the specified (x, y) coordinates.
		self.rect.center = (x, y)
		# Set the direction in which the Bullet is moving (either -1 for left or 1 for right).
		self.direction = direction

	# Define a method to update the state of the Bullet.
	def update(self):
		# Move the Bullet horizontally based on its direction and speed.
		self.rect.x += (self.direction * self.speed)
		# Check if the Bullet has gone off the screen.
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		# Check for collision with the Player and apply damage if the Player is alive.
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				# Reduce the Player's health by 5 on collision with the Bullet.
				player.health -= 5
				# Remove the Bullet from the Sprite group.
				self.kill()
		# Check for collision with the Enemy and apply damage if the Enemy is alive.
		if pygame.sprite.spritecollide(enemy, bullet_group, False):
			if enemy.alive:
				enemy.health -= 25
				self.kill()

#create sprite groups
bullet_group = pygame.sprite.Group()


# Create an instance of the Soldier class representing the Player and Enemy characters.
player = Soldier('player', 200, 200, 3, 5, 20)
enemy = Soldier('enemy', 700, 245, 3, 5, 20)


# Setting the Game Loop varibale to true.
run = True
# Game loop: runs as long as 'run' is True
while run:
	# Cap the frame rate by waiting to achieve the desired Frames Per Second (FPS).
	clock.tick(FPS)
	# Draw the background of the Game.
	draw_bg()
	# Update and draw the Player character.
	player.update()
	player.draw()
	# Update and draw the Enemy character.
	enemy.update()
	enemy.draw()

	# Update and draw the Bullet group (contains all active Bullets).
	bullet_group.update()
	bullet_group.draw(screen)

	# Update player actions if the Player is alive.
	if player.alive:
		# Shoot Bullets if the 'shoot' flag is True
		if shoot:
			player.shoot()
		# Check if the Player is in the air
		if player.in_air:
			# Update the player action to 'jump' (action code 2)
			player.update_action(2)
		# If the Player is not in the air, check movement.
		elif moving_left or moving_right:
			# Update the Player action to 'run' (action code 1) if moving.
			player.update_action(1)
		else:
			# If not moving, update the Player action to 'idle' (action code 0).
			player.update_action(0)
		# Move the Player based on the input (moving_left, moving_right).
		player.move(moving_left, moving_right)

	# Check and handle events in the Pygame event queue.
	for event in pygame.event.get():
		# Quit the Game if the Window close button is clicked.
		if event.type == pygame.QUIT:
			run = False
		# Handle keyboard key presses
		if event.type == pygame.KEYDOWN:
			# Set the 'moving_left' flag to True when the 'a' key is pressed.
			if event.key == pygame.K_a:
				moving_left = True
			# Set the 'moving_right' flag to True when the 'd' key is pressed.
			if event.key == pygame.K_d:
				moving_right = True
			# Set the 'shoot' flag to True when the spacebar is pressed.
			if event.key == pygame.K_SPACE:
				shoot = True
			# Trigger a jump if the 'w' key is pressed and the player is alive.
			if event.key == pygame.K_w and player.alive:
				player.jump = True
			# Quit the Game if the 'Escape' key is pressed.
			if event.key == pygame.K_ESCAPE:
				run = False


		# Handle keyboard key releases.
		if event.type == pygame.KEYUP:
			# Set the 'moving_left' flag to False when the 'a' key is released.
			if event.key == pygame.K_a:
				moving_left = False
			# Set the 'moving_right' flag to False when the 'd' key is released.
			if event.key == pygame.K_d:
				moving_right = False
			# Set the 'shoot' flag to False when the spacebar is released.
			if event.key == pygame.K_SPACE:
				shoot = False

	# Update the Display to show the latest changes.
	pygame.display.update()
# Quit the Pygame module and close the Game Window.
pygame.quit()