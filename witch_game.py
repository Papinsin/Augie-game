# Devid , Ali 
# protext augustana college 
# main character augustana viking (axe vapon)
# randomly generate valiens (different college logos)
# randomly generate the background 
# maskot 
'''

Use the witch to catch spiders. Move the witch using the left and right arrow keys.
If the witch catches enough spiders before they escape, you win.
'''
from graphics2 import *
import time
import random
import math
import pygame

SPIDER_SPEED = 5
WITCH_SPEED = 25
NUM_LOSE = 5
NUM_WIN = 20
STALL_TIME = 0.05
THRESHOLD = 50
AXE_SPEED = 15 

pygame.mixer.init()

# ✅ LOAD ONCE HERE (Before the loop starts)
pygame.mixer.music.load("sounds/GameLoop.mp3")
hitEnemySound = pygame.mixer.Sound("sounds/hitEnemy.mp3")
gameOverSound = pygame.mixer.Sound("sounds/gameOver.mp3")
gameOverSoundByPoints = pygame.mixer.Sound("sounds/loseByPoints.mp3")
coalision = pygame.mixer.Sound("sounds/coalision.mp3")
winSound = pygame.mixer.Sound("sounds/winSound.mp3")


# catch_sound = pygame.mixer.Sound("catch.wav")

# winSound = 
# LoseSound =

listOfAxes  =[]
WindowHeight = 666
WindowWidth = 666

rect_height = 200


mainCharacterImage = "images/dwarf_transparent_cropped.png"

mainCharacterWeaponImage = 'images/axe_spin_v2.gif' 

enemies = [
    "butler_bulldog_2.png",
    "carthage_firebird_2.png",
    "elmhurst_bluejay_2.png",
    "illinoiswesleyan_titan_2.png",
    "northcentral_cardinal_2.png",
    "wheaton_thunder_2.png",
    ]

locations = [f"images/{name}" for name in [
    "images.png",
    "images-1.png",
    "TRIC_projects_Augustana_Hanson_Hall_10.png",
]]

def throwAxe(window ,witch , weapon):


    witchPositionX = witch.getCenter().getX()
    witchPositionY = witch.getCenter().getY()

    weaponAxe = Image(Point(witchPositionX , witchPositionY -40 ), mainCharacterWeaponImage)
    weaponAxe.scale(1/7)
    weaponAxe.draw(window)
    listOfAxes.append(weaponAxe)


def throwAxe(window, witch, axes):
    '''Creates one new axe at the witch's position and adds it to the list.'''
    pos = witch.getCenter()
    axe = Image(Point(pos.getX(), pos.getY() - 40), mainCharacterWeaponImage)
    axe.scale(1/10)
    axe.draw(window)
    axes.append(axe)

def updateAxes(axes, spiderList):
    '''
    Moves every axe up one step, removes axes that leave the screen,
    and removes any enemy an axe hits.

    Returns:
    the number of enemies hit this frame
    '''
    hits = 0
    for axe in axes[:]:
        axe.move(0, -AXE_SPEED)

        # undrawing the axe if it passes y = 0

        if(axe.getCenter().getY() < 0):
            axe.undraw()
            axes.remove(axe)
            continue

        #use a for loop to check if any 
        #of the spiders were hit        
        for spider in spiderList[:]:
            if(is_close_enough(spider, axe)):
                hitEnemySound.play()
                spider.undraw()
                spiderList.remove(spider)

                axe.undraw()
                axes.remove(axe)

                hits+= 1
                break

    return hits

