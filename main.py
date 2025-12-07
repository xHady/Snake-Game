# Code By xHady

from tkinter import *
from tkinter import ttk
import random

gameBackground = "saddle brown"

# ------------------- Configure Tkinter ----------------------------
root = Tk()
root.title("Snake Game")
root.configure(background=gameBackground)
root.minsize(800, 800)
root.geometry("800x800")
# ------------------------------------------------------------------

class Snake:
    def __init__(self, root, parent, speed):
        self.root = root
        self.parent = parent
        self.speed = speed
        self.initVariables()
        self.configureCanvas()
        self.startGame()

        
    def configureCanvas(self):
        # ------------------- Configure Canvas ----------------------------
        self.canvas = Canvas(self.root, width=800, height=800, bg=gameBackground, highlightbackground=gameBackground)
        self.canvas.pack()
        # ------------------------------------------------------------------

    def initVariables(self):
        # ----------------- Main Variables 3> ------------------------------
        self.gridColors = ["green4", "yellow green"]
        self.rows = 20
        self.columns = 20
        self.cellSize = 40
        self.direction = 0 # 0 -> Right, 1 -> Up, 2 -> Down, 3 -> Left
        self.next_direction = 0 # stores last direction state
        self.score = 0
        self.SnakePosition = []
        self.MoveStarted = False
        # ------------------------------------------------------------------
        
    def updateScore(self, sc):
        self.score += sc
        self.canvas.itemconfigure(self.scoreText, text="Score : " + str(self.score))

    def on_press(self, event): # handle Keyboard
            # Left Arrow 37, 65
            # Down Arrow 40, 83
            # Right Arrow 39, 68
            # Up Arrow 38, 87
            self.MoveStarted = True
            if self.canvas.itemconfigure(self.pauseTag, "state")[4] == "normal":
                self.canvas.itemconfigure(self.pauseTag,  state="hidden")
            #self.canvas.itemconfigure(self.pauseTag, state="hidden")
            if ( event.keycode == 37 or event.keycode == 65 ) and self.direction != 0 and self.direction != 3:
                # print("left")
                self.next_direction = 3
            elif ( event.keycode == 40 or event.keycode == 83 ) and self.direction != 1 and self.direction != 2:
                # print("Down")
                self.next_direction = 2
            elif ( event.keycode == 39 or event.keycode == 68 ) and self.direction != 3 and self.direction != 0:
                # print("Right")
                self.next_direction = 0
            elif ( event.keycode == 38 or event.keycode == 87 ) and self.direction != 2 and self.direction != 1:
                # print("Up")
                self.next_direction = 1
            elif( event.keycode == 80 ):
                self.MoveStarted = False
                self.canvas.itemconfigure(self.pauseTag, state="normal")

    def drawRect(self, RectPos, color): # Draws A Rectangle ( Duhh )

        x1 = RectPos[1] * self.cellSize
        y1 = RectPos[0] * self.cellSize
        x2 = x1 + self.cellSize
        y2 = y1 + self.cellSize
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def movApple(self): # Moves apple location to a proper one
        x1 = random.randint(1, self.rows - 2) * self.cellSize
        y1 = random.randint(1, self.columns - 2) * self.cellSize
        x2 = x1 + self.cellSize
        y2 = y1 + self.cellSize
        self.canvas.coords(self.Apple, x1, y1, x2, y2)
        for part in self.SnakePosition:
            if self.canvas.coords(self.Apple) == self.canvas.coords(part):
                self.movApple()

    def addSnakeNode(self): # simple Algorithm to add Node to Snake Tail
        lastNodeX = self.canvas.coords(self.SnakePosition[len(self.SnakePosition) - 1])[0] / self.cellSize
        lastNodeY = self.canvas.coords(self.SnakePosition[len(self.SnakePosition) - 1])[1] / self.cellSize
        lastTwoNodesXCoords = lastNodeX - self.canvas.coords(self.SnakePosition[len(self.SnakePosition) - 2])[0] / self.cellSize
        lastTwoNodesYCoords = lastNodeY - self.canvas.coords(self.SnakePosition[len(self.SnakePosition) - 2])[1] / self.cellSize
        
        
        if lastTwoNodesXCoords == 0 and lastTwoNodesYCoords > 0:
            # print("Add Node Down")
            rect = self.drawRect([lastNodeX + 1, lastNodeY], "Gray")
        elif lastTwoNodesXCoords == 0 and lastTwoNodesYCoords < 0:
            # print("Add Node Up")
            rect = self.drawRect([lastNodeX - 1, lastNodeY], "Gray")
        elif lastTwoNodesXCoords > 0 and lastTwoNodesYCoords == 0:
            # print("Add Node Right")
            rect = self.drawRect([lastNodeX, lastNodeY + 1], "Gray")
        else: #lastTwoNodesXCoords < 0 and lastTwoNodesYCoords == 0:
            # print("Add Node Left")
            rect = self.drawRect([lastNodeX, lastNodeY - 1], "Gray")
        self.SnakePosition.append(rect)
        return rect

    def getNextPos(self):
        if self.direction == 0: # Right
            return [self.cellSize, 0]
        elif self.direction == 1: # Up
            return [0, -1 * self.cellSize]
        elif self.direction == 2: # Down
            return [0, self.cellSize]
        elif self.direction == 3: # Left
            return [-1 * self.cellSize, 0]
        
    def getNextCoords(self, currCoords):
        next_pos = self.getNextPos()
        x1 = currCoords[0] + next_pos[0]
        y1 = currCoords[1] + next_pos[1]
        x2 = x1 + self.cellSize
        y2 = y1 + self.cellSize
        return [x1, y1, x2, y2]

    def moveSnakeNode(self, rectId): # move specific Node
        # drawRect(RectPos, color)
        nextPos = self.getNextPos()
        self.canvas.move(rectId, nextPos[0], nextPos[1])

        x = self.canvas.coords(self.SnakePosition[0])[0] / self.cellSize
        y = self.canvas.coords(self.SnakePosition[0])[1] / self.cellSize

    def moveSnake(self): # Move entire snake hhh
        snakeCords = []

        for m in self.SnakePosition: # I am storing them first to better Performance
            Cords = self.canvas.coords(m)
            snakeCords.append([Cords[0], Cords[1], Cords[2], Cords[3]])

        for i, item in enumerate(self.SnakePosition):
            currCords = snakeCords[i]
            if item == self.SnakePosition[0]:
                self.direction = self.next_direction # get last direction
                next_coords = self.getNextCoords(currCords)
                if next_coords[0] / self.cellSize == 0 or next_coords[1] / self.cellSize == self.columns - 1 or next_coords[1] / self.cellSize == 0 or next_coords[0] / self.cellSize == self.rows - 1:
                        self.game_started = False 
                        return
                        
                for i, snakeItem in enumerate(self.SnakePosition):
                    if snakeCords[i] == next_coords: # Snake ate his own body :(
                        self.game_started = False 
                        return
                self.moveSnakeNode(item)
                if self.canvas.coords(self.Apple) == next_coords: # Head ate apple
                    # print("Ate Apple")
                    self.updateScore(100)
                    self.movApple()
                    newNode = self.addSnakeNode()
                    newNodeCords = self.canvas.coords(newNode)
                    snakeCords.append([newNodeCords[0], newNodeCords[1], newNodeCords[2], newNodeCords[3]])
            else:
                self.canvas.coords(item, last_node_cord[0], last_node_cord[1], last_node_cord[2], last_node_cord[3])
            last_node_cord = currCords

    def drawMainGrid(self): # Draw Basic Shape
        for r in range(self.rows):
            for c in range(self.columns):
                color = self.gridColors[(r + c) % 2]
                if ( r == 0 ) or ( c == 0 ) or ( r == self.rows - 1 ) or ( c == self.columns - 1 ):
                    color = gameBackground
                self.drawRect([r, c], color)

    def intializeGame(self):
        self.root.bind("<KeyPress>", self.on_press)
        self.drawMainGrid()
        self.Apple = self.drawRect([3, 3], "Red")
        self.SnakePosition.append(self.drawRect([10, 10], "Black"))
        self.SnakePosition.append(self.drawRect([10, 9], "Gray"))

    def addObjectstoUI(self):

        self.scoreText = self.canvas.create_text(50, 20, text="Score : 0", font=("Pursia", 20), anchor=W)
        self.pauseTag = self.canvas.create_text(400, 400, text="Pauesd", font=("Pursia", 40), anchor=CENTER)
        self.canvas.itemconfigure(self.pauseTag, state="hidden")

    def gameLoop(self):
        if self.MoveStarted:
            self.moveSnake()
        if self.game_started:
            self.root.after(int(1000 / self.speed), self.gameLoop)
        else:
            self.canvas.destroy()
            self.parent.gameEnded(self.score)
    def startGame(self):
        self.intializeGame()
        self.addObjectstoUI()
        self.game_started = True
        self.root.after(int(1000 / self.speed), self.gameLoop)

        # self.__init__(self.root, self.canvas)

