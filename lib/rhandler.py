# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 21:28:55 2021
Raffle Handler
@author: https://github.com/GearFox98
"""

import random as rd

def scramble(objects):
    length = len(objects)
    picked = list()
    full = 0
    while True:
        x = rd.randint(0, length - 1)
        if full == 0:
            picked.append(objects[x])
            full += 1
        elif full < length:
            if not picked.__contains__(objects[x]):
                picked.append(objects[x])
                full += 1
        elif full == length:
            break
    return picked

def doAssignments(cont):    
    if len(cont) >= 3:
        ASSIGNMENTS = list()
        scrambleContestants = scramble(cont)
        length = len(scrambleContestants)
        if length > 5:
            if length % 2 == 0:
                for x in range(int(length / 2)):
                    ASSIGNMENTS.append((scrambleContestants[x], scrambleContestants[x + int(length / 2)]))
                ls0 = scrambleContestants[0:int(length/2)]
                ls1 = scrambleContestants[int(length/2):length]
                ls1.reverse()
                for x in range(int(length / 2)):
                    ASSIGNMENTS.append((ls1[x], ls0[x]))
            else:
                ln2 = (length - 3) / 2
                ls2 = list()
                ls2.append(scrambleContestants[-1])
                ls2.append(scrambleContestants[-2])
                ls2.append(scrambleContestants[-3])
                for x in range(int(ln2)):
                    ASSIGNMENTS.append((scrambleContestants[x], scrambleContestants[x + int(ln2)]))
                ls0 = scrambleContestants[0:int(ln2)]
                ls1 = scrambleContestants[int(ln2):length - 3]
                ls1.reverse()
                for x in range(int(ln2)):
                    ASSIGNMENTS.append((ls1[x], ls0[x]))
                
                x = rd.randint(0, 1)
                if x == 0:
                    ASSIGNMENTS.append((ls2[0], ls2[1]))
                    ASSIGNMENTS.append(([1], ls2[2]))
                    ASSIGNMENTS.append((ls2[2], ls2[0]))
                else:
                    ASSIGNMENTS.append((ls2[0], ls2[2]))
                    ASSIGNMENTS.append((ls2[1], ls2[0]))
                    ASSIGNMENTS.append((ls2[2], ls2[1]))
            
        else:
            for x in range(length):
                if not x == length - 1:
                    ASSIGNMENTS.append((scrambleContestants[x], scrambleContestants[x + 1]))
                else:
                    ASSIGNMENTS.append((scrambleContestants[x], scrambleContestants[0]))
        
        return ASSIGNMENTS
    else:
        return "nil"

'''
Raffle Maker

It gets a list of participants [cont] and a maximum places to give prizes [max] by default 3
Once the max value is reached it returns a result (list)
'''
def raffle(cont, max = 3):
    if len(cont) == 0:
        return 'nil'
    else:
        raffleList = scramble(cont)
        finale = list()
        temp = list()
        count = 0
        while count < max:
            y = rd.randint(0, max - 1)
            if not temp.__contains__(y):
                finale.append(raffleList[y])
                temp.append(y)
                count += 1
        return finale