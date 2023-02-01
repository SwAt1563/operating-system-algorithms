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

def Optimal_Page():
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

                farthest_page = [-1] * MEMORY_SIZE
                # For get the last use of page in the memory from the reference strings
                for j in range(i + 1, P):
                   for k in range(MEMORY_SIZE):
                       if reference_strings[j] == memory[k] and farthest_page[k] == -1:
                           farthest_page[k] = j


                index = -1
                for k in range(MEMORY_SIZE):
                    # If we will not use the reference string again then pop it
                    if farthest_page[k] == -1:
                        index = k
                        break
                    else:
                        if index == -1:
                            index = k
                        else:
                            # If the another reference string farther than the current reference string then replace it
                            if farthest_page[index] < farthest_page[k]:
                                index = k


                memory[index] = reference_strings[i]
                page_faults += 1


        Scheduling.scheduling(time, reference_strings[i], memory.copy())
        time += 1
    return page_faults


print('Page Faults: ', Optimal_Page())
Scheduling.print_scheduling()