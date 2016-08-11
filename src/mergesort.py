import random

def mergesort(sort1,sort2):
    retList=[]
    i=j=0
    while i < len(sort1) and j < len(sort2):
        if sort1[i] < sort2[j]:
            retList.append(sort1[i])
            i += 1
        else:
            retList.append(sort2[j])
            j += 1
            
    while i < len(sort1):
        retList.append(sort1[i])
        i += 1
    while j < len(sort2):
        retList.append(sort2[j])
        j += 1
            
    return retList

def sort(sortList):
    length=len(sortList)
    if length==1:
        return sortList
    middle=length/2
    sa1=sort(sortList[0:middle])
    sa2=sort(sortList[middle:length])
    return mergesort(sa1, sa2)

mylist=[ x for x in xrange(0,30)]
random.shuffle(mylist)
print mylist
print sort(mylist)