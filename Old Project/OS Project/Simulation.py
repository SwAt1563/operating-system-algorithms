
class Simulation:
    __memory_steps = []
    __ready_queue_steps = []
    __current_processes_in_thread = []

    @classmethod
    def add_all(cls, process_id, memory, ready_queue, time):
        cls.add_process_id(process_id, time)
        cls.add_memory_step(memory, time)
        cls.add_queue_step(ready_queue, time)

    @classmethod
    def add_process_id(cls, process_id, time):
        cls.__current_processes_in_thread.append([time, process_id])

    @classmethod
    def add_memory_step(cls, memory, time):
        cls.__memory_steps.append([time, memory])

    @classmethod
    def add_queue_step(cls, ready_queue, time):
        processes_id = []
        for p in ready_queue:
            processes_id.append(p.get_id())
        cls.__ready_queue_steps.append([time, processes_id])


    @classmethod
    def __get_list_of_ids_for_pages_tables(cls, mm_memory):
        from PageTable import PageTable
        p_ids = []
        for m in mm_memory:
            if isinstance(m, PageTable):
                p_ids.append("P{0}_PageTable".format(m.process_id))
            else:
                p_ids.append("X")  # if the frame empty
        return p_ids
    @classmethod
    def divide_the_data(cls):
        from Memory import Memory
        times = []
        page_tables = []
        frames_of_processes = []
        ready_queue = []
        processes_ids = []
        for m in cls.__memory_steps:
            times.append(m[0])
            page_tables.append(cls.__get_list_of_ids_for_pages_tables(m[1][0:Memory.get_sizes_info()[1]]))
            frames_of_processes.append(m[1][Memory.get_sizes_info()[1]:])
        for q in cls.__ready_queue_steps:
            ready_queue.append(q[1])

        for p_id in cls.__current_processes_in_thread:
            processes_ids.append(p_id[1])

        return times, processes_ids, ready_queue, page_tables, frames_of_processes
    @classmethod
    def simulation(cls, processing_thread):
        cycles = processing_thread.cycles
        finish_time = processing_thread.work_time
        print("The Cycles: {0}".format(cycles))
        print("The Finished Time By Quantum : {0}".format(finish_time))

        times, processes_ids, ready_queue, page_tables, frames_of_processes = cls.divide_the_data()
        for i in range(finish_time + 2):
            print("At time {0}: ".format(times[i]))
            if processes_ids[i] == "None":
                print("The thread doesn't have any processes work on it")
            else:
                print("The current process in the thread: P{0}".format(processes_ids[i]))
            print("Ready_queue: {0}".format(ready_queue[i]))
            print("Memory Management: {0}".format(page_tables[i]))
            print("Memory: {0}".format(frames_of_processes[i]))

        print("Finish The Simulation")
