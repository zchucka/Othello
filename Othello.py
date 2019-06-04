import sys
sys.path.append('C:\\Users\\zchuc\\Appdata\\Roaming\\Python\\Python27\\site-packages')

import numpy as np
import threading
import time

'''
Class: CPSC 427
Team Member: Zachary Chucka
Submitted By: Zachary Chucka
GU Username: zchucka
File Name: proj13.py
uses an AB pruning function to sort through a created tree
using the minmax method of adversarial gaming, min tries to minimize the score of
the max player (the AI) while the AI tries to maximize his own score
The score function calculates what min and max are battling over:
    -it the score and other factors which help in the game to create the score
The AB function uses recursion and calls either the min or max player based on whos
turn it is and then continues until the depth bound
'''

class Othello:
    def __init__(self):
        self.board = np.empty((8, 8), dtype= 'str')
        self.changesBoard = np.empty((8, 8), dtype= 'str')
    
    #making the eight by eight matrix
    def makingTheBoard(self, isReversed):
        self.board[:] = ' '
        self.changesBoard[:] = ' '
        if not isReversed:
            self.board[4][3] = 'B'
            self.board[3][4] = 'B'
            self.board[3][3] = 'W'
            self.board[4][4] = 'W'
            self.changesBoard[4][3] = 'B'
            self.changesBoard[3][4] = 'B'
            self.changesBoard[3][3] = 'W'
            self.changesBoard[4][4] = 'W'
        else:
            self.changesBoard[4][3] = 'W'
            self.changesBoard[3][4] = 'W'
            self.changesBoard[3][3] = 'B'
            self.changesBoard[4][4] = 'B'
            self.board[4][3] = 'W'
            self.board[3][4] = 'W'
            self.board[3][3] = 'B'
            self.board[4][4] = 'B'

    #prints the board more naturally
    def displayTheBoard(self, numB, numW):
        print('    A   B   C   D   E   F   G   H   ')
        for x in range(8):
            print(x + 1),
            for y in range(8):
                print('|'),
                if self.board[x][y] != self.changesBoard[x][y]:
                    print('X'),
                else:
                    print(self.board[x][y]),
            print('|')
        print("White: " + str(numW))
        print("Black: " + str(numB))

    # counts the amount of Bs and Ws returns it as a tuple
    # returns W number then the B number
    def countTheNumber(self):
        numberW = 0
        numberB = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 'B':
                    numberB = numberB + 1
                elif self.board[x][y] == 'W':
                    numberW = numberW + 1
        return numberW, numberB

    #if shouldKeep is true, the changes board is updated
    #if not, the board is reverted back
    def keepChanges(self, shouldKeep):
        if shouldKeep:
            for x in range(8):
                for y in range(8):
                    self.changesBoard[x][y] = self.board[x][y]
        else:
            for x in range(8):
                for y in range(8):
                    self.board[x][y] = self.changesBoard[x][y]
            
    #checks the move to make sure its valid
    def isValidMove(self, x, y, player):
        #checks to make sure no piece is there
        if self.board[x][y] != ' ':
            return False
        elif self.checkHorizontal(x, y, player):
            return True
        elif self.checkVertical(x, y, player):
            return True
        elif self.checkDiagnol(x, y, player):
            return True
        else:
            return False

    #checks if the move is valid in the horizontal direction
    def checkHorizontal(self, x, y, player):
        if player == 'B':
            if y > 1 and self.board[x][y-1] == 'W': #left
                z = y - 1
                while z >= 0 and self.board[x][z] != ' ':
                    if self.board[x][z] == 'B':
                        return True
                    z = z - 1
            if y < 7 and self.board[x][y+1] == 'W': #right
                z = y + 1
                while z < 8 and self.board[x][z] != ' ':
                    if self.board[x][z] == 'B':
                        return True
                    z = z + 1
        elif player == 'W':
            if y > 1 and self.board[x][y-1] == 'B': #left
                z = y - 1
                while z >= 0 and self.board[x][z] != ' ':
                    if self.board[x][z] == 'W':
                        return True
                    z = z - 1
            if y < 7 and self.board[x][y+1] == 'B': #right
                z = y + 1
                while z < 8 and self.board[x][z] != ' ':
                    if self.board[x][z] == 'W':
                        return True
                    z = z + 1

    #checks if the move can be played in the vertical direction
    # x and y are swapped because the matrix to me seems backwards due to how I display it--realized later
    #     and I kept messing up the calls
    def checkVertical(self, x, y, player):
        if player == 'B':
            if x > 1 and self.board[x-1][y] == 'W': # above
                z = x - 1
                while z >= 0 and self.board[z][y] != ' ':
                    if self.board[z][y] == 'B':
                        return True
                    z = z - 1
            if x < 7 and self.board[x+1][y] == 'W': # below
                z = x + 1
                while z < 8 and self.board[z][y] != ' ':
                    if self.board[z][y] == 'B':
                        return True
                    z = z + 1
        elif player == 'W':
            if x > 1 and self.board[x-1][y] == 'B': #above
                z = x - 1
                while z >= 0 and self.board[z][y] != ' ':
                    if self.board[z][y] == 'W':
                        return True
                    z = z - 1
            if x < 7 and self.board[x+1][y] == 'B': #below
                z = x + 1
                while z < 8 and self.board[z][y] != ' ':
                    if self.board[z][y] == 'W':
                        return True
                    z = z + 1

    #checks the diagnol if possible
    # x and y are swapped because the matrix to me seems backwards to how I display it -- realized later
    #     and I kept messing up the calls
    def checkDiagnol(self, x, y, player):
        if player == 'B':
            if y > 1 and x > 1 and self.board[x-1][y-1] == 'W': #minus both
                w = x - 1
                z = y - 1
                while z >= 0 and w >= 0 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'B':
                        return True
                    w = w - 1
                    z = z - 1
            if y < 7 and x < 7 and self.board[x+1][y+1] == 'W': # plus both
                z = y + 1
                w = x + 1
                while z < 8 and w < 8 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'B':
                        return True
                    w = w + 1
                    z = z + 1
            if y < 7 and x > 1 and self.board[x-1][y+1] == 'W': #plus y minus x
                z = y + 1
                w = x - 1
                while z < 8 and w >= 0 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'B':
                        return True
                    z = z + 1
                    w = w - 1
            if x < 7 and y > 1 and self.board[x+1][y-1] == 'W': # plus x minus y
                z = y - 1
                w = x + 1
                while z >= 0 and w < 8 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'B':
                        return True
                    z = z - 1
                    w = w + 1
        elif player == 'W':
            if y > 1 and x > 1 and self.board[x-1][y-1] == 'B': #minus both
                z = y - 1
                w = x - 1
                while z >= 0 and w >= 0 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'W':
                        return True
                    w = w - 1
                    z = z - 1
            if y < 7 and x < 7 and self.board[x+1][y+1] == 'B': #plus both
                z = y + 1
                w = x + 1
                while z < 8 and w < 8:
                    if self.board[w][z] == 'W':
                        return True
                    z = z + 1
                    w = w + 1
            if y < 7 and x > 1 and self.board[x-1][y+1] == 'B': #plus y minus x
                z = y + 1
                w = x - 1
                while z < 8 and w >= 0 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'W':
                        return True
                    z = z + 1
                    w = w - 1
            if y > 1 and x < 7 and self.board[x+1][y-1] == 'B': # plus x minus y
                z = y - 1
                w = x + 1
                while z >= 0 and w < 8 and self.board[w][z] != ' ':
                    if self.board[w][z] == 'W':
                        return True
                    z = z - 1
                    w = w + 1

    #places the piece in the location for the specified team
    # x and y are swapped because the matrix to me seems backgrounds
    #     and I kept messing up the calls
    def placePiece(self, player, y, x):
        self.board[x][y] = player
        self.fixTheBoard(y, x)

    # fixes the tiles that need to be replaced
    # x and y are swapped because the matrix to me seems backgrounds
    #     and I kept messing up the calls. Long term- i regret this decision
    def fixTheBoard(self, y, x):
        player = self.board[x][y]
        if self.checkDiagnol(x, y, self.board[x][y]): #fix the diagnol pieces
            if y > 1 and x > 1 and self.board[x-1][y-1] != player and self.board[x-1][y-1] != ' ': #minus both
                z = x - 1
                w = y - 1
                while z >= 0 and w >= 0 and self.board[z][w] != ' ':
                    if self.board[z][w] == player:
                        self.replaceTiles(x, y, w, z)
                        w = -100 #exits loop
                    w = w - 1
                    z = z - 1
            if y < 7 and x < 7 and self.board[x+1][y+1] != player and self.board[x+1][y+1] != ' ': # plus both
                w = y + 1
                z = x + 1
                while z < 8 and w < 8 and self.board[z][w] != ' ':
                    if self.board[z][w] == player:
                        self.replaceTiles(x, y, w, z)
                        w = 10 #exits loop
                    w = w + 1
                    z = z + 1
            if y < 7 and x > 1 and self.board[x-1][y+1] != player and self.board[x-1][y+1] != ' ': #plus y minus x
                w = y + 1
                z = x - 1
                while w < 8 and z >= 0 and self.board[z][w] != ' ':
                    if self.board[z][w] == player:
                        self.replaceTiles(x, y, w, z)
                        w = 10 #exits loop
                    z = z - 1
                    w = w + 1
            if y > 1 and x < 7 and self.board[x+1][y-1] != player and self.board[x+1][y-1] != ' ':# plus x minus y
                w = y - 1
                z = x + 1
                while w >= 0 and z < 8 and self.board[z][w] != ' ':
                    if self.board[z][w] == player:
                        self.replaceTiles(x, y, w, z)
                        w = -100 #exits loop
                    z = z + 1
                    w = w - 1
        if self.checkVertical(x, y, self.board[x][y]): #fix the vertical pieces
            if x > 1 and self.board[x-1][y] != player and self.board[x-1][y] != ' ': #checks above
                z = x - 1
                while z >= 0 and self.board[z][y] != ' ':
                    if self.board[z][y] == player:
                        self.replaceTiles(x, y, -1, z)
                        z = -1 #exits the loop
                    z = z - 1
            if x < 7 and self.board[x+1][y] != player and self.board[x+1][y] != ' ': #checks below
                z = x + 1
                while z <= 7 and self.board[z][y] != ' ':
                    if self.board[z][y] == player:
                        self.replaceTiles(x, y, -1, z)
                        z = 10 #exits the loop
                    z = z + 1
        if self.checkHorizontal(x, y, self.board[x][y]): #fix the horizontal pieces
            # check to the left (less than the x)
            if y > 1 and self.board[x][y-1] != player and self.board[x][y-1] != ' ':
                w = y - 1
                while w >= 0 and self.board[x][w] != ' ':
                    if self.board[x][w] == player:
                        self.replaceTiles(x, y, w, -1)
                        w = -1 #exits the loop
                    w = w - 1
            if y < 7 and self.board[x][y+1] != player and self.board[x][y+1] != ' ':
                w = y + 1
                while w <= 7 and self.board[x][w] != ' ':
                    if self.board[x][w] == player:
                        self.replaceTiles(x, y, w, -1)
                        w = 10 #exits the loop
                    w = w + 1
                    
    # replacing the tiles if it is a valid play
    # if w or z are equal to -1, their is no variable
    # z coorelates with x and w coorelates with y
    def replaceTiles(self, x, y, w, z):
        if w == -1 and z == -1:
            print("something broke")
        elif w == -1: #x case
            if z > x:
                while z > x:
                    self.board[z][y] = self.board[x][y]
                    z = z - 1
            elif z < x:
                while z < x:
                    self.board[z][y] = self.board[x][y]
                    z = z + 1
        elif z == -1: #y case
            if w < y:
                while w < y:
                    self.board[x][w] = self.board[x][y]
                    w = w + 1
            elif w > y:
                while w > y:
                    self.board[x][w] = self.board[x][y]
                    w = w - 1
        else: #diagnol case
            if w > y and z > x: #both greater
                while z > x: # we only need to track one since they will both increment at the same time
                    self.board[z][w] = self.board[x][y]
                    z = z - 1
                    w = w - 1
            if w > y and z < x: #w greater, z less
                while z < x:
                    self.board[z][w] = self.board[x][y]
                    z = z + 1
                    w = w - 1
            if w < y and z > x: # w less, z greater
                while z > x:
                    self.board[z][w] = self.board[x][y]
                    z = z - 1
                    w = w + 1
            if w < y and z < x: #both lesser
                while z < x:
                    self.board[z][w] = self.board[x][y]
                    z = z + 1
                    w = w + 1

