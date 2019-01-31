dim = 3
expNum = 1200
lim = 100

import random
import Queue
import math
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
            if self.values[i] == 0:
                self.eRow = i / dim
                self.eCol = (i % dim)
        # for row in range(dim):
        #     for col in range(dim):
        #         if values[i] == " ":
        #             self.eRow = row
        #             self.eCol = col
        #         self.values[row][col] = values[i]
        #         i += 1

    def __hash__(self):
        return hash(tuple(self.values))

    def __eq__(self, other):
        if(other == None):
            if type(self) == type(other):
                return True
            else:
                return False
        for i in range(dim * dim):
            if self.values[i] != other.values[i]:
                return False
        return True

    def __str__(self):
        string = ""
        for row in range(dim):
            temp = ""
            for col in range(dim):
                temp += "|" + str(self.values[(row * dim) + col])
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
            if self.values[i] == 0:
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
            if current.values[i] != goal.values[i] and goal.values[i] != 0:
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
            index = i + 1
            count += abs(currentDict[index][0] - goalDict[index][0]) + abs(currentDict[index][1] - goalDict[index][1])
    return count

def makeMove(board, dir):
#0 is up, 1 is down, 2 is right, 3 is left
#so I recreate the value list that is taken in Board to do the move, but I think this may be an expensive operation
    tempVals= [0 for i in range(dim * dim)]
    for row in range(dim):
        for col in range(dim):
            tempVals[row* dim + col] = board.values[(row * dim) + col]
    temp = Board(tempVals, board.pCost, board.hCost)
    # print("board about to be moved")
    # temp.showBoard()
    if dir == 0: # up
        if temp.eRow + 1 < dim:
            #print(temp.values[temp.eRow + 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[((temp.eRow + 1) * dim) + temp.eCol]
            temp.values[((temp.eRow + 1) * dim) + temp.eCol] = 0
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
            temp.values[((temp.eRow - 1) * dim) + temp.eCol] = 0
            temp.eRow -= 1
            temp.pCost += 1
        else:
            return None
    if dir == 2: # right
        #print(temp.eRow, temp.eCol)
        if not(temp.eCol - 1 < 0):
            #print(temp.values[temp.eRow - 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[(temp.eRow * dim) + (temp.eCol - 1)]
            temp.values[(temp.eRow * dim) + (temp.eCol - 1)] = 0
            temp.eCol -= 1
            temp.pCost += 1
        else:
            return None
    if dir == 3: # left
        #print(temp.eRow, temp.eCol)
        if temp.eCol + 1 < dim:
            #print(temp.values[temp.eRow - 1][temp.eCol])
            temp.values[(temp.eRow * dim) + temp.eCol] = temp.values[(temp.eRow * dim) + (temp.eCol + 1)]
            temp.values[(temp.eRow * dim) + (temp.eCol + 1)] = 0
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
    while(not(frontier.empty())):
        node = frontier.get()[1]
        if(node.isGoal(goal)):
            return [node, (len(explored) + frontier.qsize())]
        explored.add(node)
        for i in range(4):
            tempBoard = Board(node.values, node.pCost, node.hCost)
            childBoard = makeMove(tempBoard, i)
            if childBoard is not None:
                if childBoard not in explored:
                    childBoard.hCost = getH(childBoard, goal, option)
                    childBoard.tCost = childBoard.pCost + childBoard.hCost
                    frontier.put((childBoard.tCost, childBoard))
    return None
#we have a problem in random puzzle when we generate a faulty move because our makeMove returns None. The code below is an idea for a solution
#where we try to preserve a copy of the board before we try any move and maintain a set of illegal moves for that board, so that whenever we
#try to make an illegal move, we add that direction to the set and try a different move that could be legal. Another option which might be worth
#exploring is changing our makeMove function to just return the input board if you try to make a wrong move. We would have to alter some of our test
#cases, saying "if moveBoard == startBoard" instead of "if newBoard == None".
def randomPuzzle(start, depth):
    rBoard = Board(start.values, 0, 0)
    # #not using rNumDep right now
    # randVals = [2,4,6,8,10,12,14,16,18,20,22,24]
    # for i in finished:
    #     randVals.remove(i)
    # rNumSol = random.choice(randVals)
    visited = set()
    visited.add(rBoard)
    for i in range(depth):
        rNumDir = random.randint(0,3)
        #create a copy before making the move
        flag = False
        while(flag == False):
            temp = Board(rBoard.values, rBoard.pCost, rBoard.hCost)
            rBoard = makeMove(rBoard, rNumDir)
            if(rBoard != None):
                if rBoard not in visited:
                    flag = True
                    visited.add(rBoard)
                # flag = True
            else:
                rBoard = temp
                rNumDir = random.randint(0,3)
                        # while rBoard is not None:
        #     wrongDirs.add(rNumDir)
        #     newRNumDir = random.randint(0,4)
        #     if newRNumDir not in wrongDirs:
        #         safeBoard = makeMove(safeBoard, newRNumDir)
        #     else:
        #         wrongDirs.add(newRNumDir)
        # rBoard = safeBoard
    return rBoard

