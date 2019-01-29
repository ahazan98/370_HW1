dim = 3

import random
import Queue
#board class and A* function, with init, make a move, is goal, shuffle, compares
#h1 and h2 are different functions, could be either
#General Notes:
#I don't think we need the Tile class, it will make it simpler to index if we just make the board a nested list of strings
#I think it's better to have a Tile class, I'll explain why later.
#Is it slower to use a double list for our board than doing a single list indexed by arithmetic?
#Nah, same amount of assignments and comparisons algorithmically right?

class Board:
    def __init__(self, values, pCost, hCost):
        self.values = values
        self.eRow = 0
        self.eCol = 0
        self.ePos = self.eRow * dim + self.eCol
        self.pCost = pCost
        self.hCost = hCost
        self.tCost = self.pCost + self.hCost

        for i in range(dim * dim):
            if self.values[i] == " ":
                self.eRow = i / dim

                self.eCol = (i % dim)
        # for row in range(dim):
        #     for col in range(dim):
        #         if values[i] == " ":
        #             self.eRow = row
        #             self.eCol = col
        #         self.values[row][col] = values[i]
        #         i += 1

    def __str__(self):
        string = ""
        for row in range(dim):
            temp = ""
            for col in range(dim):
                temp += "|" + self.values[(row * dim) + col]
            string += temp + "|\n"
        return string

    def showBoard(self):
        print(self)

    def isGoal(self, goal):
        for i in range(dim * dim):
            if self.values[i] != goal.values[i]:
                return False
        return True
        # for row in range(dim):
        #     for col in range(dim):
        #         if self.values[(row * dim) + col] != goal.values[(row * dim) + col]:
        #             return False
        #     return True

    def shuffleBoard(self):
        # values = ["1","2","3","4","5","6","7","8", " "]
        random.shuffle(self.values)
        for i in range(dim * dim):
            if self.values[i] == " ":
                self.eRow = i / dim
                self.eCol = i % dim
        # i = 0
        # for row in range(dim):
        #     for col in range(dim):
        #         if values[i] == " ":
        #             self.eRow = row
        #             self.eCol = col
        #         self.values[(row * dim) + col] = values[i]
        #         i += 1

def getH(current, goal, option):
    if(option == 1):
        count = 0
        for i in range(dim * dim):
            if current.values[i] != goal.values[i] and goal.values[i] != " ":
                count += 1
        return count

    elif(option == 2):
        count = 0
        currentDict = {}
        goalDict = {}
        for row in range(dim):
            for col in range(dim):
                currentDict[current.values[(row * dim) + col]] = [row, col]
                goalDict[goal.values[(row * dim) + col]] = [row, col]
        for i in range((dim * dim) - 1):
            index = str(i + 1)
            count += abs(currentDict[index][0] - goalDict[index][0]) + abs(currentDict[index][1] - goalDict[index][1])
    return count

def makeMove(board, dir):
#0 is up, 1 is down, 2 is right, 3 is left
#so I recreate the value list that is taken in Board to do the move, but I think this may be an expensive operation
    tempVals= [" " for i in range(dim * dim)]
    for row in range(dim):
        for col in range(dim):
            tempVals[row* dim + col] = board.values[(row * dim) + col]
    temp = Board(tempVals, board.pCost, board.hCost)
    #
    # print("board about to be moved")
    # temp.showBoard()
    if dir == 0: # up
        if temp.eRow + 1 < dim:
            #print(temp.values[temp.eRow + 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[((temp.eRow + 1) * dim) + temp.eCol]
            temp.values[((temp.eRow + 1) * dim) + temp.eCol] = " "
            temp.eRow += 1
            temp.pCost += 1
            #print(temp.eRow)
        else:
            return None
    if dir == 1: # down
        #print("moving down \n")
        if not(temp.eRow - 1 < 0):
            #print(temp.values[temp.eRow - 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[((temp.eRow - 1) * dim) + temp.eCol]
            temp.values[((temp.eRow - 1) * dim) + temp.eCol] = " "
            temp.eRow -= 1
            temp.pCost += 1
        else:
            return None
    if dir == 2: # right
        #print(temp.eRow, temp.eCol)
        if not(temp.eCol - 1 < 0):
            #print(temp.values[temp.eRow - 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[temp.eRow + ((temp.eCol - 1) * dim)]
            temp.values[temp.eRow + ((temp.eCol - 1) * dim)] = " "
            temp.eCol -= 1
            temp.pCost += 1
        else:
            return None
    if dir == 3: # left
        #print(temp.eRow, temp.eCol)
        if temp.eCol + 1 < dim:
            #print(temp.values[temp.eRow - 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[temp.eRow + ((temp.eCol + 1) * dim)]
            temp.values[temp.eRow + ((temp.eCol + 1) * dim)] = " "
            temp.eCol -= 1
            temp.pCost += 1
        else:
            return None
    return temp

def aStar(start, goal, option):
    frontier = Queue.PriorityQueue()
    explored = set()
    frontier.put((start.tCost, start))
    node = start
    j = 0
    while(not(frontier.empty())):
        node = frontier.get()[1]
        print("Stage: " + str(j))
        print(node)
        j += 1
        if(node.isGoal(goal)):
            return node
        explored.add(node) #if we go over class today how to prevent this nvm
        #creating possible successors from the node
        for i in range(4):
            #print("Child: " + str(i))
            tempBoard = Board(node.values, node.pCost, node.hCost) #do we need this line?
            #tempBoard.showBoard()
            childBoard = makeMove(tempBoard, i)
            #print(childBoard)
            if childBoard != None:
                if childBoard not in explored:
                    childBoard.hCost = getH(childBoard, goal, option)
                    childBoard.tCost = childBoard.pCost + childBoard.hCost
                    frontier.put((childBoard.tCost, childBoard))
    return None



def main():
    values = ["7","2","4","5"," ","6","8","3","1"]
    gValues = [" ","1","2","3","4","5","6","7","8"]
    testBoard = Board(values, 0, 0)
    goalBoard = Board(gValues, 0, 0)
    # testBoard.showBoard()
    # goalBoard.showBoard()
    # print(testBoard.isGoal(testBoard))
    # print(testBoard.eRow, testBoard.eCol)
    # print("modulo"+ str(2 % 3) + "\n")
    # testBoard.shuffleBoard()
    # testBoard.showBoard()
    # print(testBoard.eRow, testBoard.eCol)
    # print("moving up..\n")
    # moveBoard = makeMove(testBoard,0)
    # print("moved board\n")
    # moveBoard.showBoard()
    # print(moveBoard.eRow, moveBoard.eCol)
    # nextBoard = makeMove(moveBoard, 1)
    # print("board after move \n")
    # nextBoard.showBoard()
    print("Initial: ")
    print(testBoard)
    print("Final: ")
    final = aStar(testBoard , goalBoard, 1)
    print(final.pCost)



if __name__== "__main__":
    main()
