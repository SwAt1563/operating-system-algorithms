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

def LRU():
    time = 0
    page_faults = 0
    for i in range(P):
        if len(memory) != MEMORY_SIZE:
            exist = False
            # If the memory has empty frame
            for frame in memory:
                # If the reference string exist already in the memory
                # then no page fault
                if frame[0] == reference_strings[i]:

                    # Least Recently Used Update it time if it exist before in the memory
                    frame[1] = time

                    exist = True
                    break
            if not exist:
                # For add the reference string with the time when it enter the memory
                memory.append([reference_strings[i], time])
                page_faults += 1
        else:
            exist = False
            for frame in memory:
                # If the reference string exist already in the memory
                # then no page fault
                if frame[0] == reference_strings[i]:

                    # Least Recently Used frame update it time if it exist before in the memory
                    frame[1] = time

                    exist = True
                    break
            if not exist:
                index = 0
                # For get the oldest booked frame in the memory
                for j in range(1, MEMORY_SIZE):
                    if memory[index][1] > memory[j][1]:
                        index = j
                memory[index] = [reference_strings[i], time]
                page_faults += 1


        Scheduling.scheduling(time, reference_strings[i], memory.copy())
        time += 1
    return page_faults



print('Page Faults: ', LRU())
Scheduling.print_scheduling()