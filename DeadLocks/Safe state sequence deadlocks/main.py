from Scheduling import Scheduling

resources = []
processes_max = []
processes_allocations = []
processes_needs = []
safe_sequence = []
finished = []
P = 0
R = 0


# File Form
# 3 --> number of resources
# 0 7 --> resources id, resource size
# 1 2
# 2 6
def read_resources(file_path):
    global resources, R
    with open(file_path, 'r') as f:
        lines = f.readlines()
        R = int(lines[0])
        lines = lines[1:]
        for line in lines:
            if line != '\n':
                line = line.replace("\n", "")
                divide_line = list(map(int, line.split(" ")))
                resources.append(divide_line[1])

# File Form
# 2 --> number of processes
# 0 0 1 0 --> process id, number of all requests from each resources
# 0 0 1 0 --> process id, number of all current allocation from each resources
# 1 4 0 2 --> process id, number of all requests from each resources
# 1 2 0 0 --> process id, number of all current allocation from each resources
def read_processes(file_path):
    global processes_max, processes_allocations, P
    with open(file_path, 'r') as f:
        lines = f.readlines()
        P = int(lines[0])
        lines = lines[1:]

        count = 0
        for line in lines:
            if line != '\n':
                line = line.replace("\n", "")
                divide_line = list(map(int, line.split(" ")))
                if count % 2 == 0:
                    processes_max.append(divide_line[1:])
                else:
                    processes_allocations.append(divide_line[1:])
                count += 1


read_resources("Resources")
read_processes("Processes")

resources_current_state = resources.copy()

# For find the remaining requests for each process
# and find the available size in the resource
for i in range(P):
    need = []
    for j in range(R):
        need.append(processes_max[i][j] - processes_allocations[i][j])
        resources_current_state[j] -= processes_allocations[i][j]
    processes_needs.append(need)

finished = [False] * P

print(P, R)
print(resources)
print(processes_allocations)
print(processes_max)
print(processes_needs)
print(resources_current_state)
print(finished)

deadlock = False
resources_previous_state = resources_current_state.copy()
count = 0
# Continue until finish all request or deadlock occurred
while True:
    count += 1
    for i in range(P):
        if finished[i]:
            continue

        need = processes_needs[i]
        finish = True

        # For check if the amount of request from all resources less than the available in it
        for j in range(R):
            if resources_current_state[j] >= need[j]:
                continue
            else:
                finish = False
                break

        if finish:
            for j in range(R):
                resources_current_state[j] += processes_allocations[i][j]
            finished[i] = finish
            safe_sequence.append(i)
            # For Scheduling
            Scheduling.scheduling(count, i, resources_current_state.copy(), need.copy(), True)
        else:
            # For Scheduling
            Scheduling.scheduling(count, i, resources_current_state.copy(), need.copy(), False)

    # If all processes finished
    if False not in finished:
        break

    # If there no any change on the resources amount
    if resources_previous_state == resources_current_state:
        deadlock = True
        break
    else:
        resources_previous_state = resources_current_state.copy()

if deadlock:
    print("DeadLock")
    Scheduling.print_scheduling()
else:
    print(finished)
    print(resources_current_state)
    print(safe_sequence)
    Scheduling.print_scheduling()
