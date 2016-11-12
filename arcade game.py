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
width = 500
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# List containing all sprites in the program to draw them
all_sprites_list = pygame.sprite.Group()

# Define wall
class Wall(pygame.sprite.Sprite):
    #initialises parameters of a wall
    def __init__(self, corner_x, corner_y, width, height, color):
        super().__init__() #inherits all parameters of a sprite
        self.width = width
        self.height = height
        self.color = color
        #set the image of the wall
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect() #finds the rectangle object that has the dimensions of the image
        self.rect.x = corner_x
        self.rect.y = corner_y
    #draws a wall
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])

#this is the list of all walls in the game
wall_list = pygame.sprite.Group()

# Parameters of the map
widthofwalls = 20
heightofwalls = 20
colorofwalls = RED

# Function for adding the map from a given string
def adding_map(mapdescription, heightofwalls, widthofwalls, colorofwalls):
    # For each row, starting from 0
    current_row = 0
    for each_string in mapdescription:
        # For each column
        for i in range(0, len(each_string)):
            # Letter W means wall
            if each_string[i] == "W":
                newWall = Wall(i*widthofwalls, current_row*heightofwalls, widthofwalls, heightofwalls, colorofwalls)
                wall_list.add(newWall)
                all_sprites_list.add(newWall)
        current_row += 1                

# Declaration of the maze
basicmap = ["WWWWWWWWWWWWWWWWWWWWWWWWW",
            "W           W           W",
            "W WWW WWWWW W WWWWW WWW W",
            "W WWW WWWWW W WWWWW WWW W",
            "W                       W",
            "W WWW W WWWWWWWWW W WWW W",
            "W     W     W     W     W",
            "WWWWW WWWWW W WWWWW WWWWW",
            "    W W           W W    ",
            "WWWWW W WWWWWWWWW W WWWWW",
            "        W       W        ",
            "WWWWW W WWWWWWWWW W WWWWW",
            "    W W           W W    ",
            "WWWWW W WWWWWWWWW W WWWWW",
            "W           W           W",
            "W WWW WWWWW W WWWWW WWW W",
            "W   W               W   W",
            "WWW W W WWWWWWWWW W W WWW",
            "W     W     W     W     W",
            "W WWWWWWWWW W WWWWWWWWW W",
            "W                       W",
            "WWWWWWWWWWWWWWWWWWWWWWWWW"]
adding_map(basicmap, heightofwalls, widthofwalls, colorofwalls)

# Define moving object
class moving_object(pygame.sprite.Sprite):
    
    #initialises theobject
    def __init__(self, speed, direction, height, width, color):
        super().__init__()
        self.speed = speed
        self.direction = direction
        self.height = height
        self.width = width
        self.color = color
        #set the image of Pacman
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # fetches the rectangle in which the image is enclosed
        self.rect = self.image.get_rect()

    #moves the object
    def move(self):
        #moves upwards
        if self.direction == 1:
            self.rect.y -= self.speed
        #moves right
        if self.direction == 2:
            self.rect.x += self.speed
        #moves down
        if self.direction == 3:
            self.rect.y += self.speed
        #moves left
        if self.direction == 4:
            self.rect.x -= self.speed
    
    #allows the direction of movement to be changed
    def new_direction(self, newdirection):
        self.direction = newdirection
    
    #returns direction
    def get_direction(self):
        return self.direction
    
    #returns speed
    def get_speed(self):
        return self.speed
    
    #returns coordinates
    def get_coordinates(self):
        return (self.rect.x, self.rect.y)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])
        
#class Pacman(moving_object):
    
    #def __init__(self):
        #inherits from moving object
        #moving_object.__init__(self)
        
#initialise variables
initxPac = 20
inityPac = 20
initspeedPac = 1
initdirectionPac=2
heightPac = 20
widthPac = 20
colorPac = BLACK

Pacman = moving_object(initspeedPac, initdirectionPac, widthPac, heightPac, colorPac)
Pacman.rect.x = initxPac
Pacman.rect.y = inityPac

# Will be used for implementing changing direction as it is in original Pacman
Pacmanexampleforcollisions = Pacman
# Two direction indicators, one for the current, one for the one that is to be the next one
currentdirection = 1
newdirection = None

all_sprites_list.add(Pacman)
# -------- Main Program Loop -----------
while not done:

    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    

    #user pressed down on a key
        elif event.type == pygame.KEYDOWN:

            #find if it was an arrow and adjust the next direction accordingly
            # Pacman now moves right
            if event.key == pygame.K_RIGHT:
                newdirection = 2
            # Pacman now moves up
            if event.key == pygame.K_UP:
                newdirection = 1
            # Pacman now moves down
            if event.key == pygame.K_DOWN:
                newdirection = 3
            # Pacman now moves left
            if event.key == pygame.K_LEFT:
                newdirection = 4
        # This is changing the direction of movement of 'trial' Pacman
        Pacmanexampleforcollisions.new_direction(newdirection)
        
    # --- Game logic should go here

    #Pacman moves every step in the game
    
    # Checks the new position of Pacman
    Pacmanexampleforcollisions.move()
    # If it is such that there would be a collision, moves Pacman back
    if pygame.sprite.spritecollide(Pacmanexampleforcollisions, wall_list, False):
        Pacman.move()
        Pacmanexampleforcollisions.new_direction(currentdirection)
    else:
        if Pacman.get_direction() == 3:
            Pacman.new_direction(1)
            Pacman.move()
            Pacman.new_direction(3)
        if Pacman.get_direction() == 1:
            Pacman.new_direction(3)
            Pacman.move()
            Pacman.new_direction(1)
        if Pacman.get_direction() == 2:
            Pacman.new_direction(4)
            Pacman.move()
            Pacman.new_direction(2)
        if Pacman.get_direction() == 4:
            Pacman.new_direction(2)
            Pacman.move()
            Pacman.new_direction(4)
    
    # screen cleared to white
    screen.fill(WHITE)
 
    # --- Drawing
    all_sprites_list.draw(screen)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
