import random
def sort(mylist,start,end):
    if start >= end:
        return -1
    if len(mylist) <= 1:
        return -1
    flag=start
    key=mylist[flag]
    start += 1
    while start < end:
        while start < end and mylist[end] > key:
            end -= 1
        while start < end and mylist[start] <= key:
            start += 1
        tmp=mylist[start]
        mylist[start]=mylist[end]
        mylist[end]=tmp
        if start < end:
            end -= 1
            start += 1
    tmp=mylist[flag]
    mylist[flag]=mylist[start]
    mylist[start]=tmp
    print start,end
    print mylist
    return start

def quicksort(mylist,start,end):
    if len(mylist)<=1:
        return
    if start >= end:
        return
    middle=sort(mylist,start,end)
    if middle < 0:
        return
    quicksort(mylist, start, middle-1)
    quicksort(mylist, middle+1, end)

mylist=[ x for x in xrange(0,20)]
random.shuffle(mylist)
print mylist
quicksort(mylist, 0, len(mylist)-1)
# start=sort(mylist, 0, len(mylist)-1)
# print start
# print mylist
    