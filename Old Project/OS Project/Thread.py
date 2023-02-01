from CPU import CPU
from Process import Process
from Trace import Trace
from Simulation import Simulation


# one thread for memory management for updating the pages tables
# and one thread for disk access
# other threads for processes


class Thread(CPU):
    __NUMBER_OF_CREATED_THREADS = 0

    def __init__(self):
        self.processing_thread = False  # if this thread used for processes
        self.process = None  # if this thread for process then self.process should equal to the process reference
        self.work_time = 0  # for save the processing time
        self.cycles = 0
        self.ready_queue = []
        self.mm_exist = False  # if this thread for memory management then mm_exist should equal True
        self.mm = None
        self.disk_exist = False  # if this thread for disk then disk_exist should equal True
        self.disk = None

    # for not allowed to create more than THREADS_NUMBER
    @classmethod
    def create_thread(cls):
        if cls._MAX_NUMBER_OF_NUMBER <= cls.__NUMBER_OF_CREATED_THREADS:
            print("You can't create more than {0} threads".format(cls._MAX_NUMBER_OF_NUMBER))
            return None
        cls.__NUMBER_OF_CREATED_THREADS += 1
        return cls()

    # each page reference take one quantum
    # if quantum = 3, then there is 3 page references
    def processing(self, mm_thread, disk_thread, page_replacement):
        if self.processing_thread:
            self.insert_the_beginning_process_at_time_zero_to_the_ready_queue(self.ready_queue)
            # insert the data for simulation
            Simulation.add_all("None", mm_thread.mm.memory.copy(), self.ready_queue, self.work_time)
            while True:

                current_process = self.get_process_from_ready_queue(self.work_time, self.ready_queue)
                if current_process is None:  # when no any process in the ready queue
                    check_done = Process.check_all_processes_finished()  # check if the all processes finished
                    if check_done:
                        # insert the data for simulation
                        # when clear the memory then we should put the time plus one
                        Simulation.add_all("None", mm_thread.mm.memory.copy(), self.ready_queue, self.work_time + 1)
                        break
                    else:
                        self.work_time += 1  # if the processes not finished yet and not enter the ready queue
                        # for get the arrival processes and put them in the ready queue
                        arrival_processes = Process.get_new_processes(self.work_time)
                        for p in arrival_processes:
                            self.insert_process_in_ready_queue_initially(p, self.work_time, self.ready_queue)
                        # insert the data for simulation
                        Simulation.add_all("None", mm_thread.mm.memory.copy(), self.ready_queue, self.work_time)

                else:
                    # put the process in the thread
                    self.process = current_process
                    # Context switching should take 5 cycles
                    self.cycles += self._CONTEXT_SWITCHING_TIME_BY_CYCLE
                    memory_accesses = 0
                    check_current_process = False
                    # for insert the oldest pages in the memory before the new one
                    old_pages = self.process.save_pages
                    number_of_old_pages = len(old_pages)
                    old_pages_counter = 0

                    while memory_accesses != self._QUANTUM:

                        # for put the oldest pages in the memory after make page replacement for the new page
                        if not self.process.exist_in_memory and old_pages_counter != number_of_old_pages:
                            page_faults = mm_thread.mm.insert_old_pages_to_process_frames_by_mm(self.process,
                                                                                                old_pages[
                                                                                                    old_pages_counter],
                                                                                                disk_thread.disk,
                                                                                                self.work_time)
                            old_pages_counter += 1

                        else:
                            page_faults = mm_thread.mm.insert_new_page_to_process_frames_by_mm(self.process,
                                                                                               disk_thread.disk,
                                                                                               self.work_time,
                                                                                               page_replacement)
                            # in the else scope
                            ###
                            self.process.processing_time += 1  # when insert new page in the memory
                            self.process.exist_in_memory = True
                            ###

                        self.work_time += 1
                        # memory references should take 1 cycle
                        self.cycles += 1
                        # disk reference should take 300 cycle
                        self.cycles += page_faults * disk_thread.disk.get_search_cycles()
                        memory_accesses += 1
                        check_process_done = self.process.set_finished_if_done(self.work_time)

                        # for insert the arrival processes in the ready queue
                        arrival_processes = Process.get_new_processes(self.work_time)
                        for p in arrival_processes:
                            self.insert_process_in_ready_queue_initially(p, self.work_time, self.ready_queue)

                        # insert the data for simulation
                        Simulation.add_all(self.process.get_id(), mm_thread.mm.memory.copy(), self.ready_queue,
                                           self.work_time)

                        if check_process_done:
                            # for clear the process from memory
                            mm_thread.thread_of_mm_clear_the_process_from_memory(self.process)
                            self.process = None
                            check_current_process = True
                            break

                    # if the current process not finish it work yet
                    if not check_current_process:
                        self.insert_process_in_ready_queue(self.process, self.work_time, self.ready_queue)
                        # if there enough frames for new process then don't delete the frames of the current process
                        if not mm_thread.mm.check_minimum_frame_for_new_process() and len(self.ready_queue) > 1:
                            mm_thread.thread_of_mm_clear_frames_of_the_process(self.process)
                            self.process.exist_in_memory = False
                        self.process = None

    # when create processing thread
    def set_thread_for_processes(self):
        self.processing_thread = True

    # for let the access of memory by the thread
    def set_mm_in_thread(self, memory):
        self.mm_exist = True
        self.mm = memory

    # for let the access of disk by the thread
    def set_disk_in_thread(self, disk):
        self.disk_exist = True
        self.disk = disk

    def thread_of_disk_insert_data_initially_in_disk(self):
        if self.disk_exist:
            traces_of_processes = Process.get_traces_of_processes(self)
            for traces in traces_of_processes:
                self.disk.load_data_on_disk_initially(traces)

    def thread_of_mm_clear_frames_of_the_process(self, process):
        if self.mm_exist:
            self.mm.free_frames_of_the_process(process)

    def thread_of_mm_clear_the_process_from_memory(self, process):
        if self.mm_exist:
            self.mm.free_frames_of_the_process(process)
            self.mm.delete_pages_table_by_mm(process.get_id())

    def thread_of_mm_create_pages_tables_initially(self):
        if self.mm_exist:
            all_processes = Process.get_all_processes(self)
            for process in all_processes:
                self.mm.create_pages_table_by_mm(process.get_id(),
                                                 Trace.get_pages_number(process.size, self.mm.get_page_size()),
                                                 process.traces)
