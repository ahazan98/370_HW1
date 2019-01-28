dim = 3

import random

#General Notes:
#I don't think we need the Tile class, it will make it simpler to index if we just make the board a nested list of strings
#I think it's better to have a Tile class, I'll explain why later.
#Is it slower to use a double list for our board than doing a single list indexed by arithmetic?
#Nah, same amount of assignments and comparisons algorithmically right?
class Tile:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val


class Node:
    def __init__(self, hCost, pCost, parent):
        self.hCost = hCost
        self.pCost = pCost
        self.tCost = self.hCost + self.pCost
        self.parent = parent
        self.board = [[0 for x in range(dim)] for y in range(dim)]
        self.eRow = 0
        self.eCol = 0
        for row in range(dim):
            for col in range(dim):
                c = Tile(row, col, " ")
                self.board[row][col] = c

    def __str__(self):
        string = ""
        for row in range(dim):
            temp = ""
            for col in range(dim):
                temp += "|" + self.board[row][col].val
            string += temp + "|\n"
        return string

    def makeRBoard(self):
        values = ["1","2","3","4","5","6","7","8"]
        random.shuffle(values)
        self.eRow = random.randint(1, dim + 1)
        self.eCol = random.randint(1, dim + 1)
        for row in range(dim):
            for col in range(dim):
                if(row != self.eRow) and (col != self.eCol):
                    self.board[row][col].val = values.pop()

    def makeBoard(self, values):
        i = 0
        for row in range(dim):
            for col in range(dim):
                if(values[i] == " "):
                    self.eRow = row
                    self.eCol = col
                self.board[row][col].val = values[i]
                i += 1

    #rudimentary make move funciton in a board. Requires that you know which tile you are moving.
    #Another approach to this would be tracking the empty spot and having an input for which direction you want a neighbor tile to move

    def showBoard(self):
        print(self)

    def getH(self, goalB):
        if(option == 1):
            count = 0
            for row in range(dim):
                for col in range(dim):
                    if goalB.board[row][col].val != " " and self.board[row][col].val != goalB.board[row][col].val:
                        count += 1
            return count

        elif(option == 2):
            count = 0
            init = Tile(0,0, " ")
            tilesCurr = [init for i in range((dim * dim) - 1)]
            tilesGoal = [init for i in range((dim * dim) - 1)]
            #or we could store the Tiles of the goal state and the board of the goal state as a global variable because itll be a stagnant
            #value that many of the functions are going to need.
            for row in range(dim):
                for col in range(dim):
                    tempCurr = self.board[row][col]
                    tempGoal = goalB.board[row][col]
                    if tempCurr.val != " ":
                        tilesCurr[int(tempCurr.val) - 1] = tempCurr;
                    if tempGoal.val != " ":
                        tilesGoal[int(tempGoal.val) - 1] = tempGoal;
            for i in range((dim * dim) - 1):
                count += abs(tilesCurr[i].row - tilesGoal[i].row)
                count += abs(tilesCurr[i].col - tilesGoal[i].col)

            return count

class pQueue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)

    def pop(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].tCost < self.queue[min].tCost:
                min = i
        pop = self.queue[min]
        del self.queue[min]
        return pop

class aStar:
    #probably a functions we need are: path cost calculator, next Tile generator, queue manipulator, heuristic calculator, showing Tiles
    def __init__(self, start, goal, option):
        self.start = start
        self.goal = goal
        self.queue = pQueue()
        self.option = option
        return

    def makeMove(self, node, dir):
        node.showBoard()
        temp = Node(0,0,None)
        temp.board = node.board

        if dir == 0: #0 = up
            if node.eRow + 1 < dim:
                temp.board[node.eRow][node.eCol].val = node.board[node.eRow + 1][node.eCol].val
                temp.board[node.eRow + 1][node.eCol].val = " "
            else:
                return None

        elif dir == 1: #1 = down
            if not(node.eRow - 1 < 0):
                temp.board[node.eRow][node.eCol].val = node.board[node.eRow - 1][node.eCol].val
                temp.board[node.eRow - 1][node.eCol].val = " "
            else:
                return None

        elif dir == 2: #2 = right
            if not(node.eCol - 1 < 0) :
                temp.board[node.eRow][node.eCol].val = node.board[node.eRow][node.eCol - 1].val
                temp.board[node.eRow][node.eCol - 1].val = " "
            else:
                return None

        elif dir == 3: #3 = left
            if node.eCol + 1 < dim :
                temp.board[node.eRow][node.eCol].val = node.board[node.eRow][node.eCol + 1].val
                temp.board[node.eRow][node.eCol + 1].val = " "
            else:
                return None

        return temp

    #simulation of heuristic one, don't know if this should be counted in our board class or should be a separate function

    def addChild(self, current):
        start = current
        for i in range(4):
            current = start
            temp = self.makeMove(current, i)
            #temp.showBoard()
            if(temp != None):
                # temp.pCost++
                # temp.hCost += temp.getH(self.goal)
                self.queue.insert(temp)

    def stage(self, current, goal):
        return


def main():
    test = Node(0,0,None)
    gTest = Node(0,0,None)
    testStart = ["7","2","4","5"," ","6","8","3","1"]
    testGoal = [" ","1","2","3","4","5","6","7","8"]
    test.makeBoard(testStart)
    gTest.makeBoard(testGoal)

    test.showBoard()
    gTest.showBoard()

    mTest = aStar(test, gTest, 1)

    mTest.addChild(test)

if __name__== "__main__":
    main()
