# Bubble sort

def bubble_sort(array) -> list | tuple | set:
    local_array = array

    if len(local_array) >= 1:
        pos_arr: int = 0
        swaps: int = 0

        while True:
            if pos_arr > len(local_array) - 2:
                pos_arr = 0
                if swaps == 0:
                    return local_array
                swaps = 0
            
            if local_array[pos_arr] > local_array[pos_arr + 1]:
                current_data = local_array[pos_arr]
                local_array[pos_arr] = local_array[pos_arr + 1]
                local_array[pos_arr + 1] = current_data
                swaps += 1

            pos_arr += 1
    else:
        return local_array
