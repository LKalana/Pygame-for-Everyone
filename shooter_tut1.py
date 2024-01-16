# Import the pygame library
import pygame

# Initialize pygame
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window caption
pygame.display.set_caption('Shooter')

# Define the Soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the soldier image
        img = pygame.image.load('img/player/Idle/0.png')
        # Scale the image
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        # Get the rectangle bounding the image
        self.rect = self.image.get_rect()
        # Set the initial position of the soldier
        self.rect.center = (x, y)

    def draw(self):
        # Draw the soldier on the screen
        screen.blit(self.image, self.rect)

# Create two instances of the Soldier class
player = Soldier(200, 200, 3)
player2 = Soldier(400, 200, 3)

# Run the game loop
run = True
while run:
    # Draw the players on the screen
    player.draw()
    player2.draw()

    # Check for events
    for event in pygame.event.get():
        # Quit the game if the window is closed
        if event.type == pygame.QUIT:
            run = False

    # Update the display
    pygame.display.update()

# Quit pygame when the game loop exits
pygame.quit()
