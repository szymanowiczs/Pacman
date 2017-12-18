# import library called pygame
import pygame
import random
import time
import math
# initialize the game engine
pygame.init()

# Seed the random numbers
random.seed()

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)
font_scores = pygame.font.SysFont("sans-serif", 30)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_SALMON = (255, 160, 122)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_CORAL = (240, 128, 128)

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

# Load the image of Pacman
PacmanImage = pygame.image.load("Pacman.png")

# Load the image of starting screen
StartingScreen = pygame.image.load("starting_screen.png")

# Load the image of the screen when the game is over
GameOverScreen = pygame.image.load("game_over.png")

# Load the image of the screen when the game is won
YouWonScreen = pygame.image.load("you_won.png")

# Define wall
class Wall(pygame.sprite.Sprite):
    # initialises parameters of a wall
    def __init__(self, corner_x, corner_y, width, height, color):
        super().__init__()  # inherits all parameters of a sprite
        self.width = width
        self.height = height
        self.color = color
        # set the image of the wall
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()  # finds the rectangle object that has the dimensions of the image
        self.rect.x = corner_x
        self.rect.y = corner_y


# Define coins to collect
class coin(pygame.sprite.Sprite):
    # initialses parameters of the coin
    def __init__(self, corner_x, corner_y, width, height, color):

        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        # set the image of the coin
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()  # finds the rectangle object that has the dimensions of the image
        self.rect.x = corner_x
        self.rect.y = corner_y

# this is the list of all walls in the game
wall_list = pygame.sprite.Group()
# this is the list of all coins in the game
coin_list = pygame.sprite.Group()
# this is the list of all enemies in the game
enemies_list = pygame.sprite.Group()

# Parameters of the map
widthofwalls = 20
heightofwalls = 20
colorofwalls = BLUE
colorofcoins = LIGHT_SALMON
heightofcoins = 4
widthofcoins = 4

# Function for adding the map from a given string
def adding_map(mapdescription, heightofwalls, widthofwalls, colorofwalls, colorofcoins):
    # For each row, starting from 0
    current_row = 0
    for each_string in mapdescription:
        # For each column
        for i in range(0, len(each_string)):
            # Letter W means wall
            if each_string[i] == "W":
                newWall = Wall(i * widthofwalls, current_row * heightofwalls, widthofwalls, heightofwalls, colorofwalls)
                wall_list.add(newWall)
                all_sprites_list.add(newWall)
            # A . means a coin
            elif each_string[i] == ".":
                x_coordinate = i * widthofwalls+(widthofwalls-widthofcoins)/2
                y_coordinate = current_row * heightofwalls+(heightofwalls-heightofcoins)/2
                newCoin = coin(x_coordinate, y_coordinate, widthofcoins, heightofcoins, colorofcoins)
                coin_list.add(newCoin)
                all_sprites_list.add(newCoin)
        current_row += 1

# Declaration of the maze


basicmap = ["WWWWWWWWWWWWWWWWWWWWWWWWW",
            "W...........W...........W",
            "W.WWW.WWWWW.W.WWWWW.WWW.W",
            "W.WWW.WWWWW.W.WWWWW.WWW.W",
            "W.......................W",
            "W.WWW.W.WWWWWWWWW.W.WWW.W",
            "W.....W.....W.....W.....W",
            "WWWWW.WWWWW.W.WWWWW.WWWWW",
            "    W.W...........W.W    ",
            "WWWWW.W.WWWWWWWWW.W.WWWWW",
            "........W       W........",
            "WWWWW.W.WWWWWWWWW.W.WWWWW",
            "    W.W...........W.W    ",
            "WWWWW.W.WWWWWWWWW.W.WWWWW",
            "W...........W...........W",
            "W.WWW.WWWWW.W.WWWWW.WWW.W",
            "W...W...............W...W",
            "WWW.W.W.WWWWWWWWW.W.W.WWW",
            "W.....W.....W.....W.....W",
            "W.WWWWWWWWW.W.WWWWWWWWW.W",
            "W.......................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWW"]

adding_map(basicmap, heightofwalls, widthofwalls, colorofwalls, colorofcoins)


