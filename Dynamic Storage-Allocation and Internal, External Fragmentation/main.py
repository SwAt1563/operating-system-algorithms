

partitions_sizes = []
processes_sizes = []

P = 0
R = 0


# File Form
# 6 --> number of partitions
# 5 --> first partition size
# 2
# 1
# 7
# 3
# 2 --> last partition size
def read_resources(file_path):
    global partitions_sizes, R
    with open(file_path, 'r') as f:
        lines = f.readlines()
        R = int(lines[0])
        lines = lines[1:]
        for line in lines:
            if line != '\n':
                line = line.replace("\n", "")
                divide_line = list(map(int, line.split(" ")))
                partitions_sizes.append(divide_line[0])

# File Form
# 5 --> number of processes
# 2 --> first process size
# 5
# 1
# 3
# 6 --> last process size
def read_processes(file_path):
    global processes_sizes, P
    with open(file_path, 'r') as f:
        lines = f.readlines()
        P = int(lines[0])
        lines = lines[1:]

        for line in lines:
            if line != '\n':
                line = line.replace("\n", "")
                divide_line = list(map(int, line.split(" ")))
                processes_sizes.append(divide_line[0])



read_resources("Memory")
read_processes("Processes")

# For save the available space in the memories
current_partitions_sizes = partitions_sizes.copy()
# For know if the partition empty or  not
empty = [True] * R
# For save the position of the process in which memory partition
booked = {}
for i in range(P):
    booked[i] = -1
# For know if the process finished or not
finished = [False] * P

def print_info(finished, processes_sizes, partitions_sizes, booked, internal_fragment, external_fragment):
    if False not in finished:
        print("All processes booked")
    else:
        print("Not all processes booked")

    print('Processes: ', processes_sizes)
    print('Memory: ', partitions_sizes)
    print('Memory_booked: ', booked)
    print('Internal Fragmentation: ', internal_fragment)
    print('External Fragmentation: ', external_fragment)


def FF():
    internal_fragment = 0
    external_fragment = 0

    for i in range(P):
        # linear search for empty space then book it
        for j in range(R):
            if processes_sizes[i] <= current_partitions_sizes[j]:
                current_partitions_sizes[j] -= processes_sizes[i]

                empty[j] = False
                finished[i] = True
                booked[i] = j
                break

    for j in range(R):
        if empty[j]:
            external_fragment += current_partitions_sizes[j]

    for j in range(R):
        if not empty[j]:
            internal_fragment += current_partitions_sizes[j]


    print_info(finished, processes_sizes, partitions_sizes, booked, internal_fragment, external_fragment)




def BF():
    internal_fragment = 0
    external_fragment = 0

    # linear search for the least empty space for the process size then book it
    for i in range(P):
        index = -1
        for j in range(R):
            if processes_sizes[i] <= current_partitions_sizes[j] and index == -1:
                index = j
            elif current_partitions_sizes[index] > current_partitions_sizes[j]\
                    and processes_sizes[i] <= current_partitions_sizes[j] and index != -1:
                index = j

        if index != -1:
            empty[index] = False
            current_partitions_sizes[index] -= processes_sizes[i]
            finished[i] = True
            booked[i] = index

    for j in range(R):
        if empty[j]:
            external_fragment += current_partitions_sizes[j]

    for j in range(R):
        if not empty[j]:
            internal_fragment += current_partitions_sizes[j]

    print_info(finished, processes_sizes, partitions_sizes, booked, internal_fragment, external_fragment)

def WF():
    internal_fragment = 0
    external_fragment = 0

    # linear search for the highest empty space for the process size then book it
    for i in range(P):
        index = -1
        for j in range(R):
            if processes_sizes[i] <= current_partitions_sizes[j] and index == -1:
                index = j
            elif current_partitions_sizes[index] < current_partitions_sizes[j] \
                    and processes_sizes[i] <= current_partitions_sizes[j] and index != -1:
                index = j

        if index != -1:
            empty[index] = False
            current_partitions_sizes[index] -= processes_sizes[i]
            finished[i] = True
            booked[i] = index

    for j in range(R):
        if empty[j]:
            external_fragment += current_partitions_sizes[j]

    for j in range(R):
        if not empty[j]:
            internal_fragment += current_partitions_sizes[j]

    print_info(finished, processes_sizes, partitions_sizes, booked, internal_fragment, external_fragment)

BF()