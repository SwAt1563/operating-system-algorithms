from Scheduling import Scheduling
reference_strings = []
MEMORY_SIZE = 3  # MEMORY SIZE 3 FRAMES
memory = []
P = 0



# File Form
# 4 --> number of processes
# 7AC  --> reference string - two lowest digits = process id
# 0BC
# 1AA
# 200
def read_reference_strings(file_path):
    global reference_strings, P
    with open(file_path, 'r') as f:
        lines = f.readlines()
        P = int(lines[0])
        lines = lines[1:]

        for line in lines:
            if line != '\n':
                line = line.replace("\n", "")
                line = line[:-2]
                reference_strings.append(line)



read_reference_strings("Processes")

print(P, reference_strings)


def FIFO():
    time = 0
    page_faults = 0
    for i in range(P):
        # If the memory has empty frame
        if len(memory) != MEMORY_SIZE:
            if reference_strings[i] not in memory:

                # For add the reference string in the memory
                memory.append(reference_strings[i])
                page_faults += 1
        else:
            # If the page not in the memory
            if reference_strings[i] not in memory:

                memory.pop(0)
                memory.append(reference_strings[i])
                page_faults += 1

        Scheduling.scheduling(time, reference_strings[i], memory.copy())
        time += 1
    return page_faults

print('Page Faults: ', FIFO())
Scheduling.print_scheduling()