# Define moving object
class moving_object(pygame.sprite.Sprite):
    # initialises theobject
    def __init__(self, speed, direction, height, width, color):
        super().__init__()
        self.speed = speed
        self.direction = direction
        self.height = height
        self.width = width
        self.color = color
        # set the image of Pacman
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # fetches the rectangle in which the image is enclosed
        self.rect = self.image.get_rect()

    # moves the object
    def move(self):
        # moves upwards
        if self.direction == 1:
            self.rect.y -= self.speed
        # moves right
        if self.direction == 2:
            self.rect.x += self.speed
            # Enables going through the tunnel
            self.rect.x = self.rect.x % width
        # moves down
        if self.direction == 3:
            self.rect.y += self.speed
        # moves left
        if self.direction == 4:
            self.rect.x -= self.speed
            # Enables going through the tunnel
            self.rect.x = self.rect.x % width

    # allows the direction of movement to be changed
    def new_direction(self, newdirection):
        self.direction = newdirection

    # returns direction
    def get_direction(self):
        return self.direction

    # returns speed
    def get_speed(self):
        return self.speed

    # returns coordinates
    def get_coordinates(self):
        return (self.rect.x, self.rect.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])

    # This function checks if Pacman would collide with a wall if it moved
    def wouldcollide(self, wall_list):
        self.move()
        if pygame.sprite.spritecollide(self, wall_list, False):
            return True
        else:
            return False

    # Moves Pacman in opposite direction
    def move_back(self):
        if self.get_direction() == 3:
            self.new_direction(1)
            self.move()
            self.new_direction(3)
        if self.get_direction() == 1:
            self.new_direction(3)
            self.move()
            self.new_direction(1)
        if self.get_direction() == 2:
            self.new_direction(4)
            self.move()
            self.new_direction(2)
        if self.get_direction() == 4:
            self.new_direction(2)
            self.move()
            self.new_direction(4)

    def moving_object_detecting_collisions(self, wall_list):
        # Checks what would happen if the object would be moved as intended
        self.move()
        # If there is a collision, moves the object back in the opposite direction
        # Object ends up in the same position as it was before the collision
        if pygame.sprite.spritecollide(self, wall_list, False):
            self.move_back()

    def signalfromkeyboard(self, event):
        # find if it was an arrow and adjust the next direction accordingly
        # Pacman now moves right
        if event.key == pygame.K_RIGHT:
            newdirection = 2
            self.new_direction(newdirection)
        # Pacman now moves up
        if event.key == pygame.K_UP:
            newdirection = 1
            self.new_direction(newdirection)
        # Pacman now moves down
        if event.key == pygame.K_DOWN:
            newdirection = 3
            self.new_direction(newdirection)
        # Pacman now moves left
        if event.key == pygame.K_LEFT:
            newdirection = 4
            self.new_direction(newdirection)

    # This function checks whether Pacman collects a coin
    def collectcoin(self, coin_list):
        if pygame.sprite.spritecollide(self, coin_list, True):
            return True
        else:
            return False

# Initial value of variables
initxPac = 240
inityPac = 320
initspeedPac = 2
initdirectionPac = 1
heightPac = 20
widthPac = 20
colorPac = YELLOW
pointspercoin = 1
score = 0
initxEnA = 20
inityEnA = 20
initspeed = 2
initdirectionEnA = 2
heightEn = heightPac
widthEn = widthPac
colorEn = colorPac
initxEnB = 460
inityEnB = 20
initdirectionEnB = 4
initxEnC = 460
inityEnC = 400
initdirectionEnC = 4
initxEnD = 20
inityEnD = 400
initdirectionEnD = 4
colorEnA = RED
colorEnB = CYAN
colorEnC = ORANGE
colorEnD = LIGHT_CORAL
available_lives = 2

# THIS PART IS ABOUT DFS AND GRAPHS

class node(object):
    # Has a name, x and y coordinates
    def __init__(self, name):
        self.name = name
    # Returns the name of the object
    def getName(self):
        return self.name
    # Returns the name of the object if print(node) is called
    def __str__(self):
        return self.name