#test = Snake(root, canvas)
class MainScreen:
    def __init__(self, root):
        self.root = root
        self.addSnakeImg()
        self.getName()

    def addSnakeImg(self):
            if hasattr(self, "image_label") == False:
                self.snakeImage = PhotoImage(file="snake.png").subsample(2, 2)
            self.image_label = Label(root, image=self.snakeImage, bg=gameBackground, anchor="n")
            self.image_label.pack()

    def gameEnded(self, score):

        self.addSnakeImg()

        self.gameName = Label(self.root, text="Game Over, " + self.playerName + "\nYour Score is " + str(score), font=("pursia", 20), bg=gameBackground)
        self.gameName.pack()

        self.copyRight.destroy()

        self.showPlayButton("Play Again!")

    def enterGame(self):
        self.button.destroy()
        self.image_label.destroy()
        self.gameName.destroy()
        self.currGame = Snake(self.root, self, self.speed)

    def addCopyRights(self):
        self.copyRight = Label(self.root, text="By xHady", font=("pursia", 10), bg=gameBackground, anchor="s")
        self.copyRight.pack()

    def showPlayButton(self, text):
        self.button = Button(self.root, text=text, command=self.enterGame, height=2, width=10)
        self.button.pack(padx=5, pady=5)
        self.addCopyRights()

    def speedDefined(self):
        self.speed = int(self.playerObj.get("1.0", "end-1c"))
        if self.speed > 0 and self.speed < 51:
            self.gameName.destroy()
            self.playerObj.destroy()
            self.button.destroy()

            self.showPlayButton("Play Game")
        
    def nameEntered(self):
        self.playerName = self.playerObj.get("1.0", "end-1c")
        if(self.playerName != ""):

            self.gameName.destroy()
            self.playerObj.destroy()
            self.button.destroy()
            self.copyRight.destroy()
            self.ask.destroy()

            self.gameName = Label(self.root, text="Set Game Speed 1 - 50", font=("pursia", 15), bg=gameBackground)
            self.gameName.pack()

            self.playerObj = Text(self.root, height=1, width=25)
            self.playerObj.pack(padx=5, pady=5)
            self.playerObj.insert("end", "7")
            self.button = Button(self.root, text="Enter", command=self.speedDefined, height=2, width=10)
            self.button.pack(padx=5, pady=5)

    def getName(self):
        self.gameName = Label(self.root, text="Welcome to Snake Game", font=("pursia", 20), bg=gameBackground)
        self.gameName.pack()

        self.ask = Label(self.root, text="Enter Your Name : ", font=("pursia", 10), bg=gameBackground)
        self.ask.pack(padx=5, pady=5)

        self.playerObj = Text(self.root, height=1, width=25)
        self.playerObj.pack(padx=5, pady=5)

        self.button = Button(self.root, text="Enter", command=self.nameEntered, height=2, width=10)
        self.button.pack(padx=5, pady=5)

        self.addCopyRights()

        self.root.mainloop()
    
MainScreen(root)
