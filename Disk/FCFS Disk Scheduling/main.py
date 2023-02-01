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

# First request First reserved
def FCFS():
    global head, max_length, requests
    path = []
    path_length = 0
    num_of_requests = len(requests)
    for i in range(num_of_requests):
        path.append(requests[i])
        if i == 0:
            path_length = abs(requests[0] - head)
        else:
            path_length += abs(requests[i] - requests[i - 1])

    avg = path_length / num_of_requests
    print('Path: {}\nPath_length: {}\nAvg_time: {}'.format(path, path_length, avg))

FCFS()