def displayOfInstructions(window):
    shown = []                       # everything drawn here, so it can all be undrawn at the end

    def add(obj):
        obj.draw(window)
        shown.append(obj)

    TEXT_X = 430                     # center of the title / instructions / start message
    COL_X = 90                       # center of the enemy pictures
    GAP = 12                         # space between a picture and its name

    # black background box
    panel = Rectangle(Point(30, 40), Point(636, 626))
    panel.setFill("black")
    add(panel)

    # title
    title = Text(Point(TEXT_X, 90), "AUGUSTANA VIKING")
    title.setFill("white")
    title.setSize(24)
    add(title)

    # instructions
    info = Text(Point(TEXT_X, 200), f"Catch the rival colleges\n Protect the campus !!!\n Use the LEFT / RIGHT arrow keys to move.\nCatch {NUM_WIN} to win. Miss {NUM_LOSE} and you lose.")
    info.setFill("white")
    info.setSize(14)
    add(info)

    # enemy column: picture on the left, name to its right
    TOP = 120
    BOTTOM = 545                     # must end above the start message (y=570)
    ROW_H = (BOTTOM - TOP) / len(enemies)

    for i, file in enumerate(enemies):
        y = TOP + i * ROW_H + ROW_H / 2          # vertical center of this row

        pic = Image(Point(COL_X, y), "images/" + file)
        pic.scale(1 / 7)
        add(pic)

        label = file.replace(".png", "").replace("_", " ").rstrip("2").strip()
        textWidth = len(label) * 6               # rough width of size-10 text
        nameX = COL_X + pic.getWidth() / 2 + GAP + textWidth / 2   # Text is centered on its point
        nameText = Text(Point(nameX, y), label)
        nameText.setFill("white")
        nameText.setSize(10)
        add(nameText)

    # start message
    start = Text(Point(TEXT_X, 570), "Press any key to start")
    start.setFill("yellow")
    start.setSize(16)
    add(start)

    window.getKey()                  # wait for a key press

    for obj in shown:                # remove everything
        obj.undraw()

def distance_between_points(point1, point2):
    '''
    Calculates the distance between two points
    
    Params:
    point1 (Point): the first point
    point2 (Point): the second point
    
    Returns:
    the distance between the two points
    '''
    p1x = point1.getX()
    p1y = point1.getY()
    p2x = point2.getX()
    p2y = point2.getY()
    return math.sqrt((p1x - p2x)*(p1x - p2x) + (p1y - p2y) * (p1y - p2y))


def is_close_enough(witch_img, spider_img):
    '''
    Determines if the witch is close enough to the spider to say the witch
    caught the spider.
    
    Params:
    witch_img (Image): the image of the witch
    spider_img (Image): the image of the spider
    
    Returns:
    True if the witch catches the spider
    '''
    witchCenter = witch_img.getCenter()
    spiderCenter = spider_img.getCenter()

    if distance_between_points(witchCenter , spiderCenter) < THRESHOLD:
        return True
    else:
        return False
    
def move_spiders(spider_img_list):
    '''
    Moves every spider one SPIDER_SPEED unit down the window
    
    Params:
    sprider_img_list (list): the list of falling spiders
    '''
    for spider in spider_img_list:
        spider.move(0 , SPIDER_SPEED)


def move_witch(window, witch_img, weapons):
    '''
    Moves the witch based on:
    1. Arrow keys
    2. Mouse clicks within the witch's height:
       - Clicked to the left of the witch image -> moves left
       - Clicked to the right of the witch image -> moves right
    '''
    
    # 1. Keyboard Movement with boundary checks
    key = window.checkKey()
    witch_imgX = witch_img.getCenter().getX()

    if key == "Right" and witch_imgX < 616:
        witch_img.move(WITCH_SPEED, 0)
    elif key == "Left" and witch_imgX > 50:
        witch_img.move(-WITCH_SPEED, 0)
    elif key == "space":
        throwAxe(window ,witch_img,weapons)
    
    # 2. Mouse Click Movement relative to the image edges
    click = window.checkMouse()
    if click is not None:
        clickX = click.getX()
        clickY = click.getY()
        
        # Get the witch's center and dimensions
        center_x = witch_img.getCenter().getX()
        center_y = witch_img.getCenter().getY()
        
        # Images in graphics.py have getWidth() and getHeight()
        half_width = witch_img.getWidth() / 2
        half_height = witch_img.getHeight() / 2
        
        # Calculate image boundaries
        left_edge = center_x - half_width
        right_edge = center_x + half_width
        top_edge = center_y - half_height
        bottom_edge = center_y + half_height
        
        # Check instruction criteria:
        # - The click must be WITHIN the height of the image
        # - The click must be strictly to the left or right of the image edges
        if top_edge <= clickY <= bottom_edge:
            if clickX < left_edge and witch_imgX > 50:
                witch_img.move(-WITCH_SPEED, 0)
            elif clickX > right_edge and witch_imgX < 616:
                witch_img.move(WITCH_SPEED, 0)
            