class edge(object):
    # Initiates the object
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    # Returns the source edge
    def getSource(self):
        return self.src
    # Returns the destination edge
    def getDestination(self):
        return self.dest
    # Returns the weight of the edge
    def __str__(self):
        return str(self.src)+ '->' +str(self.dest)

# This edge is weighted
class weightedEdge(edge):
    # Overrides the constructor
    def __init__(self, src, dest, weight=1.0):
        super().__init__(src, dest)
        self.src = src
        self.dest = dest
        self.weight = weight
    # Retruns the weight
    def getWeight(self):
        return self.weight
    # Prints the edge
    def __str__(self):
        return str(self.src) + '->(' + str(self.weight) + ')' \
               + str(self.dest)

# Creates a directed graph
class Digraph(object):

    # Consists of a dictionary of edges and a set of nodes
    def __init__(self):
        # Contains all nodes, used to check node duplication
        self.nodes = set([])
        # Dictionary of dictionaries of edges coming out of a node
        self.edges = {}

    def addNode(self, node):
        # Checks if node is already in a graph
        if node in self.nodes:
            raise ValueError('Duplicate node')
        # If not adds node to the set of nodes and a list of edges for the node, initially empty
        else:
            # Node is added to the set
            self.nodes.add(node)
            # An empty dictionary of edges (to store their length) is added to that node in the dictionary
            self.edges[node] = {}

    def addEdge(self, weightededge):
        # Gets the source node of the edge
        src = weightededge.getSource()
        # Gets the destination node of the edge
        dest = weightededge.getDestination()
        # Gets the weight of the edge
        weight = weightededge.getWeight()
        # Checks if both of them are in the graph
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        # If they are, adds the destination node to the list of edges coming out of source edge
        #self.edges[src].append(dest)
        # The weight of the edge is stored as an element in the dictionary inside the dictionary
        self.edges[src][dest] = weight

    # Returns all nodes to which one can go from a given node
    def childrenOf(self, node):
        return self.edges[node]

    # Checks if a node is in a graph
    def hasNode(self, node):
        return node in self.nodes

    # Presents the graph as a string of all edges, with their sources and destinations
    def __str__(self):
        res = ''
        # For each node in the dictionary
        for k in self.edges:
            # For each edge print source, weight and destination
            for d in self.edges[k]:
                res = res + str(k) + '->(' + str(self.edges[k][d]) + ')' + str(d) + '\n'
        return res[:-1]

# Declares a subclass of a digraph - an undirected graph
class Graph(Digraph):
    # Overrides the function in the superclass
    def addEdge(self, weightededge):
        # Adds the edge to the graph
        Digraph.addEdge(self, weightededge)
        # Reverses the edge
        rev = weightedEdge(weightededge.getDestination(), weightededge.getSource(), weightededge.getWeight())
        # Adds the reverse edge
        Digraph.addEdge(self, rev)

# Function for getting the coordinates of the node from its name
def get_coordinates_from_name(node):
    ycoord = ""
    iterator = 0
    while node.getName()[iterator] != " ":
        # Gets y-coordinate, row number
        ycoord += str(node.getName()[iterator])
        iterator += 1
    # Makes it a number, rather than a string
    ycoord = int(ycoord)
    # Gets x-coordinate, column number, converts it to a string
    xcoord = int(node.getName()[(iterator + 1):])
    return (xcoord, ycoord)

