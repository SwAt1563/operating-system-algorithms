# File format
# 53 200  --> head, max_length
# 98 183 37 122 14 124 65 67  --> requests
def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        head, max_length = list(map(int, lines[0].replace("\n", "").split(" ")))
        requests = list(map(int, lines[1].replace("\n", "").split(" ")))

        return head, max_length, requests


head, max_length, requests = read_file('requests.txt')


# For return three position which nearest to the value
def BS(arr, left, right, value):
    mid = 0
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] < value:
            left = mid + 1
        elif arr[mid] > value:
            right = mid - 1
        else:
            return [mid] * 3  # when the current position same as the current request
    positions = [mid, mid - 1]
    if mid + 1 != len(arr):
        positions.append(mid + 1)
    else:
        positions.append(0)
    return positions

# The nearest request First reserved
def SSTF():
    global head, max_length, requests
    path = []
    path_length = 0
    num_of_requests = len(requests)
    requests.sort()

    current_pos = head
    for i in range(num_of_requests):
        positions = BS(requests, 0, len(requests) - 1, current_pos)
        less_one = positions[0]

        for j in range(1, 3):
            if abs(requests[positions[j]] - current_pos) < abs(requests[less_one] - current_pos):
                less_one = positions[j]
        path_length += abs(requests[less_one] - current_pos)
        current_pos = requests[less_one]
        path.append(current_pos)
        requests.remove(current_pos)

    avg = path_length / num_of_requests
    print('Path: {}\nPath_length: {}\nAvg_time: {}'.format(path, path_length, avg))

SSTF()
