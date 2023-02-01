# File format
# 53 200 0 --> head, max_length, TOWARD ZERO(IF 1 THEN TOWARD MAX)
# 98 183 37 122 14 124 65 67  --> requests
def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        head, max_length, DIRECTION = list(map(int, lines[0].replace("\n", "").split(" ")))
        requests = list(map(int, lines[1].replace("\n", "").split(" ")))

        return head, max_length, DIRECTION, requests


head, max_length, DIRECTION, requests = read_file('requests.txt')

# For return the index of the current value if it exist in the array
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:

        mid = (high + low) // 2

        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

    # If we reach here, then the element was not present
    return -1


# if DIRECTION = 0, then the algorithm will scan on the left side firstly until reach the end if it doesn't finish
# the requests then go to the right side then finish
# if DIRECTION = 1, the opposite of 0 by change the directions
def SCAN():
    global head, max_length, DIRECTION, requests
    path = []
    path_length = 0
    num_of_requests = len(requests)
    requests.sort()
    current_pos = head
    if DIRECTION == 0:

        for p in reversed(range(current_pos)):
            if len(requests) == 0:
                break
            index = binary_search(requests, p)
            path_length += 1
            if index == -1:
                continue
            path.append(requests[index])
            requests.remove(requests[index])

        for p in range(1, max_length):
            if len(requests) == 0:
                break
            index = binary_search(requests, p)
            path_length += 1
            if index == -1:
                continue
            path.append(requests[index])
            requests.remove(requests[index])

    elif DIRECTION == 1:
        for p in range(current_pos + 1, max_length):
            if len(requests) == 0:
                break
            index = binary_search(requests, p)
            path_length += 1
            if index == -1:
                continue
            path.append(requests[index])
            requests.remove(requests[index])

        for p in reversed(range(max_length - 1)):
            if len(requests) == 0:
                break
            index = binary_search(requests, p)
            path_length += 1
            if index == -1:
                continue
            path.append(requests[index])
            requests.remove(requests[index])

    avg = path_length / num_of_requests
    print('Path: {}\nPath_length: {}\nAvg_time: {}'.format(path, path_length, avg))


SCAN()
