from Process import Process
from CPU import CPU
from Scheduling import Scheduling
def sort_by_arrival_time(process):
    return process.arrival_time

def read_processes(file_path):
    processes = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            if line != '\n':
                line = line.replace("\n", "")
                divide_line = list(map(int, line.split(" ")))
                process = Process(divide_line[0], divide_line[1], divide_line[2])
                processes.append(process)
    processes.sort(key=sort_by_arrival_time)
    return processes


all_processes = read_processes("Processes.txt")
cpu = CPU()
current_time = 0
QUANTUM = 3

for p in all_processes:
    print(p.to_string())


def RR():
    global current_time

    turn = 0
    # Stop when all processes states = Terminate
    while not Process.check_terminate_all_processes(all_processes):

        # Insert the arrival processes in the ready queue
        arrival_processes = Process.get_arrival_processes(current_time, all_processes)
        for p in arrival_processes:
            cpu.ready_queue.append(p)
            p.enter_ready_queue_first_time()



        # If the CPU not has any process in it and the ready queue not empty then put the first process in the CPU
        if cpu.process is None and len(cpu.ready_queue) != 0:
            turn = 0
            cpu.process = cpu.ready_queue.pop(0)
            # FOR FIND THE RESPONSE TIME IF IT ENTER THE CPU FIRST TIME
            if cpu.process.start_time == 0 and cpu.process.arrival_time != 0:
                cpu.process.enter_CPU_first_time(current_time)
            else:
                cpu.process.enter_CPU(current_time)

        if len(cpu.ready_queue) != 0 and cpu.process is not None and turn == QUANTUM:
            turn = 0
            cpu.ready_queue.append(cpu.process)
            cpu.process.enter_ready_queue(current_time)

            cpu.process = cpu.ready_queue.pop(0)
            # FOR FIND THE RESPONSE TIME IF IT ENTER THE CPU FIRST TIME
            if cpu.process.start_time == 0:
                cpu.process.enter_CPU_first_time(current_time)
            else:
                cpu.process.enter_CPU(current_time)


        # For Scheduling
        Scheduling.scheduling(current_time, cpu.process, cpu.ready_queue.copy())

        # For decrease the burst time of the process and check if it finish then pop it from the CPU
        if cpu.process is not None:
            cpu.process.achieved_work += 1
            turn += 1
            if cpu.process.check_finish_process():
                cpu.process.terminate(current_time + 1)
                cpu.process = None

        # For increase the time
        current_time += 1


RR()
for p in all_processes:
    print(p.to_string())

Scheduling.print_scheduling()