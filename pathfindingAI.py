import turtle, random, time, math
 
'''
0 = empty floor
1 = wall/barrier
9 = enemy
'''
 
# ---------------------Initial conditions-----------
# creating global variables, creatingin initial screen,
# loading and drawing map, etc
mywindow = turtle.Screen()
gridSquare = turtle.Turtle()
w = turtle.Turtle()
screenSize = 600  # dont edit this
dimension = 20  # this will be a fixed, 20x20 grid
gutter = 40  # so dont edit any
offset = 20  # of these values
squareSize = int((screenSize - (2 * gutter)) / dimension)  # each square will be this size
coordinates = []  # the list of lists containing centres of grid squares
theMap = []
currentLevel = 1
keyStatus = False
meRow = 1  # player's starting coordinates
meCol = 1
monsterCol = 19 # monster's starting coordinates
monsterRow = 19
checkedSquares = []
dummyStorage = []  # these are points on the edge of what we already have searched, search is done when this is empty or we found the player
gameIsOver = False
startTime = time.time()
parentSquares = []
 
 
# ----------------------------functions-------------------------
def initialScreenSetup():
   global screenSize, dimension, gutter, offset, squareSize, coordinates
   mywindow.setup(screenSize, screenSize)
   mywindow.title('Dark Dungeon')
   gridSquare.speed(0)
   gridSquare.penup()
   gridSquare.shape('square')
   gridSquare.turtlesize(1, 1)
   gridSquare.fillcolor('white')
   mywindow.tracer(0, 0)
   w.penup()
   w.hideturtle()
   w.goto(0, -280)
   w.write('Explore... if you dare!', align="center", font=("Arial", 12, "normal"))
   # -----------------------------the grid parameters----------------------------
 
   # ---these values are calculated----
 
   gridSquare.turtlesize(squareSize / 20, squareSize / 20)
   # -----------------now create the grid and underlying data structures
   # now draw the grid
   createGrid(screenSize, dimension, squareSize, offset)
   print('-----------cooridinates-------------')
   for i in range(len(coordinates)):
       print(coordinates[i])
   return
 
 
def createGrid(scr, dim, sq, off):
   # scr = screen width/height
   # dim = how many grid squares along screen edge
   # sq = grid square width/height
   # off = offset from left and top edge
   # now,determine the location (x,y) of the upper left square
   firstSqX = -1 * int(scr / 2) + sq + off
   firstSqY = int(scr / 2) - sq - off
   lastSqX = firstSqX + (dim * sq)
   lastSqY = firstSqY - (dim * sq)
   global coordinates
   for y in range(firstSqY, lastSqY, -1 * sq):
       temp = []
       for x in range(firstSqX, lastSqX, sq):
           # coordX = int((sq/2) * (col - dim))
           # gridSquare.goto(x,y)
           # gridSquare.stamp()
           temp.append((x, y))
           # print(x,y)
           # time.sleep(0.1)
       coordinates.append(temp)
   # mywindow.update()
   return
 
 
def leave():
   mywindow.bye()
   return
 
 
def loadMap(f):
   global theMap
   theMapFile = open(f, 'r')
   for line in theMapFile:
       temp = line.strip('\n')
       temp = list(temp)
       theMap.append(temp)
   theMapFile.close()
   for i in range(0, len(theMap), 1):
       for j in range(0, len(theMap[i]), 1):
           theMap[i][j] = int(theMap[i][j])
       print()
   return
 
 
def drawBoard():
   for row in range(len(theMap)):
       for col in range(len(theMap[row])):
           gridSquare.goto(coordinates[row][col])
           if theMap[row][col] == 0:
               gridSquare.fillcolor('white')
           else:
               gridSquare.fillcolor('black')
           gridSquare.stamp()
   mywindow.update()
   return
 
 
def specialSquare():
   return
 
 
def goRight():
   global meRow, meCol
   w.clear()
   if meCol < 19:
       if theMap[meRow][meCol + 1] != 1:
           meCol += 1
           me.goto(coordinates[meRow][meCol])
           specialSquare()
           mywindow.update()
   return
 
 
def goLeft():
   global meRow, meCol
   if meCol > 0:
       if meCol > 0:
           if theMap[meRow][meCol - 1] != 1:
               meCol -= 1
               me.goto(coordinates[meRow][meCol])
               specialSquare()
               mywindow.update()
   return
 
 