def add_spider_to_window(window):
    '''
    Adds one spider to the top of the window at a random location
    
    Params:
    window (GraphWin): the window where game play takes place
    
    Returns:
    the spider added to the window
    '''
    x_coordinate = random.randrange(20,620)
    spider = Image(Point(x_coordinate , 0),f'images/{random.choice(enemies)}')
    spider.scale(1/7)
    spider.draw(window)
    return spider
def gameOver(witch ,  window):
    time.sleep(1)
    gameOverText = Text(Point(WindowWidth/2, WindowHeight/2) ,"Game Over")
    gameOverText.setSize(90)
    gameOverText.draw(window)
    gameOverText.setStyle("bold")
    gameOverText.setFace("times roman")
    gameOverText.setTextColor("darkRed")
    witch.move(WindowHeight + 2 , WindowWidth + 2)
    window.getMouse()

def win(witch,window):
    winSound.play()
    time.sleep(1)
    gameOverText = Text(Point(WindowWidth/2, WindowHeight/2) ,"You Win")
    gameOverText.setSize(90)
    gameOverText.draw(window)
    gameOverText.setStyle("bold")
    gameOverText.setFace("times roman")
    gameOverText.setTextColor("darkGreen")
    witch.move(WindowHeight + 2 , WindowWidth + 2)
    window.getMouse()


def game_loop(window, witch):
    spiderList = []
    axes = []
    missed = 0
    cought = 0
    loseStatus = False 
    score = Text(Point(50, 40), '')
    score.draw(window)

    pygame.mixer.music.play(-1)  
    while missed < NUM_LOSE and cought < NUM_WIN and not loseStatus:
        score.setText(f"missed: {missed}  caught: {cought}")
        score.setFill("red")

        move_witch(window, witch, axes)

        # randomly spawn a new enemy
        if random.randrange(100) < 6:
            spider = add_spider_to_window(window)
            spiderList.append(spider)

        # move enemies, check for witch catch or escape
        for spider in spiderList[:]:
            spider.move(0, SPIDER_SPEED)

            if is_close_enough(witch, spider):
                coalision.play() 
                gameOver(witch , window )
                loseStatus = True
                    

            elif spider.getCenter().getY() > 700:
                spider.undraw()
                spiderList.remove(spider)
                missed = missed + 1

        # move axes and check for axe hits
        cought = cought + updateAxes(axes, spiderList)

        time.sleep(STALL_TIME)
        if (missed >= NUM_LOSE):
            pygame.mixer.music.stop()
            gameOverSoundByPoints.play()
            gameOver(witch, window)

        elif(cought >= NUM_WIN):
            win(witch,  window)
    




# def creatingActionSquares(window):
#     # WindowHeight;
#     # WindowWidth;

    
    
#     left_rectangle = Rectangle(Point(0, WindowHeight - rect_height), Point(WindowWidth /2, WindowWidth))
#     # left_rectangle.setOutline("black")
#     left_rectangle.draw(window)

#     left_rectangle = left_rectangle.getCenter()
#     left_rectangle = Text(left_rectangle, "")
#     # left_rectangle.setFill("black")
#     left_rectangle.draw(window)


#     right_rectangle = Rectangle(Point(WindowWidth/2, WindowHeight - rect_height), Point(WindowWidth, WindowWidth))
#     # right_rectangle.setOutline("black")
#     right_rectangle.draw(window)

#     right_rectangle = right_rectangle.getCenter()
#     right_rectangle = Text(right_rectangle, "")
#     # right_rectangle.setFill("black")
#     right_rectangle.draw(window)

def main():
    # setup the game 
    window = GraphWin("Arachnophobia!!!", 666,666)
    BGImage = Image(Point(WindowHeight/2,WindowWidth/2), random.choice(locations))
    BGImage.setShapeSize(WindowWidth , WindowHeight)
    BGImage.draw(window)
    directions = Text(Point(333, 650), 'Use the left/right arrow keys to move the witch.')
    directions.setSize(16)
    directions.draw(window)
    
    witch = Image(Point(333,580), mainCharacterImage)
    witch.scale(1/5)
    witch.draw(window)

    # creatingActionSquares(window)
    displayOfInstructions(window)
    game_loop(window, witch)
    

main()