# This is a function which creates a graph for a given string
def graphconstructor(mapdescription):
    mapGraph = Graph()
    # Goes through each row in the map
    for row in range(0, len(mapdescription)):
        # Goes through every field in that row
        for field in range(0, len(mapdescription[row])):
            # For every point which may be a node
            if mapdescription[row][field] == ".":
                # It needs to have a way down or up
                if mapdescription[row+1][field] == "." or mapdescription[row-1][field] == ".":
                    # And a way left or right
                    if mapdescription[row][field+1] == "." or mapdescription[row][field-1] == ".":
                        # Then it's a node
                        mapGraph.addNode(node(str(row)+" "+str(field)))

    # Now adds edges to the graph
    for eachNode in mapGraph.nodes:
        # First the vertical edges
        # Gets the coordinates of the node to use it
        ycoord = get_coordinates_from_name(eachNode)[1]
        xcoord = get_coordinates_from_name(eachNode)[0]
        # If there is space below to move then there must be a node somewhere below
        if mapdescription[ycoord+1][xcoord] == ".":
            # Will measure the weight of that edge
            distancecounter = 0
            found = False
            # Moves until it finds the node below
            while not found:
                # Changes the weight of the edge and moves down
                ycoord += 1
                distancecounter += 1
                # Checks if it is at a node
                for thatNode in mapGraph.nodes:
                    if thatNode.getName() == (str(ycoord) + " " + str(xcoord)):
                        found = True
                        # Adds the edge
                        mapGraph.addEdge(weightedEdge(eachNode, thatNode, distancecounter))

        # Now horizontal edge
        # Gets the coordinates of the node to use it
        ycoord = get_coordinates_from_name(eachNode)[1]
        xcoord = get_coordinates_from_name(eachNode)[0]
        # If there is space to move to the right then there must be a node somewhere to the right
        if mapdescription[ycoord][xcoord+1] == ".":
            # Will measure the weight of that edge
            distancecounter = 0
            # Moves until there is a junction on the right
            found = False
            # Moves until it finds the node below
            while not found:
                # Changes the weight of the edge and moves down
                xcoord += 1
                distancecounter += 1
                if xcoord == 25:
                    xcoord = 0
                # Checks if it is at a node
                for thatNode in mapGraph.nodes:
                    if thatNode.getName() == (str(ycoord) + " " + str(xcoord)):
                        found = True
                        # Adds the edge
                        mapGraph.addEdge(weightedEdge(eachNode, thatNode, distancecounter))
    return mapGraph

mapGraph = graphconstructor(basicmap)

# DFS
def DepthFirstSearch(start_node, goal_node, aGraph, path_stack, visited_nodes):
    # Adds the node to visited nodes
    visited_nodes.append(start_node)
    # If found, returns the path
    if start_node == goal_node:
        # After adding the current node to the path stack
        path_stack.append(start_node)
        return path_stack
    # Executes the algorithm on each child
    for child in aGraph.childrenOf(start_node).keys():
        # Does not traverse if already visited
        if child not in visited_nodes:
            # Appends the child and calls the algorithm recursively
            path_stack.append(start_node)
            p = DepthFirstSearch(child, goal_node, aGraph, path_stack, visited_nodes)
            if p:
                return p
    return ""

# This function checks if the coin is collected and increments score
def scorecounter(score, coin_list, Pacman, pointspercoin, all_sprites_list):
    if Pacman.collectcoin(coin_list):
        # Increments score
        score += pointspercoin
        # Delete the coin from the coin_list
        pygame.sprite.spritecollide(Pacman, coin_list, True)
        # Delete the coin from the list of all sprites so that it is not displayed
        pygame.sprite.spritecollide(Pacman, all_sprites_list, True)
        # Add Pacman to ensure it is displayed
        if Pacman not in all_sprites_list:
            all_sprites_list.add(Pacman)
    return (score, coin_list, all_sprites_list)

# Function for updating the list of top 10 scores
def newhighscores(highscorelist, newscore):
    for i in range(0, len(highscorelist)):
        # Checks if the new score is bigger
        if highscorelist[i] < newscore:
            # And swaps them if neccessary
            temp = highscorelist[i]
            highscorelist[i] = newscore
            newscore = temp
    return highscorelist

def inarea(x_coor_pic, y_coor_pic, wid_pic, he_pic, x_mous, y_mous):
    result = True
    if x_mous < x_coor_pic or x_mous > (x_coor_pic + wid_pic):
        result = False
    if y_mous > (600 - y_coor_pic) or y_mous < (600 - y_coor_pic - he_pic):
        result = False
    return result

# render text for displaying the score
label = myfont.render("Score: "+str(score), 1, (255,255,0))

