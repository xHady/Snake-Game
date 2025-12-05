from tkinter import *
from tkinter import ttk
import random

    
gridColors = ["green4", "yellow green"]

# ----------------- Main Variables 3> ------------------------------
speed = 10
rows = 20
columns = 20
cellSize = 40
direction = 0 # 0 -> Right, 1 -> Up, 2 -> Down, 3 -> Left
score = 0
SnakePosition = []
MoveStarted = False
# ------------------------------------------------------------------

# ------------------- Configure Tkinter ----------------------------
root = Tk()
root.title("Snake Game")
root.configure(background="saddle brown")
root.minsize(800, 800)
root.geometry("800x800")
# ------------------------------------------------------------------

# ------------------- Configure Canvas ----------------------------
canvas = Canvas(root, width=800, height=800, bg="saddle brown", highlightbackground="saddle brown")
canvas.pack()

# ------------------------------------------------------------------

def updateScore(sc):
    global score, scoreText
    score += sc
    canvas.itemconfigure(scoreText, text="Score : " + str(score))

def on_press(event): # handle Keyboard
        # Left Arrow 37, 65
        # Down Arrow 40, 83
        # Right Arrow 39, 68
        # Up Arrow 38, 87
        global direction
        global MoveStarted
        if ( event.keycode == 37 or event.keycode == 65 ) and direction != 0 and direction != 3:
            # print("left")
            direction = 3
        elif ( event.keycode == 40 or event.keycode == 83 ) and direction != 1 and direction != 2:
            # print("Down")
            direction = 2
        elif ( event.keycode == 39 or event.keycode == 68 ) and direction != 3 and direction != 0:
            # print("Right")
            direction = 0
        elif ( event.keycode == 38 or event.keycode == 87 ) and direction != 2 and direction != 1:
            # print("Up")
            direction = 1
        MoveStarted = True

def drawRect(RectPos, color): # Draws A Rectangle ( Duhh )

    x1 = RectPos[1] * cellSize
    y1 = RectPos[0] * cellSize
    x2 = x1 + cellSize
    y2 = y1 + cellSize
    return canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

def movApple(): # Moves apple location to a proper one
    global rows, columns
    x1 = random.randint(1, rows - 2) * cellSize
    y1 = random.randint(1, columns - 2) * cellSize
    x2 = x1 + cellSize
    y2 = y1 + cellSize
    canvas.coords(Apple, x1, y1, x2, y2)
    for part in SnakePosition:
        if canvas.coords(Apple) == canvas.coords(part):
           movApple()

def addSnakeNode(): # simple Algorithm to add Node to Snake Tail
    lastNodeX = canvas.coords(SnakePosition[len(SnakePosition) - 1])[0] / cellSize
    lastNodeY = canvas.coords(SnakePosition[len(SnakePosition) - 1])[1] / cellSize
    lastTwoNodesXCoords = lastNodeX - canvas.coords(SnakePosition[len(SnakePosition) - 2])[0] / cellSize
    lastTwoNodesYCoords = lastNodeY - canvas.coords(SnakePosition[len(SnakePosition) - 2])[1]/ cellSize
    
    
    if lastTwoNodesXCoords == 0 and lastTwoNodesYCoords > 0:
        # print("Add Node Down")
        SnakePosition.append(drawRect([lastNodeX + 1, lastNodeY], "Gray"))
    elif lastTwoNodesXCoords == 0 and lastTwoNodesYCoords < 0:
        # print("Add Node Up")
        SnakePosition.append(drawRect([lastNodeX - 1, lastNodeY], "Gray"))
    elif lastTwoNodesXCoords > 0 and lastTwoNodesYCoords == 0:
        # print("Add Node Right")
        SnakePosition.append(drawRect([lastNodeX, lastNodeY + 1], "Gray"))
    elif lastTwoNodesXCoords < 0 and lastTwoNodesYCoords == 0:
        # print("Add Node Left")
        SnakePosition.append(drawRect([lastNodeX, lastNodeY - 1], "Gray"))


def moveSnakeNode(rectId): # move specific Node
    # drawRect(RectPos, color)
    if direction == 0: # Right
        canvas.move(rectId, cellSize, 0)
    elif direction == 1: # Up
        canvas.move(rectId, 0, -1 * cellSize)
    elif direction == 2: # Down
        canvas.move(rectId, 0, cellSize)
    elif direction == 3: # Left
        canvas.move(rectId, -1 * cellSize, 0)

    x = canvas.coords(SnakePosition[0])[0] / cellSize
    y = canvas.coords(SnakePosition[0])[1] / cellSize
    if ( x == 0 ) or ( y == 0 ) or ( x == rows -1 ) or ( y == columns - 1):
        global game_started
        game_started = False

def moveSnake(): # Move entire snake hhh
    global game_started
    last_pos = canvas.coords(SnakePosition[len(SnakePosition) - 1])
    x = last_pos[0] / cellSize
    y = last_pos[1] / cellSize
    for i in SnakePosition:
        tempcord = canvas.coords(i)
        if i == SnakePosition[0]:
            headSnakeCords = canvas.coords(i)
            moveSnakeNode(i)
            for part in SnakePosition:
                if canvas.coords(part) == headSnakeCords: # Snake ate his own body :(
                    game_started = False 
                    return
            if canvas.coords(Apple) == canvas.coords(i): # Head ate apple
                # print("Ate Apple")
                addSnakeNode()
                updateScore(100)
                movApple()
            
        else:
            canvas.coords(i, last_node_cord[0], last_node_cord[1], last_node_cord[2], last_node_cord[3])
        last_node_cord = tempcord

def drawMainGrid(): # Draw Basic Shape
    for r in range(rows):
        for c in range(columns):
            color = gridColors[(r + c) % 2]
            if ( r == 0 ) or ( c == 0 ) or ( r == rows - 1 ) or ( c == columns - 1 ):
                color = "saddle brown"
            drawRect([r, c], color)

def intializeGame():
    root.bind("<KeyRelease>", on_press)
    drawMainGrid()
    SnakePosition.append(drawRect([10, 10], "Black"))
    SnakePosition.append(drawRect([10, 9], "Gray"))

def addObjectstoUI():

    global score, Apple, scoreText
    Apple = drawRect([3, 3], "Red")
    scoreText = canvas.create_text(50, 20, text="Score : 0", font=("Pursia", 20), anchor=W)

intializeGame()
addObjectstoUI()
game_started = True

while game_started:
    if MoveStarted:
        moveSnake()
    root.update()
    root.after(int(1000 / speed))
