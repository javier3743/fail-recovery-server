import matplotlib.pyplot as plt
import numpy as np
import math


def generateRandomExponential():
    return round(float(np.random.exponential(scale = 5, size = 1)))

def generateRandomNormal():
    return math.ceil(np.random.normal(loc = 6, scale = 2, size = 1))

def generateRandomUniformR():
    return math.ceil(np.random.uniform(low = 1, high = 10, size = 1))

def generateRandomUniform():
    return math.ceil(np.random.uniform(low = 1, high = 8, size = 1))


def recoverServer(recoveryTime, arrivalTime):
    if arrivalTime > recoveryTime:
        arrivalTime = arrivalTime - recoveryTime
        return arrivalTime
    else:
        global queue
        global totalTasks
        print("Added to queue while recovering")
        queue+=1
        totalTasks+=1
        recoveryTime = recoveryTime - arrivalTime
        arrivalTime = generateRandomNormal()
        return recoverServer(recoveryTime, arrivalTime)
        
def initServer():  
    times = []
    recuperationTime = 0
    global totalTasks
    totalTasks = 0
    global queue
    queue = 1

    times.append(generateRandomNormal())
    times.append(generateRandomUniform()) 
    times.append(generateRandomExponential()) 
    x = 30.0
    totalWaitingTime = times[1]
    while x > 0:
        print("Queue:", queue)
        minTime = min(times)
        x = x - minTime

        print(times)
        times[0] = times[0] - minTime
        times[1] = times[1] - minTime
        times[2] = times[2] - minTime

        print(times) 
        if times[0] == 0:
            print("Arrived new task")
            times[0] = generateRandomNormal()
            times[1] = generateRandomUniform()
            times[2] = generateRandomExponential()
            totalWaitingTime += times[1]            
            totalTasks += 1            
            queue+=1
            continue
        
        if times[1] == 0:
            if queue == 0:
                print("Queueu is empty")
                times[0] = 0
                continue
            print("Task is processing")
            times[0] = generateRandomNormal()
            times[1] = generateRandomUniform()
            times[2] = generateRandomExponential()
            
            queue-=1
            continue

        if times[2] == 0:
            print("Server failed")

            recuperationTime = generateRandomUniformR()
            totalWaitingTime += recuperationTime

            newArrivalTime = recoverServer(recuperationTime, times[0])
            print("Server Recovered")

            times[0] = newArrivalTime
            times[1] = generateRandomUniform()
            times[2] = generateRandomExponential()

    averageWaitingTime = totalWaitingTime/totalTasks

    print("Server OFF\n")
    print("Total waiting time: " + str(totalWaitingTime))
    print("Total task arrived: " + str(totalTasks))
    print("Average waiting time: " + str(averageWaitingTime))

    return averageWaitingTime


iterations = 100000
data = []
while iterations > 0:
    iterations-=1
    data.append(initServer())


plt.hist(data, density=True, bins=30)

plt.xlabel('Minutos')
plt.ylabel('Frecuencia %')

plt.title('Frecuencia del promedio de espera')

plt.show()