# Will be used for implementing changing direction as it is in original Pacman
def createacopyofobject(Pacman):
    Pacmanexampleforcollisions = moving_object(Pacman.get_speed(), Pacman.get_direction(), widthPac, heightPac,
                                               colorPac)
    Pacmanexampleforcollisions.rect.x = Pacman.rect.x
    Pacmanexampleforcollisions.rect.y = Pacman.rect.y
    return Pacmanexampleforcollisions

# Declaring Pacman
Pacman = moving_object(initspeedPac, initdirectionPac, widthPac, heightPac, colorPac)
Pacman.rect.x = initxPac
Pacman.rect.y = inityPac

# Declaring an enemy
EnA = moving_object(initspeed, initdirectionEnA, widthEn, heightEn, colorEnA)
EnA.rect.x = initxEnA
EnA.rect.y = inityEnA
# And adding it to the list of enemies
enemies_list.add(EnA)

# Declaring an enemy
EnB = moving_object(initspeed, initdirectionEnB, widthEn, heightEn, colorEnB)
EnB.rect.x = initxEnB
EnB.rect.y = inityEnB
# And adding it to the list of enemies
enemies_list.add(EnB)

# Declaring an enemy
EnC = moving_object(initspeed, initdirectionEnC, widthEn, heightEn, colorEnC)
EnC.rect.x = initxEnC
EnC.rect.y = inityEnC
# And adding it to the list of enemies
enemies_list.add(EnC)

# Declaring an enemy
EnD = moving_object(initspeed, initdirectionEnD, widthEn, heightEn, colorEnD)
EnD.rect.x = initxEnD
EnD.rect.y = inityEnD
# And adding it to the list of enemies
enemies_list.add(EnD)

Pacmanexampleforcollisions = createacopyofobject(Pacman)

# Two direction indicators, one for the current, one for the one that is to be the next one
currentdirection = initdirectionPac
newdirection = currentdirection

all_sprites_list.add(Pacman)
all_sprites_list.add(EnA)
all_sprites_list.add(EnB)
all_sprites_list.add(EnC)
all_sprites_list.add(EnD)

list_nodes_to_Pacman = {}
list_nodes_to_Pacman[EnA] = []
list_nodes_to_Pacman[EnB] = []
list_nodes_to_Pacman[EnC] = []
list_nodes_to_Pacman[EnD] = []

# Have a variable indicating if the game has just been reset (after just starting or reseting the positions
justStarted = True

# Have values for xcoord and ycoord to avoid error at the beginning of the game
xcoord = 0
ycoord = 0
# Have a variable for indicating the level
level = 2

# Have a variable indicating if it's start, game or end screen
screen_state = 0

# Have a variable for preserving the score before resetting the game
last_score = 0

# Gets a list of high scores from the file
with open('high_scores.txt') as f:
    list_of_high_scores = f.read().splitlines()
    # Convert them to integers
    for i in range(0, len(list_of_high_scores)):
        list_of_high_scores[i] = int(list_of_high_scores[i])

print(list_of_high_scores)

def print_high_scores(list_of_high_scores, color):
    for i in range(0, 10):
        score_to_print = font_scores.render(str(str(list_of_high_scores[i])), 1, color)
        screen.blit(score_to_print, (120 + 240*(math.floor(i/5)), 250 + 40*(i%5)))

def print_high_scores_start(list_of_high_scores, color):
    for i in range(0, 10):
        score_to_print = font_scores.render(str(str(list_of_high_scores[i])), 1, color)
        screen.blit(score_to_print, (330, 200 + 40*i))