def checkFull(data):
    evens = [2,4,6,8,10,12,14,16,18,20,22,24]
    for i in evens:
        if len(data[i]) < 100:
            return False
    return True

#okay one problem here, you know how we asked about 1200 random puzzles we test? If you look at the reading
#it's 1200 random puzzles beacuse they did 100 puzzles at each depth from 2-24 going up even. In other words,
#for depth 2,4,6,....24 they had 100 random puzzles to do for each depth. But if we generate the puzzles
#the way Dr. Ramanujan told us to do, we have no control of controlling the depth, and therefore we are going to
#get a way variety of numbers. So we are given three choices:
#1. Ignore the 1200 stuff on the paper and create our own experiment protocol and conduct it
#2. Do it the above randomPuzzle way and do the algorithms until we reach 100 for each (ofc we'll code this)
#3. Re-code the randomPuzzle function so that we can choose our depth
#Think it'd be best if we ask Dr. R tomorrow how to go on but I wanted to hear your thoughts too
#Apparently other groups did it by second method

#Alex Comments: I like doing option number two
def experiment(option):
    tested = {}
    data = {}
    evens = [2,4,6,8,10,12,14,16,18,20,22,24]
    for i in evens:
        data[i] = []
    finished = []
    flag = False
    count = 0
    # while(flag == False):
    for i in evens:
        print(i)
        while(len(data[i]) < lim):
            print(str(i) + "'s" +"length: " + str(len(data[i])))
            values = [0,1,2,3,4,5,6,7,8]
            random.shuffle(values)
            testStart = Board(values, 0, 0)
            testGoal = randomPuzzle(testStart, i)
            if testStart in tested:
                if tested[testStart] == testGoal:
                    continue
            tested[testStart] = testGoal
            solved = aStar(testStart, testGoal, option)
            solution = solved[0].pCost
            numNodes = solved[1]
            if solution in data:
                data[solution].append(numNodes)
            #     if len(data[solution]) < 100:
            #         data[solution].append(numNodes)
            #     else:
            #         if solution not in finished:
                        #print(str(solution) + " is full!\n")
                        #finished.append(solution)
            #flag = checkFull(data)
            count += 1
            # if(count > 50000):
            #     break
            print("count: " + str(count))
        finished.append(i)
    return [finished, data]

def computeAverage(data):
    average = {}
    for i in data.keys():
        sum = 0
        index = 0
        for j in data[i]:
            if(index == lim):
                break
            index += 1
            sum += j
        average[i] = sum / lim
    return average

def main():
    # Test Case for Scan
    values = [7,2,4,5,0,6,8,3,1]
    # gValues = [0,1,2,3,4,5,6,7,8]
    testBoard = Board(values, 0, 0)
    print("Start: ")
    print(testBoard)
    # goalBoard = Board(gValues, 0, 0)
    # print("Initial: ")
    # print(testBoard)
    # print("Final: ")
    # final = aStar(testBoard , goalBoard, 2)
    # print(final)
    # print(final.pCost)
    test1 = experiment(1)
    test2 = experiment(2)
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("Experiments: ")
    print("Number of Tests for each depth: ")
    print("_____ H1:")
    for i in test1[0]:
        print str(i) + ": " + str(len(test1[1][i]))
        print("\n")
    print("_____ H2:")
    for i in test2[0]:
        print str(i) + ": " + str(len(test2[1][i]))
        print("\n")
    print("\n")
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("Data Values for each depth: ")
    print("_____ H1:")
    for i in test1[1].keys():
        print str(i) +  ": "
        print str(test1[1][i])
        print("\n")
    print("_____ H2:")
    for i in test2[1].keys():
        print str(i) +  ": "
        print str(test2[1][i])
        print("\n")
    print("\n")
    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("Averages for each depth: ")
    print("_____ H1:")
    final = computeAverage(test1[1])
    for i in final.keys():
        print str(i) +  ": " + str(final[i])
    print("\n")
    print("_____ H2:")
    final = computeAverage(test2[1])
    for i in final.keys():
        print str(i) +  ": " + str(final[i])

if __name__== "__main__":
    main()
