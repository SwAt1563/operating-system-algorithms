from Process import Process
from Trace import Trace


class CPU:
    _MAX_NUMBER_OF_NUMBER = 0  # READ FROM USER
    _waiting_queue = []  # WE WILL NOT USE IT CUZ NO I/O IN THIS PROJECT
    _QUANTUM = 0  # READ FROM USER
    _CONTEXT_SWITCHING_TIME_BY_CYCLE = 5  # WRITTEN IN PROJECT

    @classmethod
    def get_max_number_of_threads(cls):
        return cls._MAX_NUMBER_OF_NUMBER

    @classmethod
    def set_number_of_threads(cls, num):
        if num > 2:
            cls._MAX_NUMBER_OF_NUMBER = num
        else:
            cls._MAX_NUMBER_OF_NUMBER = 3
            print("At least 3 threads one for memory management and disk and the other processes")

    @classmethod
    def set_quantum(cls, q):
        from Memory import Memory
        # min_frames for put the oldest frames in the memory
        # then make replacement for the new pages
        if q >= Memory.get_min_frames_number() + 1:
            cls._QUANTUM = q
        else:
            cls._QUANTUM = Memory.get_min_frames_number() + 1
            print("the quantum should be larger than {0}".format(Memory.get_min_frames_number()))

    @classmethod
    def insert_the_beginning_process_at_time_zero_to_the_ready_queue(cls, ready_queue):
        arrival_processes = Process.get_new_processes(0)
        for p in arrival_processes:
            cls.insert_process_in_ready_queue_initially(p, 0, ready_queue)

    @classmethod
    def insert_process_in_ready_queue_initially(cls, process, arrival_time, ready_queue):
        process.enter_ready_queue_initially(arrival_time)
        ready_queue.append(process)

    @classmethod
    def insert_process_in_ready_queue(cls, process, time, ready_queue):
        process.enter_ready_queue(time)
        ready_queue.append(process)

    # this function used when there a priority
    @classmethod
    def get_process_from_ready_queue_to_thread(cls, process_id, ready_queue):
        for p in ready_queue:
            if p.get_id() == process_id:
                process = p
                ready_queue.remove(p)
                process.enter_thread()
                return process

        print("The process {0} not in the ready queue".format(process_id))
        return None

    # FIFO : FIRST IN FIRST OUT : THE OLDEST PROCESS WILL BE AT INDEX[0] AND THE NEW ONE AT THE END
    @classmethod
    def get_process_from_ready_queue(cls, time, ready_queue):
        if len(ready_queue) == 0:
            return None
        else:
            process = ready_queue[0]
            process.enter_thread(time)
            ready_queue.remove(process)
            return process

    @classmethod
    def start_the_program(cls, file_path, dictionary_path, threads_num, quantum):
        from Memory import Memory
        from Disk import Disk
        from Thread import Thread
        # firstly for create the processes
        file = open(file_path, "r")
        all_lines = file.readlines()
        num_of_processes = int(all_lines[0])
        memory_size = int(all_lines[1])
        min_frames = int(all_lines[2])

        for i in range(3, num_of_processes + 3):
            if all_lines[i] != "\n":
                p_id, arrival_time, duration_time, p_size = list(map(int, all_lines[i].split(" ")))
                memory_traces = Trace.read_memory_traces_from_file(p_id, dictionary_path)
                Process(p_id, memory_traces, p_size, arrival_time, duration_time)
        file.close()

        # for initialize memory sizes
        Memory.set_min_framers_per_process(min_frames)
        Memory.set_memory_size(memory_size)
        Memory.set_os_size(num_of_processes)

        # for initialize disk size
        Disk.set_disk_size(10 * memory_size)

        # for initialize number of threads
        cls.set_number_of_threads(threads_num)

        # for initialize the quantum
        cls.set_quantum(quantum)

        # for create memory and disk
        memory = Memory()
        disk = Disk()

        # for crete threads for mm and disk
        mm_thread = Thread.create_thread()
        mm_thread.set_mm_in_thread(memory)
        disk_thread = Thread.create_thread()
        disk_thread.set_disk_in_thread(disk)

        # for insert all data on the disk initially
        disk_thread.thread_of_disk_insert_data_initially_in_disk()

        # for create pages table for each process
        mm_thread.thread_of_mm_create_pages_tables_initially()

        return mm_thread, disk_thread
