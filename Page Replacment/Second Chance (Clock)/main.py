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

def Clock():
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

                    # if the page exist before the give it chance
                    frame[1] = 1

                    exist = True
                    break
            if not exist:
                # For add the reference string with the time when it enter the memory
                memory.append([reference_strings[i], 0])
                page_faults += 1
        else:
            exist = False
            for frame in memory:
                # If the reference string exist already in the memory
                # then no page fault
                if frame[0] == reference_strings[i]:

                    # if the page exist before the give it chance
                    frame[1] = 1

                    exist = True
                    break
            if not exist:

                while True:
                    check = False
                    # For get the oldest booked frame in the memory
                    for j in range(MEMORY_SIZE):
                        # if the page has chance then remove it
                        if memory[j][1] == 1:
                            memory[j][1] = 0
                        # if the page hasn't chance then replace it
                        else:
                            memory.pop(j)
                            memory.append([reference_strings[i], 0])
                            check = True
                            break
                    if check:
                        break
                page_faults += 1


        Scheduling.scheduling(time, reference_strings[i], memory.copy())
        time += 1
    return page_faults



print('Page Faults: ', Clock())
Scheduling.print_scheduling()