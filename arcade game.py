#import library called pygame
import pygame
#initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
width = 700
height = 500
size = (width, height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#initialise variables

# Define wall
class Wall(object):
    def __init__(self, corner_x, corner_y, width, height, color):
        self.corner_x=corner_x
        self.corner_y=corner_y
        self.width=width
        self.height=height
        self.color=color
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.corner_x, self.corner_y, self.width, self.height])

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here

    # screen cleared to white
    screen.fill(WHITE)
 
    # --- Drawing

    wallblockingmovement=Wall(0, 0, 10, 10, RED)
    wallblockingmovement.draw()
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
