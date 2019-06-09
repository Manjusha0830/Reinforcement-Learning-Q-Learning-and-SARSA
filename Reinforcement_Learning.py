import  random
import numpy as np


R = {0:-1,1:-2,2:-2,3:-3}
AString = {0:'^^^^',1:'>>>>',2:'<<<<',3:'VVVV',4:'####',5:'GGGG'}
maze = [
        [1,1,1,1,1,1,1,1,1,1,50],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,'####','####','####','####',1,1,1],
        [1,1,1,1,'####',1,1,'####',1,1,1],
        [1,1,1,'####','####',1,1,'####',1,1,1],
        [1,1,1,1,1,1,'####','####',1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ]


rowLen = len(maze)
colLen= len(maze[0])
gamma = 0.9

    
class Values(object):
    
    def __init__(self):
        self.val =[0,0,0,0]

    def setVal(self, val,dir):
        self.val[dir]=val
        
    
    def getVal(self,dir):
        return self.val[dir]

class Cell(object):
    
    def __init__(self):
        self.afVal= Values()
        self.Qval = Values()
        self.isBlocked = False
        self.bestAction =0

    def setAfVal(self, val,dir):
        self.afVal.setVal(val,dir)

    def getAfVal(self,dir):
        if self.isBlocked==False:
            return self.afVal.getVal(dir)
        else:
            return "####"
    
    def setAfAll(self, values):
        self.afVal = values

    def getAfAll(self):
        if self.isBlocked==False:
            return self.afVal.val
        else:
            return ["####","####","####","####"]
    def setQval(self,val,dir):
        self.Qval.setVal(val,dir)

    def getQval(self,dir):
        if self.isBlocked==False:
            return self.Qval.getVal(dir)
        else:
            return "####"
    
    def setQvalAll(self, values):
        self.Qval = values

    def getQvalAll(self):
        if self.isBlocked==False:
            return self.Qval.val
        else:
            return ["####","####","####","####"]

    

    def setbestAction(self, action):
        self.bestAction = action

    def getbestAction(self):
        return self.bestAction
    
    def setIsBlocked(self,block):
        self.isBlocked = block
    
    def getIsBlocked(self):
        return self.isBlocked 

def isObstacle(row,col):
    if row<0 or col<0 or row>=rowLen or col>=colLen or maze[row][col]=='####':
        return True
    else:
        return False




def random_free_place():
    
    row= random.randrange(0,rowLen)
    col= random.randrange(0,colLen)

    while isObstacle(row,col) is True or (maze[row][col] == 50):
        row = random.randrange(0,rowLen)
        col = random.randrange(0,colLen)
    return (row,col)


def initMaze(outMaze):
    
    for row in range(0,rowLen):
        outMaze[row] =dict()
        for col in range(0,colLen):
            c = Cell()
            if maze[row][col] is 1:
                afVal = Values()
                Qval = Values()
                c.setAfAll(afVal)
                c.setQvalAll(Qval)
                c.setIsBlocked(False)
                c.setbestAction(0)
            elif maze[row][col] == '####' :
                c.setIsBlocked(True)
                afVal = Values()
                Qval = Values()
                c.setAfAll(afVal)
                c.setQvalAll(Qval)
                c.setbestAction(4)# #####
            else:
                afVal = Values()
                Qval = Values()
                Qval.val =[50,50,50,50]
                c.setAfAll(afVal)
                c.setQvalAll(Qval)
                c.setIsBlocked(False)
                c.setbestAction(5)#GGGG
            outMaze[row][col] = c

def printValues(outMaze,valueType):
    for row in range(0,rowLen):
        firstRow = ""
        secondRow  =""
        thirdRow = ""
        for col in range(0,colLen):
            if valueType=='AfVal':
                val = outMaze[row][col].getAfAll()
            elif valueType=='QVal':
                val = outMaze[row][col].getQvalAll()
                if(outMaze[row][col].isBlocked==False):
                    val = [  round(elem,1) for elem in val ]            
                
            else:
                print('invalid call'+valueType)

            firstRow = firstRow + "\t"+ str(val[0]).center(4) + "\t" 
            secondRow = secondRow + "\t" + str(val[3]).center(4) + "\t" + str(val[1]) +"\t"
            thirdRow = thirdRow + "\t" +  str(val[2]).center(4) + "\t" 
        print(firstRow)
        print(secondRow)
        print(thirdRow)

def printBestAction(outMaze):
    for row in range(0,rowLen):
        rowString =''
        for col in range(0,colLen):
            if(outMaze[row][col].isBlocked== False):
                rowString = rowString + AString[outMaze[row][col].getbestAction()] + '\t'
            else:
                rowString = rowString + '####' + '\t'
        print(rowString)