def goUp():
   global meRow, meCol
   if meRow > 0:
       if theMap[meRow - 1][meCol] != 1:
           meRow -= 1
           me.goto(coordinates[meRow][meCol])
           specialSquare()
           mywindow.update()
   return
 
 
def goDown():
   global meRow, meCol
   if meRow < 19:
       if theMap[meRow + 1][meCol] != 1:
           meRow += 1
           me.goto(coordinates[meRow][meCol])
           specialSquare()
           mywindow.update()
   return
 
 
def surroundingSquares(squareRow, squareCol):
   global monsterCol, monsterRow, theMap, coordinates, monsterRow, monsterCol, bordertoCheck, checkedSquares, parentSquares
   for row in range(-1, 2):
       try:
           if theMap[squareRow + row][squareCol] != 1 and [squareRow + row, squareCol] not in checkedSquares and [
               monsterRow, monsterCol] != [squareRow + row, squareCol]:
               if row != 0:
                   checkedSquares.append([squareRow + row, squareCol])
                   parentSquares.append([squareRow,squareCol])
       except:
           pass
   for col in range(-1, 2):
       try:
           if theMap[squareRow][squareCol + col] != 1 and [squareRow, squareCol + col] not in checkedSquares and [
               monsterRow, monsterCol] != [squareRow, squareCol + col]:
               if col != 0:
                   checkedSquares.append([squareRow, squareCol + col])
                   parentSquares.append([squareRow, squareCol])
       except:
           pass
 
 
def gameOver():
   mywindow.bye()
 
 
def monsterSearch():
   global monsterCol, monsterRow, theMap, coordinates, monsterRow, monsterCol, bordertoCheck, checkedSquares, dummyStorage, parentSquares
   FOUNDYOU = False
   surroundingSquares(monsterRow, monsterCol)
   while len(checkedSquares) > 0 and (meCol,meRow) != (monsterCol,monsterRow):
       for i in range(0, len(checkedSquares)):
           if [meRow, meCol] in checkedSquares:  # if one of the frontier squares is where the player is
               FOUNDYOU = True
           elif [meRow, meCol] not in checkedSquares and checkedSquares[i] not in dummyStorage:
               surroundingSquares(checkedSquares[i][0], checkedSquares[i][1])
           if FOUNDYOU:
               movetheMonster(meRow, meCol)
               break
       if FOUNDYOU:
           checkedSquares = []
           parentSquares = []
           break
   mywindow.ontimer(monsterSearch, 200)
 
 
def movetheMonster(row, col):
   global meRow, meCol, monsterRow, monsterCol, parentSquares, dummyStorage, checkedSquares, coordinates
   for i in range(0,len(checkedSquares)):
       if checkedSquares[i] == [row,col]:
           for k in range(0,len(parentSquares)):
               if k == i:
                   if parentSquares[k] == [monsterRow,monsterCol]:
                       theGoober.goto(coordinates[checkedSquares[i][0]][checkedSquares[i][1]])
                       monsterRow = checkedSquares[i][0]
                       monsterCol = checkedSquares[i][1]
                       mywindow.update()
                   elif parentSquares[k] != [monsterRow,monsterCol]:
                       movetheMonster(parentSquares[k][0], parentSquares[k][1])
 
initialScreenSetup()
loadMap('D:\\Programs by me\\CP12\\pathfindingmap.txt')
drawBoard()  # choose the theMap to load
# ---------------------------and create the player's sprite-----------
me = turtle.Turtle()
me.speed(0)
me.penup()
me.shape('square')
me.turtlesize(squareSize / 20, squareSize / 20)
me.fillcolor('green')
me.goto(coordinates[meRow][meCol])
 
theGoober = turtle.Turtle()
theGoober.speed(0)
theGoober.penup()
theGoober.shape('square')
theGoober.turtlesize(squareSize / 20, squareSize / 20)
theGoober.fillcolor('orange')
theGoober.goto(coordinates[monsterRow][monsterCol])
mywindow.update()
monsterSearch()
# -----------------------keyboard and mouse handling events---------------------
mywindow.listen()
mywindow.onkey(leave, 'q')
mywindow.onkey(goRight, 'd')
mywindow.onkey(goLeft, 'a')
mywindow.onkey(goUp, 'w')
mywindow.onkey(goDown, 's')
mywindow.mainloop()
 
 
 
 
 
