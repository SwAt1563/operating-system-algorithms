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

def LFU():
    time = 0
    page_faults = 0
    for i in range(P):
        # If the memory has empty frame
        if len(memory) != MEMORY_SIZE:
            # For check if the page exist or not in the memory
            if reference_strings[i] not in memory:
                # For add the reference string
                memory.append(reference_strings[i])
                page_faults += 1
        else:
            # For check if the page exist or not in the memory
            if reference_strings[i] not in memory:

                # for count the times that the pages in the memory used before
                count_frequencies = [0] * MEMORY_SIZE
                for j in range(i):
                    for k in range(MEMORY_SIZE):
                        if reference_strings[j] == memory[k]:
                            count_frequencies[k] += 1

                # for select the page which has least count
                index = 0
                for k in range(1, MEMORY_SIZE):
                    if count_frequencies[k] < count_frequencies[index]:
                        index = k

                memory.pop(index)
                memory.append(reference_strings[i])
                page_faults += 1

        Scheduling.scheduling(time, reference_strings[i], memory.copy())
        time += 1
    return page_faults



print('Page Faults: ', LFU())
Scheduling.print_scheduling()