def calcQlearn():
    outMaze = dict()
    initMaze(outMaze)
    countMoves = dict()
    for trial in range(10000):
        count=0   
        x,y = random_free_place()
        while(maze[x][y]!=50 and count<50):
            count +=1
            nextX =0
            nextY=0
            
            qValues = outMaze[x][y].getQvalAll()
            bestAction = np.argmax(qValues)
            outMaze[x][y].setbestAction(bestAction)
            randAction = random.randint(0,3)
            randNumber = random.uniform(0,1)
            randNumberDrift = random.uniform(0,1)
            if randNumber<0.95:
                action = bestAction
            else:
                action = randAction
            
            if(action =='0'):
                if randNumberDrift<0.8:
                    nextX = x-1
                    nextY= y
                elif randNumberDrift<0.9:
                    nextX = x
                    nextY= y+1
                else:
                    nextX = x
                    nextY= y-1
            elif(action =='1'):
                if randNumberDrift<0.8:
                    nextX = x
                    nextY= y+1
                elif randNumberDrift<0.9:
                    nextX = x-1
                    nextY= y
                else:
                    nextX = x+1
                    nextY= y
            elif(action =='2'):
                if randNumberDrift<0.8:
                    nextX = x
                    nextY= y-1
                elif randNumberDrift<0.9:
                    nextX = x+1
                    nextY= y
                else:
                    nextX = x-1
                    nextY= y
            else:
                if randNumberDrift<0.8:
                    nextX = x+1
                    nextY= y
                elif randNumberDrift<0.9:
                    nextX = x
                    nextY= y+1
                else:
                    nextX = x
                    nextY= y-1
            
            if(isObstacle(nextX,nextY)): #bounce back and check best action again
                continue

            reward = R[action]
            Qvalue = qValues[action]
            afVal = outMaze[x][y].getAfVal(action) + 1
            outMaze[x][y].setAfVal(afVal,action)
            nextQValues = outMaze[nextX][nextY].getQvalAll()
            maxQvalue = max(nextQValues) 
            qlearning = Qvalue + (1/afVal)*(reward + gamma*(maxQvalue) - Qvalue)
            outMaze[x][y].setQval(qlearning,action) 
            x=nextX
            y=nextY
        countMoves[trial] = count
        #if(trial == 999):
            #print("Qlearning trial 1000, Access Frequency")
            #printValues(outMaze,'AfVal')
            #print("Qlearning trial 1000, Qvalue")
            #printValues(outMaze,'QVal')
            #print("Qlearning trial 1000,Optimal Action")
            #printBestAction(outMaze)
            
        if(trial == 9999):
            #print("Qlearning trial 10000, Access Frequency")
            #printValues(outMaze,'AfVal')
            #print("Qlearning trial 10000, Qvalue")
            #printValues(outMaze,'QVal')
            print("Qlearning trial 10000,Optimal Action")
            printBestAction(outMaze)
            

def calcSarsa():
    outMaze = dict()
    initMaze(outMaze)
    countMoves = dict()
    for trial in range(10000):
        count=0   
        x,y = random_free_place()
        while(maze[x][y]!=50 and count<50):
            count +=1
            nextX =0
            nextY=0
            qValues = outMaze[x][y].getQvalAll()
            bestAction = np.argmax(qValues)
            randAction = random.randint(0,3)
            randNumber = random.uniform(0,1)            
            randNumberDrift = random.uniform(0,1)
            if randNumber<0.95:
                action = bestAction
            else:
                action = randAction          
            if(action =='0'):
                if randNumberDrift<0.8:
                    nextX = x-1
                    nextY= y
                elif randNumberDrift<0.9:
                    nextX = x
                    nextY= y+1
                else:
                    nextX = x
                    nextY= y-1
            elif(action =='1'):
                if randNumberDrift<0.8:
                    nextX = x
                    nextY= y+1
                elif randNumberDrift<0.9:
                    nextX = x-1
                    nextY= y
                else:
                    nextX = x+1
                    nextY= y
            elif(action =='2'):
                if randNumberDrift<0.8:
                    nextX = x
                    nextY= y-1
                elif randNumberDrift<0.9:
                    nextX = x+1
                    nextY= y
                else:
                    nextX = x-1
                    nextY= y
            else:
                if randNumberDrift<0.8:
                    nextX = x+1
                    nextY= y
                elif randNumberDrift<0.9:
                    nextX = x
                    nextY= y+1
                else:
                    nextX = x
                    nextY= y-1
            if(isObstacle(nextX,nextY)): #bounce back and check best action again
                continue

            reward = R[action]
            Qvalue = qValues[action]
            afVal = outMaze[x][y].getAfVal(action) +1
            outMaze[x][y].setAfVal(afVal,action)
            nextQValue = outMaze[nextX][nextY].getQval(action)
            SarsaQvalue = Qvalue + (1/afVal)*(reward + gamma*(nextQValue) - Qvalue)
            outMaze[x][y].setQval(SarsaQvalue,action)
            
            x=nextX
            y=nextY
        countMoves[trial] = count
        #if(trial == 999):
            #print("Sarsa trial 1000, Access Frequency")
            #printValues(outMaze,'AfVal')
            #print("Sarsa trial 1000,Qvalue")
            #printValues(outMaze,'QVal')
            #print("Sarsa trial 1000,Optimal Action")
            #printBestAction(outMaze)
            
        '''if(trial == 9999):
            #print("Sarsa trial 10000, Access Frequency")
            #printValues(outMaze,'AfVal')
            #print("Sarsa trial 10000,Qvalue")
            #printValues(outMaze,'QVal')
            print("Sarsa trial 10000,Optimal Action")
            printBestAction(outMaze)'''
            


def main():
    calcSarsa()
    calcQlearn()
    
        
if __name__ == "__main__":
    main()