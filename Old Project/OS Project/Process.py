

class Process:

    __Processes_list = []  # for save the created processes

    def __init__(self, p_id, traces, size, arrival_time, duration_time):
        self.__id = p_id
        self.traces = traces  # it length equal to number of pages
        self.size = size  # in byte
        self.arrival_time = arrival_time  # the time when enter the queue
        self.duration_time = duration_time  # burst time = number of pages: each page take one unit of time
        self.state = "created"  # for save the state of the process ['ready', 'execution', 'finished']
        self.save_index = 0  # for save the last index of traces should be in the next state
        self.save_pages = []  # for save the last processing pages before enter the ready queue
        self.time = 0  # for put the time before the process enter the ready queue
        self.waiting_time = 0  # for save the times of the process in the ready queue
        self.processing_time = 0  # will increasing until reach duration_time
        self.start_time = 0  # will start when the process set in the ready queue at first time
        self.end_time = 0  # will end when the processing_time == duration_time
        self.turnaround = 0  # end_time - start_time
        self.page_faults = 0  # will increase by the page replacement algorithm
        self.exist_in_memory = False  # for check if the process has frames in the memory

        Process.insert_new_process(self)

    # just the mm_thread or processing_thread can access this function
    @classmethod
    def get_all_processes(cls, check_thread):
        if check_thread.mm_exist or check_thread.processing_thread:
            return cls.__Processes_list

    @classmethod
    def number_of_processes(cls):
        return len(cls.__Processes_list)

    # for insert it in the disk initially
    @classmethod
    def get_traces_of_processes(cls, disk_thread):
        if disk_thread.disk_exist:
            traces_list = []
            for p in cls.__Processes_list:
                traces_list.append(p.traces)
            return traces_list
        return None


    @classmethod
    def check_all_processes_finished(cls):
        done = True
        for p in cls.__Processes_list:
            if p.state != 'finished':
                done = False
                break
        return done

    # for check if there new process came while scheduling
    @classmethod
    def get_new_processes(cls, arrival_time):
        arrival_processes = []
        for p in cls.__Processes_list:
            if p.arrival_time == arrival_time:
                arrival_processes.append(p)
        return arrival_processes

    @classmethod
    def insert_new_process(cls, p):
        cls.__Processes_list.append(p)

    def get_id(self):
        return self.__id

    def get_current_trace(self):
        if self.save_index != len(self.traces):
            return self.traces[self.save_index]
        return -1  # when all pages done

    def set_turnaround_time(self):
        self.turnaround = self.end_time - self.start_time

    # when the process arrive the ready queue at first time
    def enter_ready_queue_initially(self, time):
        self.start_time = time  # the first time the process inter the ready_queue
        self.enter_ready_queue(time)

    def enter_ready_queue(self, time):
        self.state = 'ready'
        self.time = time  # the time when enter the ready_queue

    def enter_thread(self, time):
        self.state = 'execution'
        self.waiting_time += time - self.time
        self.time = 0

    # when the process finished processing
    def set_finished_if_done(self, time):
        try:
            if self.duration_time < self.processing_time:
                raise Exception
        except Exception as LD:
            print("The duration time of the P{0} finished, not enough time for all traces".format(self.__id))
            exit(-1)

        if self.processing_time == len(self.traces):
            self.state = 'finished'
            self.end_time = time
            self.set_turnaround_time()
            return True
        return False

