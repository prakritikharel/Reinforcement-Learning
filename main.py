#Prakriti Kharel-- A3

#Goal:  using simple Learning Automata, learn the best floor for the car to be waiting using the Tsetlin, Krinsky, Krylov and LRI Schemes,
#in each case, use a suitable value for the "memory" and learning parameter
import random
import math
import queue
import heapq
from collections import deque
import numpy
from random import choices
import time
#reward when Beta = 0
#penalty when Beta =1

#minimize penalty, maximize reward
#final stored in an array of 6 * 6 (because it will be easier to calculate using the mod function )

#state
outerloop = 7;
state  = [0] * outerloop
oneA= []
twoA = []
threeA = []
fourA = []
fiveA = []
sixA = []

weights = [(1/6), (1/6),(1/6), (1/6), (1/6), (1/6) ]
population = [1, 2, 3, 4, 5, 6]


def printfunc ():
    print ("----------------------------------------------------")

    for i in range (6):
        for j in range (outerloop):
            print(state[i][j], end =' ')
        print()

#till i is 0, move left, if i is 0, stay where you are
#by this logic, the closer to j = 0, the
def moveLeft(i, j):
    if(j == 0):
        return
    else:
        state[i][j-1]= state[i][j]
        state[i][j] = 0

def moveRight(i, j):
    if(j == (outerloop-1)):
        return
    else:
        state[i][j+1]= state[i][j]
        state[i][j] = 0

#reward & penalty treated the same
def Tsetlin(beta, i, j):
    if (beta == 0):
        moveLeft(i,j)
        h1 = random.randint(1,6) #write now its guessing randomly but we want to guess using the f and g matrix
        return h1

    else:
        moveRight(i,j)

        h1 = random.randint(1, 6)
        return h1

#reward treated much more seriously than the penalty
def Krinsky(beta, i, j):
    if(beta == 0): #reward move it to the first
        if(j != 0 ):
            state[i][0] = state[i][j]
            state[i][j] = 0
    else: #penalty
        moveRight(i,j)

def Krylov(beta, i, j):
    #reward, same as Tsetlin
    if (beta == 0):
        Tsetlin(beta, i, j)
    #penalty half half
    else:
        h1 = random.randint(0, 11)
        if(h1 >= 5):
            Tsetlin(0, i, j)
        else:
            Tsetlin(1, i, j)

#action probablity updataed scheme
def LRI(beta, i, j):
    if(beta == 1): #penalty no change
        return
    else: #reward, move it up
        # + 0.1 for the chosen
        #- 0.02 for the rest to balance probability
        track = 0
        for k in range (6):
            temp = weights[i-1]
            # 1 - sum of all probabiliites after decrease
            if (k  != (i-1)):
                weights[k] -= temp
        #keeping track of the weight
        for k in range (6):
            if (k != (i - 1)):
                track += weights[k]

        weights[i-1] == track


def Environment(i, current):
    #need to change this
    h1 = random.randint(1,6)
    temp = (0.8* (i)) + 0.4 * (i/2) + h1
    if ((current- i) < temp): #maybe now the best way but for now it works
        return 0
    #penalty
    else:
        return 1

#gives the y value for where the x is
def yVal(x):
    for i in range(6):
        for j in range(outerloop):
            if (state[i][j] == x):
                return j

#next best guess
def bestGuess():
    least = (outerloop -1)
    final  = 0
    for i in range(6):
        temp = yVal(i+1)
        if (temp < least):
            least = temp
            final = i
    return (final +1)

def tracking(x):
    if (x >= 0 and x < 60 ):
        return 1
    elif (x > 60 and x < 120):
        return 2
    elif (x > 120 and x < 180):
        return 3
    elif (x > 180 and x < 240):
        return 4
    elif (x > 240 and x < 360):
        return 5
    else:
        return 6

def Tguess(x, beta):
    if (x != 0 and beta == 0):
        x = x -1
        return x
    else:
        x = x + 1
        return x

def Kguess(x, beta, y):
    if (x != 0 and beta == 0):
        if (y != 0):
            x = tracking(x)
            x = (x - 1) + 60
            return x
        else:
            x = x - 1
            return x
    else:
        x = x + 1
        return x

def Pguess(x, beta, y):
    temp= random.randint(1,2)
    if (x != 0 and beta == 0):
        x = x - 1
        return x
    elif (temp > 1):
        x = x + 1
        return x
    else:
        x = x - 1
        return x




#10,000 times, evaluate the last 1000 times
def Simulation(h1):
    #keeping track
    one = 0
    two  = 0
    three = 0
    four = 0
    five = 0
    six = 0
    #5000 iterations
    i = 0
    beta = 0
    temp = random.randint(1, 360)
    guess = tracking(temp)

    while (i < 15000):

        beta = Environment(guess, h1)
        #when i get guess, i want to figure out the y value for that guess
        y = yVal(guess)
        if (guess != 0):
            guess = guess -1

        #Tsetlin
      #  Tsetlin(beta,guess, y) #need to figure out the y value
       # temp = Tguess(temp, beta)
        #guess = tracking(temp)


        #Krinsky
        #Krinsky(beta, guess, y)
        #temp = Kguess(temp, beta, y)
        #guess = tracking(temp)

        #Krylov
        #Krylov(beta, guess, y)
        #temp = Pguess(temp, beta, y)
        #guess = tracking(temp)


        #LRI
        LRI(beta, guess, y)
        t = choices(population, weights)
        guess = t[0]

        if (i > 14000 ):
            if (guess == 1):
                one += 1
            elif(guess == 2):
                two += 1
            elif(guess == 3):
                three += 1
            elif(guess == 4):
                four += 1
            elif (guess == 5):
                five += 1
            else:
                six += 1
      #  guess = bestGuess()
        i = i + 1;


    oneA.append((one/1000))
    twoA.append((two/1000))
    threeA.append((three / 1000))
    fourA.append((four/1000))
    fiveA.append((five / 1000))
    sixA.append((six / 1000))



     #i need to know how many times each was chosen to calculate the average

def Ensemble():
    for i in range(100):
        h1 = random.randint(1, 6)  # where the person currently is
        Simulation(h1)

def averageAcc(temp = [], *args):
    total = 0
    for i in range (len(temp)):
        total += temp[i]
    return (total/(len(temp)))



def main():
    global current
    #initializing
    for i in range(6):
        state[i] = [0] * outerloop

    temp = int(outerloop/2)
    state[0][temp] = 1
    state[1][temp]= 2
    state[2][temp] = 3
    state[3][temp] = 4
    state[4][temp] = 5
    state[5][temp] = 6
    h1 = random.randint(1, 6)
    #Simulation(h1)
    Ensemble()
    #Ensemble()
    print("The average for one is ", averageAcc(oneA))
    print("The average for two is ", averageAcc(twoA))
    print("The average for three is ", averageAcc(threeA))
    print("The average for four is ",averageAcc(fourA))
    print("The average for five is ",averageAcc(fiveA))
    print("The average for six is ", averageAcc(sixA))


    printfunc()
    start_time = time.clock()
    print("--- %s seconds ---" % (time.clock() - start_time))



main()

