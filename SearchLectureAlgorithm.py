import sys 
import turtle
import copy
import time



class Node():
    def __init__ (self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def changeState(self, action, state):
        if (action == 0):
           #state.playerPosition[1] -=1 

           newPlayerPosition = [state.playerPosition[0], state.playerPosition[1] -1 ]

        elif (action == 1):
           #state.playerPosition[0] -=1
           newPlayerPosition = [state.playerPosition[0] -1, state.playerPosition[1]]

        elif (action == 2):
           #state.playerPosition[1] +=1 
            newPlayerPosition = [state.playerPosition[0], state.playerPosition[1] +1 ]


        elif (action == 3):
           #state.playerPosition[0] +=1 
           newPlayerPosition = [state.playerPosition[0] +1, state.playerPosition[1]]

        returnState = State(state.mazeArrangement, newPlayerPosition, state.endPosition)
        return returnState

    

class State():
    def __init__ (self, mazeArrangement, playerPosition, endPosition):
        self.mazeArrangement = mazeArrangement
        self.playerPosition = playerPosition
        self.endPosition = endPosition



class StackFrontier():
    def __init__(self):
        frontier = []
        self.frontier = frontier

    def add (self, node):
        self.frontier.append(node)

    def containsState (self, state):
        for node in self.frontier:
            if node.state == state:
                return True
               
            else:
                continue

    def isEmpty(self):
        if (len(self.frontier) == 0):
            return True
        else:
            return False
    
    def removeNode(self):
        if (self.isEmpty()):
            raise Exception("empty frontier")
            
        else:
            node = self.frontier[-1]
            self.frontier.pop()
            return node

class QueueFrontier(StackFrontier):
    def removeNode (self):
         if (self.isEmpty()):
             raise Exception("empty frontier")
         else:
              node = self.frontier[0]
              self.frontier.pop(0)
              return node

class Maze():
    def __init__(self, mf):
        self.mazeFile = open(mf, "rt")
        
        

    def storeMazeFile(self):
        self.mazeArray = []
        self.pPosition = []
        self.ePosition = []
        rowArray = []
        
        

        rowNum = 0
        colNum = 0
       
        for line in self.mazeFile:
            print(line)
            rowArray = []
            colNum = 0
            for char in line:
                if char == '*':
                    rowArray.append(1)
                if char == " ":
                    rowArray.append(0)
                if char == "A":
                    self.pPosition = [rowNum, colNum]

                    rowArray.append(2)
                if char == "B":
                    rowArray.append(3)
                    self.ePosition = [rowNum,colNum]
                    
                colNum +=1
            self.mazeArray.append(rowArray)
            rowNum+=1
           
        self.thisState = State(self.mazeArray, self.pPosition, self.ePosition)
        return self.thisState
        
       
        

    def isGoalState(self, state):
        if state.playerPosition == state.endPosition:
            return True
        else:
            return False

    
    def containsNode(self, node, eS):
        for eachNode in eS:
            if eachNode.state.playerPosition == node.state.playerPosition:
                return True

        else:
            return False

    


    def solve(self):
        frontier = QueueFrontier()
        self.storeMazeFile()
        self.initState = State(self.mazeArray, self.pPosition, self.ePosition)
        #print("initial state end position = " + str(self.initState.endPosition))
        initNode = Node(state = self.initState, parent = None, action = None)
        frontier.add(initNode)
        #print("node added")
        #print(frontier.frontier[0].state.playerPosition)
        #print(frontier.isEmpty())
        exploredSet = []
        finalAction = []
        loopNum = 0
        isGoalReached = False 
        while not isGoalReached:
            #print("running")
            loopNum+=1
            if frontier.isEmpty():
                raise Exception("noSolution")
                
            #print(frontier.isEmpty())

            currentNode = frontier.removeNode()
            #print("removed Node")
            #print("exploring node: " + str(currentNode.state.playerPosition))
            
            if  self.isGoalState(currentNode.state):
                #print("goalreached")
                isGoalReached = True
                iteratingNode = currentNode
                while iteratingNode.parent != None:
                    #print("iteratingNode")
                    finalAction.append(iteratingNode.action)
                    iteratingNode = iteratingNode.parent
                   
                #set final action back to letter form
                finalAction.reverse()
                for x in range(len(finalAction)):
                    if finalAction[x] == 0: finalAction[x] = "l"
                    if finalAction[x] == 1: finalAction[x] = "u"
                    if finalAction[x] == 2: finalAction[x] = "r"
                    if finalAction[x] == 3: finalAction[x] == "d"

                #print("number of states explored: " + str(loopNum))
                return finalAction


            exploredSet.append(currentNode)

            #expand node
            for i in range(4):
                
                checkState = currentNode.changeState(i, currentNode.state)
                if currentNode.state.mazeArrangement[checkState.playerPosition[0]][checkState.playerPosition[1]] == 0: 
                    newNode = Node(checkState, currentNode, action = i)
                    if not frontier.containsState(checkState) and  not self.containsNode(newNode, exploredSet):
                        frontier.add (newNode)
                        #print("addded node")
                        #print(newNode.state.playerPosition)
                if currentNode.state.mazeArrangement[checkState.playerPosition[0]][checkState.playerPosition[1]] == 3:
                    
                    newNode = Node(checkState, currentNode, action = i)
                    frontier.add (newNode)
                    #print("added node")
                    #print(newNode.state.playerPosition)
            

            

print("\nMaize: \n\n")            
maze1 = Maze("Maze2.txt")

fa = maze1.solve()

time.sleep(2) #for dramatic effect

print("\n\nfinal solution: ")
print(fa)
print("\n\n")
