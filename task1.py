import random
import time

def createlist():
    nums=[]
    for i in range(10000):
        nums.append(random.randint(0, 999))
    return nums
def createhist(list):
    hist=[0]*10
    for i in list:
        if i in range(0, 99):
            hist[0]+=1
        elif i in range(100, 199):
            hist[1]+=1
        elif i in range(200, 299):
            hist[2]+=1
        elif i in range(300, 399):
            hist[3]+=1
        elif i in range(400, 499):
            hist[4]+=1
        elif i in range(500, 599):
            hist[5]+=1
        elif i in range(600, 699):
            hist[6]+=1
        elif i in range(700, 799):
            hist[7]+=1
        elif i in range(800, 899):
            hist[8]+=1
        else:
            hist[9]+=1
    return hist
def timecalc(l):
    start = time.time()
    createhist(l)
    end = time.time()
    return end - start

timelist = []
amount=0
summa=0
for i in range(0, 100):
    x = createlist()
    timelist.append(timecalc(x))
    summa+=timelist[i]
    amount+=1
    mid=summa/amount
print(summa)
print(max(timelist))
print(min(timelist))
print(mid)