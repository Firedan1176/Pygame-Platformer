#Contains utilities for sorting and inserting into a list of INTEGERS


#Searches for val in iterator or returns next highest value's index
def binarySearch(iterator, val, start, end):
    if start == end:
        if iterator[start] > val:
            return start
        else:
            return start + 1

    if start> end:
        return start

    mid = (start + end) // 2
    if iterator[mid] < val:
        return binarySearch(iterator, val, mid + 1, end)
    elif iterator[mid] > val:
        return binarySearch(iterator, val, start, mid - 1)
    else:
        return mid
    
#Sorty boi
def insertionSort(iterator):
    for i in range(1, len(iterator)):
        val = iterator[i]
        j = binarySearch(iterator, val, 0, i - 1)
        #Concatenate a new list that puts the selected value in the right order
        iterator = iterator[:j] + [val] + iterator[j:i] + iterator[i + 1:]
    return iterator


#Inserts val into a sorted list
def insert(iterator, val):
    #Get the index of the next highest val in iterator
    i = binarySearch(iterator, val, 0, len(iterator) - 1)
    #Concatenate a new list that puts the value in a sorted list
    iterator = iterator[:i] + [val] + iterator[i:]
    return iterator

#Removes val from a sorted list
def remove(iterator, val):
    i = binarySearch(iterator, val, 0, len(iterator) - 1)
    if iterator[i - 1] != val:
        return iterator #The value isn't even in the list so just quit

    iterator = iterator[:i - 1] + iterator[i:]
    return iterator

#Generates a friendly name that increments until no new occurrence is in lst
def friendlyName(name, lst):
    count = 0
    temp_name = name
    while temp_name in lst:
        count += 1
        temp_name = name + " " + str(count)
    return temp_name
