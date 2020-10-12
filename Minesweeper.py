import random

class Square:
    def __init__(self, loc, char, value, flagged):
        self.loc = loc
        self.char = char
        self.value = value
        self.flagged = flagged

    def changeChar(self, newChar):
        self.char = newChar

    def incrementValue(self):
        self.value += 1

    def setMine(self):
        self.value = 9

    def giveValue(self):
        return self.value

    def giveGraphic(self):
        return self.char

    def giveLoc(self):
        return self.loc

    def placeFlag(self):
        self.flagged = True

    def removeFlag(self):
        self.flagged = False

    def giveFlag(self):
        return self.flagged

class Board:
    def __init__(self, width, length):
        #to create square board set length = to 2 * width + 2
        self.width = width
        self.length = length
        self.squares = []

    def setBoard(self):
        # instantiates a new Square object for each tile on the board
        for row in range((self.length - 2) // 2):
            for column in range(self.width):
                self.squares.append(Square((column + 1, row + 1), ' ', 0, False))

    def printBoard(self, char):
        #prints a grid based board using the width and length of the Board object and a given character
        for row in range(self.length):
            for column in range(self.width):
                if row == 0:
                    if column == 0:
                        print('     ' + str(column + 1) + '    ', end = '')
                    else:
                        print('   ' + str(column + 1) + '    ', end='')
                elif (row + 1) % 2 == 0:
                    if column == 0:
                        print('  ' + char + ' ' + char + ' ' + char + ' ' + char, end=' ')
                    else:
                        print(char + ' ' + char + ' ' + char + ' ' + char, end = ' ')
                else:
                    if column == 0:
                        print(str(int(row / 2)) + ' ' + char + '  ' + str(self.squares[(((row - 2) // 2) * self.width + (column + 1)) - 1].giveGraphic()) + '  ' + char, end=' ')
                    else:
                        print(char + '  ' + str(self.squares[(((row - 2) // 2) * self.width + (column + 1)) - 1].giveGraphic()) + '  ' + char, end=' ')
            print()

class Minesweeper(Board):
    def __init__(self, width, length):
        super().__init__(width, length)
        self.rows = (length - 2) // 2
        self.visited = set()

    def appendVisited(self, newValue):
        self.visited.add(newValue)

    def setMines(self):

        def setAdjacentMines(eligibleSquares):
            for eligibleSquare in eligibleSquares:
                if eligibleSquare.giveValue() == 9:
                    self.squares[i].incrementValue()

        for square in self.squares:
            if random.randint(1, 100) >= 88:
                square.setMine()
        for i in range(len(self.squares)):
            if self.squares[i].giveValue() != 9:
                #top left corner
                if i == 0:
                    setAdjacentMines([self.squares[i + 1], self.squares[i + self.width], self.squares[i + 1 + self.width]])
                #top right corner
                elif i == self.width - 1:
                    setAdjacentMines([self.squares[i - 1], self.squares[i - 1 + self.width], self.squares[i + self.width]])
                #bottom left corner
                elif i == self.width * self.rows - self.width:
                    setAdjacentMines([self.squares[i - self.width], self.squares[i + 1 - self.width], self.squares[i + 1]])
                #bottom right corner
                elif i == self.width * self.rows - 1:
                    setAdjacentMines([self.squares[i - 1 - self.width], self.squares[i - self.width], self.squares[i - 1]])
                #top row
                elif 0 < i < self.width:
                    setAdjacentMines([self.squares[i - 1], self.squares[i + 1], self.squares[i - 1 + self.width],
                                      self.squares[i + self.width], self.squares[i + 1 + self.width]])
                #bottom row
                elif self.width * self.rows - self.width < i < self.width * self.rows:
                    setAdjacentMines([self.squares[i - 1 - self.width], self.squares[i - self.width],
                                      self.squares[i + 1 - self.width], self.squares[i - 1], self.squares[i + 1]])
                #left column
                elif i % self.width == 0:
                    setAdjacentMines([self.squares[i - self.width], self.squares[i + 1 - self.width], self.squares[i + 1],
                                      self.squares[i + self.width], self.squares[i + 1 + self.width]])
                #right column
                elif (i + 1) % self.width == 0:
                    setAdjacentMines([self.squares[i - 1 - self.width], self.squares[i - self.width], self.squares[i - 1],
                                      self.squares[i - 1 + self.width], self.squares[i + self.width]])
                #middle squares
                else:
                    setAdjacentMines([self.squares[i - 1 - self.width], self.squares[i - self.width],
                                      self.squares[i + 1 - self.width], self.squares[i - 1], self.squares[i + 1],
                                      self.squares[i - 1 + self.width], self.squares[i + self.width],
                                      self.squares[i + 1 + self.width]])

    def chainReaction(self, square):
        i = self.squares.index(square)

        def checkSurrondingSquares(eligibleSquares):
        #checks all the given surrounding squares of the square passed to chainReaction()
            for eligibleSquare in eligibleSquares:
                if eligibleSquare.giveValue() == 0:
                    eligibleSquare.changeChar('0')
                    self.appendVisited(square)
                    self.chainReaction(eligibleSquare)
                elif eligibleSquare.giveValue() < 9: #else does not work here because of a bug during recursion on the bottom row
                    eligibleSquare.changeChar(str(eligibleSquare.giveValue()))

            self.appendVisited(Square)

        if square not in self.visited:
            #top left corner
            if (square.giveLoc()[0], square.giveLoc()[1]) == (1, 1):
                checkSurrondingSquares([self.squares[i + 1], self.squares[i + self.width],
                                        self.squares[i + 1 + self.width]])
            #top right corner
            elif (square.giveLoc()[0], square.giveLoc()[1]) == (self.width, 1):
                checkSurrondingSquares([self.squares[i - 1], self.squares[i - 1 + self.width],
                                        self.squares[i + self.width]])
            #bottom left corner
            elif (square.giveLoc()[0], square.giveLoc()[1]) == (1, self.rows):
                checkSurrondingSquares([self.squares[i - self.width], self.squares[i + 1 - self.width],
                                        self.squares[i + 1]])
            #bottom right corner
            elif (square.giveLoc()[0], square.giveLoc()[1]) == (self.width, self.rows):
                checkSurrondingSquares([self.squares[i - 1 - self.width], self.squares[i - self.width],
                                        self.squares[i - 1]])
            #top row
            elif square.giveLoc()[1] == 1:
                checkSurrondingSquares([self.squares[i - 1], self.squares[i + 1], self.squares[i - 1 + self.width],
                                        self.squares[i + self.width], self.squares[i + 1 + self.width]])
            #bottom row
            elif square.giveLoc()[1] == self.rows:
                checkSurrondingSquares([self.squares[i - 1 - self.width], self.squares[i - self.width],
                                        self.squares[i + 1 - self.width], self.squares[i - 1],
                                        self.squares[i + 1]])
            #left column
            elif square.giveLoc()[0] == 1:
                checkSurrondingSquares([self.squares[i - self.width], self.squares[i + 1 - self.width],
                                        self.squares[i + 1], self.squares[i + self.width],
                                        self.squares[i + 1 + self.width]])
            #right column
            elif square.giveLoc()[0] == self.width:
                checkSurrondingSquares([self.squares[i - 1 - self.width], self.squares[i - self.width],
                                        self.squares[i - 1], self.squares[i - 1 + self.width],
                                        self.squares[i + self.width]])
            #middle squares
            else:
                checkSurrondingSquares([self.squares[i - 1 - self.width], self.squares[i - self.width],
                                        self.squares[i + 1 - self.width], self.squares[i - 1], self.squares[i + 1],
                                        self.squares[i - 1 + self.width], self.squares[i + self.width],
                                        self.squares[i + 1 + self.width]])

    def guess(self, coord):
        #checks if user input is a mine, change the square's character appropriately, and removes that squares class from the list
        for square in self.squares:
            loc = square.giveLoc()
            if loc == coord:
                if square.giveValue() == 0:
                    square.changeChar(square.giveValue())
                    print('Clear')
                    self.chainReaction(square)
                    return True
                elif square.giveValue() < 9:
                    square.changeChar(square.giveValue())
                    return True
                else:
                    square.changeChar('!')
                    print('Mine!\nGame Over')
                    return False

    def flag(self, coord, flagMode):
        for square in self.squares:
            loc = square.giveLoc()
            if loc == coord:
                if flagMode == 'p':
                    square.placeFlag()
                    square.changeChar('F')
                else:
                    square.removeFlag()
                    square.changeChar(' ')

    def victory(self):
        emptySquares = []
        for square in self.squares:
            if square.giveValue() != 9:
                emptySquares.append(square)
        if all(square.giveGraphic() != ' ' for square in emptySquares):
            self.printBoard('#')
            print('You win!')
            return False
        else:
            return True

def main():
    m = Minesweeper(9, 20)
    m.setBoard()
    m.setMines()
    alive = True

    while alive:
        m.printBoard('X')
        inputMode = input("Would you like to input a flag? (y/n)")
        targetX = int(input("Enter x coord"))
        targetY = int(input("Enter y coord"))
        target = targetX, targetY
        if inputMode == 'y':
            flagMode = input('Would you like to remove (r) or place (p) a flag?')
            m.flag(target, flagMode)

        else:
            alive = m.guess(target)

        alive = m.victory()

main()