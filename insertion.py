# Insertion sort

def insertion_sort(array) -> list | tuple | set:
    for i in range(1, len(array)):
        if array[i] < array[i - 1]:
            j = i
            while array[j] < array[j - 1] and j > 0:
                current_item = array[j]
                next_item = array[j - 1]
                
                array[j] = next_item
                array[j - 1] = current_item

                del next_item, current_item; 
                j -= 1
    return array

        