# -------- Main Program Loop -----------
while not done:

    # The following happens if the game is at start screen
    if screen_state == 0:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True

        pygame.event.get()
        # screen cleared to black
        screen.fill(BLACK)
        # Displays the image for the starting screen
        screen.blit(StartingScreen, (0, 0))
        print_high_scores_start(list_of_high_scores, YELLOW)
        # If it is over the block with "easy", sets level to 1
        if inarea(60, 339, 160, 50, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            level = 1
            # And starts if the left mouse button is pressed
            if pygame.mouse.get_pressed()[0]:
                screen_state = 1
        # If it is over the block with "medium", sets level to 2
        if inarea(60, 269, 160, 50, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            level = 2
            # And starts the game is left mouse button is pressed
            if pygame.mouse.get_pressed()[0]:
                screen_state = 1

    # The following happens if the screen is in game state
    if screen_state == 1:
        # --- Main event loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = True
            # user pressed down on a key
            elif event.type == pygame.KEYDOWN:
                Pacmanexampleforcollisions = createacopyofobject(Pacman)
                Pacmanexampleforcollisions.signalfromkeyboard(event)
                newdirection = Pacmanexampleforcollisions.get_direction()

        # --- Game logic should go here

        # Pacman moves every step in the game
        # If there was a change of the direction comming from the user
        if currentdirection != newdirection:
            # Then uses the example of Pacman to verify if turn possible
            Pacmanexampleforcollisions.new_direction(newdirection)
            # And checks if there would be a collision
            if Pacmanexampleforcollisions.wouldcollide(wall_list):
                # If so, moves Pacman as if there was nothing from the user
                Pacman.moving_object_detecting_collisions(wall_list)
                # And moves the example Pacman as well
                Pacmanexampleforcollisions = createacopyofobject(Pacman)
            else:
                # If no collision, checks the direction of movement of Pacman
                Pacman.new_direction(newdirection)
                # And moves Pacman
                Pacman.moving_object_detecting_collisions(wall_list)
                # Now the Pacman moves in the direction in which the user wants it to
                currentdirection = newdirection
        # If there is no signal from the user, just moves the Pacman preventing collisions
        else:
            Pacman.moving_object_detecting_collisions(wall_list)

        lastNodePacman = node("nameInitial")
        # Note the last node visited by Pacman
        for eachNode in mapGraph.nodes:
            if eachNode.getName() == (str(int(Pacman.rect.y / 20)) + " " + str(int(Pacman.rect.x / 20))) and int(
                            Pacman.rect.y / 20) * 20 == Pacman.rect.y and int(Pacman.rect.x / 20) * 20 == Pacman.rect.x:
                lastNodePacman = eachNode

        # Move the enemies
        for every_enemy in enemies_list:
        # If it is at a node, change direction randomly
        # Check which node it is at
            for eachNode in mapGraph.nodes:
                # Checks which node it is at and if it is at any node
                if eachNode.getName() == (
                        str(int(every_enemy.rect.y / 20)) + " " + str(int(every_enemy.rect.x / 20))) and int(
                                every_enemy.rect.y / 20) * 20 == every_enemy.rect.y and int(
                                every_enemy.rect.x / 20) * 20 == every_enemy.rect.x:
                    # Goes in random directions if the level is set as easy
                    if level == 1:
                        # Creates a list of possible destinations
                        possibleDestinations = []
                        for aNode in mapGraph.childrenOf(eachNode).keys():
                            possibleDestinations.append(aNode)
                        # Choses the destination node randomly
                        destination_node = random.choice(possibleDestinations)
                        # Gets x and y coordinates of the destination node
                        ycoord = ""
                        iterator = 0
                        while destination_node.getName()[iterator] != " ":
                            # Gets y-coordinate, row number
                            ycoord += str(destination_node.getName()[iterator])
                            iterator += 1
                        xcoord = destination_node.getName()[(iterator + 1):]
                        ycoord = int(ycoord)
                        xcoord = int(xcoord)

                    # Follows a path to the last registered node of Pacman
                    if level == 2:
                        # Finding the path using DFS
                        if lastNodePacman in mapGraph.nodes and len(list_nodes_to_Pacman[every_enemy]) == 0:
                            list_nodes_to_Pacman[every_enemy] = DepthFirstSearch(eachNode, lastNodePacman, mapGraph, [], [])
                        if len(list_nodes_to_Pacman[every_enemy])>0:
                            next_node = list_nodes_to_Pacman[every_enemy].pop(0)
                            xcoord = get_coordinates_from_name(next_node)[0]
                            ycoord = get_coordinates_from_name(next_node)[1]

                    # Changes destination accordingly
                    if xcoord*20 > every_enemy.rect.x:
                        every_enemy.new_direction(2)
                    if xcoord*20 < every_enemy.rect.x:
                        every_enemy.new_direction(4)
                    if ycoord*20 > every_enemy.rect.y:
                        every_enemy.new_direction(3)
                    if ycoord*20 < every_enemy.rect.y:
                        every_enemy.new_direction(1)
        # Move enemies
        for every_enemy in enemies_list:
            # Move forward
            every_enemy.moving_object_detecting_collisions(wall_list)

        # If Pacman collides with an enemy, it loses a life and enemies and Pacman are reset
        if pygame.sprite.spritecollide(Pacman, enemies_list, False):
            available_lives -= 1
            # Reset position of Pacman
            Pacman.rect.x = initxPac
            Pacman.rect.y = inityPac
            # Reset the position of enemies
            EnA.rect.x = initxEnA
            EnA.rect.y = inityEnA
            EnB.rect.x = initxEnB
            EnB.rect.y = inityEnB
            EnC.rect.x = initxEnC
            EnC.rect.y = inityEnC
            EnD.rect.x = initxEnD
            EnD.rect.y = inityEnD
            # Indicate the game has just been reset
            justStarted = True

        # If there are less than 0 available lives, game is over
        if available_lives < 0:
            screen_state = 2

        # If it collects all the coins, you win
        if len(coin_list.sprites()) == 0:
            screen_state = 3

        # Update score and make the coin disappear
        newscorecoinlistandspriteslist = scorecounter(score, coin_list, Pacman, pointspercoin, all_sprites_list)
        score = newscorecoinlistandspriteslist[0]
        coin_list = newscorecoinlistandspriteslist[1]
        all_sprites_list = newscorecoinlistandspriteslist[2]

        # update text for displaying the score
        label = myfont.render("Score: " + str(score), 1, (255, 255, 0))

        # screen cleared to white
        screen.fill(BLACK)

        # --- Drawing
        all_sprites_list.draw(screen)

        # Drawing the score on the left side below the map
        screen.blit(label, (10, 450))
        # Drawing as many icons of Pacman on the right side as many lives are available
        for i in range(0, available_lives):
            screen.blit(PacmanImage, (470 - 25*i, 450))

    # If the game is lost or won, it is reset to initial state
    if screen_state == 2 or screen_state == 3:
        # Set last_score to score in order to use it for the top 10 scores
        last_score = score
        # Reset Pacman's position
        Pacman.rect.x = initxPac
        Pacman.rect.y = inityPac
        # Reset the position of enemies
        EnA.rect.x = initxEnA
        EnA.rect.y = inityEnA
        EnB.rect.x = initxEnB
        EnB.rect.y = inityEnB
        EnC.rect.x = initxEnC
        EnC.rect.y = inityEnC
        EnD.rect.x = initxEnD
        EnD.rect.y = inityEnD
        # Reset the lives available and the score
        available_lives = 2
        score = 0
        # Empty the lists of coins and walls
        wall_list.empty()
        coin_list.empty()
        all_sprites_list.empty()
        # And fill them in again
        adding_map(basicmap, heightofwalls, widthofwalls, colorofwalls, colorofcoins)
        for enemy in enemies_list:
            all_sprites_list.add(enemy)
        # Check if the new score should be on the leaderboard
        list_of_high_scores = newhighscores(list_of_high_scores, last_score)

    # The following is executed if the game is lost
    if screen_state == 2:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen_state = 0

        screen.fill(BLACK)
        screen.blit(GameOverScreen, (0, 0))
        print_high_scores(list_of_high_scores, RED)

    # The following is executed is the game is won
    if screen_state == 3:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen_state = 0
        screen.fill(BLACK)
        screen.blit(YouWonScreen, (0, 0))
        print_high_scores(list_of_high_scores, GREEN)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Wait if the game has just started or has just been reset
    if justStarted:
        # Wait 3 seconds before the game goes live
        time.sleep(1)
        justStarted = False

    # --- Limit to 60 frames per second
    pygame.display.set_caption(str(clock.get_fps()))
    clock.tick(60)

high_scores_file = open('high_scores.txt', 'w')
for i in range(0, len(list_of_high_scores)):
    high_scores_file.write(str(list_of_high_scores[i])+"\n")
high_scores_file.close()

# Close the window and quit.
pygame.quit()
