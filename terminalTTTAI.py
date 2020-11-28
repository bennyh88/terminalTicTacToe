#!/usr/bin/env python3
import re
import random

def drawGrid():
    spaceList = [0, 1, 3, 4, 6, 7]
    newLineList = [2, 5]
    string = "   a   b   c \n1  "

    for index in range(0, 9):
        string = string + grid[index] + " "
        if index in spaceList:
            string = string + "| "
        if index in newLineList:
            string = string + "\n   - + - + -"
            x = newLineList.index(index)
            x = x + 2
            string = string + "\n" + str(x) + "  "

    print("\n" + string)

def startGame():
    response = input("Would you like to play Tic-Tac-Toe? Y or N \n")
    if response == "Y" or response == "y":
        global grid
        grid = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        drawGrid()
    elif response == "N" or response == "n":
        exit()
    else:
        startGame()

def getInput():
    response = input("Choose a square, eg b3 \n")
    response = getSquareFromResponse(response)
    if response != None:
        letter = response[0]
        number = response[1]
        print("you input " + letter + ", " + number)
        makeMove(letter, number)
    else:
        print("Sorry, your input was not recognised")
        getInput()


def getSquareFromResponse(response):
    if len(response) >= 2:
        response = response.lower()

        letter = re.search("[abc]", response)
        if letter == None:
            return None
        letter = response[letter.start()]
        #print(letter)

        number = re.search("[123]", response)
        if number == None:
            return None
        number = response[number.start()]
        #print(number)

        response = [letter, number]
        return response
    else:
        return None

def findGridIndex(letter, number):
    #print("Letter = " + letter)
    letters = []
    if letter == "a":
        letters = [0, 3, 6]
    elif letter == "b":
        letters = [1, 4, 7]
    else:
        letters = [2, 5, 8]

    #print("Number = " + number)
    numbers = []
    if number == "1":
        numbers = [0, 1, 2]
    elif number == "2":
        numbers = [3, 4, 5]
    else:
        numbers = [6, 7, 8]

    for index in letters:
        if index in numbers:
            print("Grid Index = " + str(index))
            return index

def makeMove(letter, number):
    index = findGridIndex(letter, number)
    if grid[index] != " ":
        print("Square " + letter + ", " + number + " is already occupied!")
        getInput()
    else:
        grid[index] = "X"

def randomMove():
    x = 1
    while x == 1:
        index = random.randint(0, 8)
        if grid[index] == " ":
            grid[index] = "O"
            x = 0

def movesRequired(pattern, spaceString):
    movesString = binaryAND(pattern, spaceString)
    movesRequired = 0;
    for bit in range(0,9):
        if movesString[bit] == "1":
            movesRequired += 1
    return movesRequired

corners = [0, 2, 6, 8]

def computerMove():
    move = findWinningMoves("O")
    if move == 100:
        move = findWinningMoves("X")
        if move == 100:
            if cornersEmpty(): #if all corners are free, pick corner
                x = random.randint(0, len(corners)-1)
                x = corners[x]
                grid[x] = "O"
            elif grid[4] == " ": #else if center is free, take it
                grid[4] = "O"
            else:
                randomMove()
        else:
            grid[move] = "O"
    else:
        grid[move] = "O"


def findWinningMoves(player):
    #look for spaces
    spaceString = ""
    for cell in grid: #for every cell in the grid, if the cell is vacant
        if cell == " ":
            spaceString = spaceString + "1"
        else:
            spaceString = spaceString + "0"
    #print("spaceString " + spaceString) #010101010
    gridString = ""
    for cell in grid: #for every cell in the grid, if there cell is filled by player, add a 1, else add 0
        if cell == player:
            gridString = gridString + "1"
        else:
            gridString = gridString + "0"
    #print("gridString " + gridString) #001010000

    #010101010 spaceString
    #001010000 gridString
    #011111010 OR

    orString = binaryOR(spaceString, gridString)

    #011111010 OR
    #000111000 a possible winning pattern
    #000111000 AND ( OR logically AND with possible pattern if pattern & AND are the same then we have a candidate)

    #010101010 space
    #000111000 a possible winning pattern
    #000101000 AND moves required for this winning combo

    for pattern in winningPatterns:
        if pattern == binaryAND(pattern, orString):
            #print("pattern = " + pattern)
            if movesRequired(pattern, spaceString) == 1: #winning move found
                move = getMove(pattern, spaceString)
                return move

    return 100

def cornersEmpty():
    for index in corners:
        if grid[index] != " ":
            return False
    return True

winningPatterns = [ "111000000", "000111000", "000000111", "100100100",
                    "010010010", "001001001", "100010001", "001010100"]
def detectWin(player): #string, either "O", or "X"
    if " " in grid: #if theres spaces then game has not ended in a tie
        gridString = ""
        for cell in grid: #for every cell in the grid, if there cell is filled by player, add a 1, else add 0
            if cell == player:
                gridString = gridString + "1"
            else:
                gridString = gridString + "0"

        #take our gridString representing the current grid, and compare it to all possible winningPatterns
        for pattern in winningPatterns:
            resultString = binaryAND(gridString, pattern)
            if resultString == pattern:
                print(player + " Won!")
                startGame()
    else:
        print("It's a draw")
        startGame()

def binaryAND(gridString, winString):
    resultString = ""
    for bit in range(0,9):
        if gridString[bit] == "1" and winString[bit] == "1":
            resultString = resultString + "1"
        else:
            resultString = resultString + "0"
    return resultString

def binaryOR(string1, string2):
    resultString = ""
    for bit in range(0,9):
        if string1[bit] == "1" or string2[bit] == "1":
            resultString = resultString + "1"
        else:
            resultString = resultString + "0"
    return resultString

def getMove(pattern, spaceString):
    for bit in range(0,9):
        if pattern[bit] == "1" and spaceString[bit] == "1":
            return bit
    print("ERROR IN getMove()")


grid = []
startGame()


x = 1
while x == 1:
    getInput()
    drawGrid()
    detectWin("X")
    computerMove()
    drawGrid()
    detectWin("O")
