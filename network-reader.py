from collections import deque
import time as timeF
from hash import Hash

FILE_NORMAL = "./packets128normal5.nfp"
FILE_DDOS = "./packets128attack3.nfp"

CYCLE_TIME = 22 #seconds
THRESHOLD = 190 #procent
MAX_ROUNDS = 16


def getTime(lyear: int,lmon: int,lday: int,lhour:int,lmin:int,lsec:int):
    return lsec + 60*lmin + 60*60*lhour + 60*60*24 * lday + lmon * 60 * 60 * 24 * 30 + lyear * 60 * 60 * 24 * 30 * 365

hashGen = Hash()



currentCycle = 0

averages = []
currentSum = []
sums: list[deque] = []
nr_round = 0
net_counter = 0

for i in range(256):
    sums.append(deque())
    currentSum.append(0)
    averages.append(0)


with open(FILE_NORMAL) as file:
    
    
    
    for line in file.read().split("\n"):
        net_counter += 1
        
        words = line.split(" ")
        if(len(words) == 0): continue
        if(len(words[0]) == 0): continue

        for id, word in enumerate(words):
            words[id] = int(word, 16)

        time = getTime(words[-7], words[-6], words[-5], words[-4], words[-3], words[-2])

        if(currentCycle == 0):
            currentCycle = time

        # print(time - currentCycle)

        ip_int = bin(words[0])[2:]
        # print(ip_int)
        dest = hashGen.hash_single(ip_int)
        currentSum[dest] += 1

        if time - currentCycle > CYCLE_TIME:
            nr_round += 1
            print("Cycle change!", nr_round, "-", net_counter)
            currentCycle = 0
            for i in range(256):
                sums[i].append(currentSum[i])
                average = averages[i]/len(sums[i])
                averages[i] += currentSum[i]
                

                if(nr_round > MAX_ROUNDS):
                    if(average > 0 and currentSum[i] * 100 / average > THRESHOLD):
                        print("Attack!", nr_round, i, "-", currentSum[i], average, sums[i])
                        timeF.sleep(2)

                    deletedItem = sums[i].popleft()
                    averages[i] -= deletedItem

                currentSum[i] = 0

                

            
            