class Game:
    def __init__(self):
        self.numW = 2
        self.numB = 2
        self.board = Othello()
        self.isOutOfTime = False
        self.isPlayerBlack = True

    #initializes the game loop settings
    def startGame(self):
        print("Welcome to Othello")
        isReversed = raw_input("Is the board reversed? (y/n) ")
        if isReversed == 'y':
            self.initGame(True)
        elif isReversed == 'n':
            self.initGame(False)
        else:
            print("invalid input") #protect better later
        
        isPlayerBlackraw = raw_input("Will the user be black? (t/f) ")
        if isPlayerBlackraw == 't':
            #doesn't matter with the AI not implemented
            print('player is black')
            self.isPlayerBlack = True
        elif isPlayerBlackraw == 'f':
            print('player is white')
            self.isPlayerBlack = False
        else:
            print("invalid input")
        
        #black goes first
        #player is placed against the computer
        #start the game loop here, continuing until the end conditions are met
        self.gameLoop()
        #returns here and asks if the user wants to play again. resets board and counts

    # initializes the game board
    def initGame(self, isReversed):
        self.board.makingTheBoard(isReversed)

    #checks if the game is over by seeing if there is no moves left for a character or if the board is full
    def isGameOver(self):
        if self.numB == 0 or self.numW == 0:
            return True
        elif self.numB + self.numW == 64:
            return True
        else:
            return False
    
    #runs the game, continues until isGameOver returns ture
    def gameLoop(self):
        playerQuits = False
        if self.isPlayerBlack:
            isPlayerTurn = True
        else:
            isPlayerTurn = False
        while not self.isGameOver() and not playerQuits:
            if isPlayerTurn:
                print("Player's Turn!")
                self.board.displayTheBoard(self.numB, self.numW) #display the board before the moves
                print("enter 'q' to quit")
                location = raw_input("Where would you like to place your piece? (ex. A,2 or n) ") #ask the user what move he wants to make
                pieces = location.split(',')
                isValidMove = False
                if pieces[0] <= 'H' and pieces[0] >= 'A' and int(pieces[1]) <= 8 and int(pieces[1]) >= 1:
                    x = int(ord(pieces[0]) - ord('A'))
                    y = int(pieces[1]) - 1
                    if self.isPlayerBlack:
                        isValidMove = self.board.isValidMove(y, x, 'B')
                    else:
                        isValidMove = self.board.isValidMove(y, x, 'W')
                elif (str(pieces[0]) == 'q'):
                    playerQuits = True
                elif (str(pieces[0]) == 'n'):
                    print("no valid moves, end of turn")
                    isPlayerTurn = False
                else:
                    print("invalid input")

                yOrN = 'n'
                if isValidMove:
                    print(location + ' is a valid move')
                    if self.isPlayerBlack:
                        self.board.placePiece('B', x, y)
                    else:
                        self.board.placePiece('W', x, y)
                    self.numW, self.numB = self.board.countTheNumber()
                    self.board.displayTheBoard(self.numB, self.numW)
                    yOrN = raw_input("Are you sure you want to place your piece at " + location + "? (y/n) ") #ask the user to confirm the move
                    if yOrN == 'y':
                        isPlayerTurn = not isPlayerTurn #change the players turn
                        self.board.keepChanges(True)
                        #recount the number of B's and W's at the end of the round
                    else:
                        self.board.keepChanges(False)
                        self.numW, self.numB = self.board.countTheNumber()
                        self.board.displayTheBoard(self.numB, self.numW)
                else:
                    #go through the loop again
                    print("move canceled because of an invalid move")
                    print("")
            else:
                print("AI's Turn!")
                timer = TimerClass()
                timer.start()

                treeDict = {}
                #forms the tree to the specified depthBound - based purely on time
                if self.isPlayerBlack:
                    treeDict = self.formTree(4, False)
                else:
                    treeDict = self.formTree(4, True)

                if treeDict[(-1, -1, -10, -10)] == []:
                    print("no moves found")
                else:
                    #trim tree at this point
                    selection = self.pruneTree(treeDict, (-1, -1, -10, -10), None, None)

                    #redisplays the scoreboard
                    if self.isPlayerBlack:
                        self.board.placePiece('W', selection[0], selection[1])
                    else:
                        self.board.placePiece('B', selection[0], selection[1])
                        
                    self.numW, self.numB = self.board.countTheNumber()
                    self.board.displayTheBoard(self.numB, self.numW)
                    
                    #AI figures move and asks the user to confirm
                    #for now, we will hardcode a single answer since I think that is what he wants
                    answer = raw_input("How about (" + chr(selection[0]+ ord('A')) + ',' + str(selection[1] + 1) + ") (y/n) ")
                    if str(answer) == 'y':
                        timer.stop()
                        self.board.keepChanges(True)
                    else:
                        #testing for the timer if the variable doesn't work
                        #need something to be in the while loop to not have indent problems so
                        self.board.keepChanges(False)
                        while (timer.isRunning):
                            uselessVariable = 2
                        #reattempt to find a new move
                        print("AI loses")
                        playerQuits = True
                    
                isPlayerTurn = not isPlayerTurn
                #recounts the scores in case it fails
                self.numW, self.numB = self.board.countTheNumber()
                
        #end of the game loop means the game is over
        print('Game over'),
        if self.numB > self.numW:
            print("the black team wins")
        elif self.numW > self.numB:
            print("the white team wins")
        elif self.numW == self.numB:
            print("- tie")
        else:
            print("Im not supposed to be here and im scared")
        self.board.displayTheBoard(self.numB, self.numW)

    #finds possible moves for the gameBoard at a given moment
    def findPossibleMoves(self, testGame, isBlackTurn):
        arrayOfSuccess = []
        for x in range(8):
            for y in range(8):
                if isBlackTurn:
                    if testGame.isValidMove(x, y, 'B'):
                        arrayOfSuccess.append((y, x, 0))
                else:
                    if testGame.isValidMove(x, y, 'W'):
                        arrayOfSuccess.append((y, x, 0))
        return arrayOfSuccess

    # recurvisevly calls to build and return the tree
    def buildTree(self, depthBound, currDepth, isBlackTurn, tree, currGame, currNode):
        tempGame = Othello()
        tempNodes = self.findPossibleMoves(currGame, isBlackTurn)

        if currDepth < depthBound and tempNodes != []: #different if close depth bound since we need the scores
            # builds the game to be matched to the current state
            for x in range(8):
                for y in range(8):
                    tempGame.board[x][y] = currGame.board[x][y]

            # placing the current node in the board
            if isBlackTurn:
                tempGame.placePiece('B', currNode[0], currNode[1])
            else:
                tempGame.placePiece('W', currNode[0], currNode[1])
            
            # get the scores for node
            tempArray = []
            tempGame.keepChanges(True)
            
            # loops through children and finds the score
            for child in tempNodes:
                if self.isPlayerBlack == True:
                    tempGame.placePiece('W', child[0], child[1])
                    w, b = tempGame.countTheNumber()
                    score = self.scoreMove(w, b, False, child, tempGame)
                    child = (child[0], child[1], score, 0) # first two are coords, third is the score, fourth is to deal with duplicates
                else:
                    tempGame.placePiece('B', child[0], child[1])
                    w, b = tempGame.countTheNumber()
                    score = self.scoreMove(w, b, True, child, tempGame)
                    child = (child[0], child[1], score, 0) 

                # if there is a duplicate, we add to the last number    
                while child in tree:
                    child = (child[0], child[1], child[2], child[3] + 1)
                
                tempArray.append(child)
                self.buildTree(depthBound, currDepth + 1, not isBlackTurn, tree, tempGame, child)
                tempGame.keepChanges(False)
            tree[currNode] = tempArray


    # scores the move in order to determine the function and returns said score
    # player wants to minimize the score so better moves subtract from score instead of add
    def scoreMove(self, w, b, isBlackTurn, node, gameState):
        score = 0
        # the percentage of pieces that change
        if self.isPlayerBlack:
            score = float(w)/ (w + b)
        else:
            score = float(b) / (w + b)
            
        #checks if its a corner piece (1 if yes, 0 if no, .5 if edge)
        if node[0] == 0 or node[0] == 7:
            if node[1] == 0 or node[1] == 7:
                if self.isPlayerBlack and isBlackTurn:
                    score = score - 1
                elif not self.isPlayerBlack and not isBlackTurn:
                    score = score - 1
                else:
                    score = score + 1
            else:
                if self.isPlayerBlack and isBlackTurn:
                    score = score - .5
                elif not self.isPlayerBlack and not isBlackTurn:
                    score = score - .5
                else:
                    score = score + .5
        elif node[1] == 0 or node[1] == 7:
            if self.isPlayerBlack and isBlackTurn:
                score = score - .5
            elif not self.isPlayerBlack and not isBlackTurn:
                score = score - .5
            else:
                score = score + .5

        #checks if danger zone (pieces that touch corners)
        if self.isInDangerZone(node):
            if self.isPlayerBlack and isBlackTurn:
                score = score + 1
            elif not self.isPlayerBlack and not isBlackTurn:
                score = score + 1
            else:
                score = score - 1

        return score
        
    # checks if the pieces lead to the corner being chosen
    def isInDangerZone(self, node):
        if node[0] <= 1 and node[1] <= 1:
            if node[0] == 0 and node[1] == 0:
                return False
            else:
                return True
        elif node[0] >= 6 and node[1] >= 6:
            if node[0] == 7 and node[1] == 7:
                return False
            else:
                return True
        else:
            return False
                
                            
    # formulates the tree in a similar fashion to AB pruning example by dePalma
    # moves to the depth bound so that AB pruning may be used to make our move
    def formTree(self, depthBound, isAIBlack):
        #copies the current board to a board we can edit
        testGame = Othello()

        for x in range(8):
            for y in range(8):
                testGame.board[x][y] = self.board.board[x][y]

        testGame.keepChanges(True)
        # fills out the dictionary
        # since there is no root node technically, we will create one
        rootNode = (-1, -1, -10, -10)
        nodes = self.findPossibleMoves(testGame, isAIBlack)
        treeDictionary = {rootNode: nodes}
        #print(treeDictionary)
        for node in nodes:
            if isAIBlack:
                testGame.placePiece('B', node[0], node[1])
            else:
                testGame.placePiece('W', node[0], node[1])
            self.buildTree(depthBound, 1, not isAIBlack, treeDictionary, testGame, node)
            testGame.keepChanges(False)
        return treeDictionary

    # prunes the tree and returns the selection for the AI
    def pruneTree(self, graph, root, alpha, beta):
        node = self.AITurn(graph, root, alpha, beta)

        #back tracks to find the right move
        if node in graph[root]:
            return node
        else:
            while node not in graph[root]:
                for key in graph:
                    if node in graph[key]:
                        node = key
        return answer

    # runs for the AI's turn to help pruneTree
    def AITurn(self, graph, node, alpha, beta):
        v = node
        if node not in graph:
            return node
        for child in graph.get(node):
            v1 = self.playerTurn(graph, child, alpha, beta)
            if v1[2] > v[2]:
                v = v1
            if beta is not None and v1[2] >= beta[2]:
                return v
            if alpha is None or v1[2] > alpha[2]:
                alpha = v1
        return v

    # runs for the player's turn to help pruneTree
    def playerTurn(self, graph, node, alpha, beta):
        v = node
        if node not in graph:
            return node
        for child in graph.get(node):
            v1 = self.AITurn(graph, child, alpha, beta)
            if v1[2] < v[2]:
                v = v1
            if alpha is not None and v1[2] <= alpha[2]:
                return v
            if beta is None or v1[2] < beta[2]:
                beta = v1
        return v

# class that defines the timer used during the game loop
class TimerClass(threading.Thread):
    isRunning = False

    #initializes the timer object
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 10

    #starts the timer
    def run(self):
        self.isRunning = True
        while self.count > 0 and not self.event.is_set():
            print self.count
            self.count -= 1
            self.event.wait(1)
        self.stop()

    #stops the timer
    def stop(self):
        self.isRunning = False
        self.event.set()
        
def main():
    newGame = Game()
    newGame.startGame()
    
main()

