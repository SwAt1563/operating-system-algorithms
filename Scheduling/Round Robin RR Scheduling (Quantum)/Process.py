class Process:
    def __init__(self, p_id, burst_time, arrival_time):
        self.p_id = p_id
        self.burst_time = burst_time  # Progress time
        self.arrival_time = arrival_time  # When the process arrived the ready queue
        self.state = 'Created'  # Terminate, Ready, In_Progress, Created
        self.achieved_work = 0  # In_Progress time
        self.response_time = 0  # start_time - arrival_time
        self.start_time = 0  # The first time the process enter the CPU
        self.end_time = 0  # When the process finish the burst time
        self.waiting_time = 0  # The summation of the waiting time in the ready queue for the process
        self.save_waiting_time = 0  # For save the waiting time each turn
        self.turnaround_time = 0  # end_time - start_time

    @classmethod
    def check_terminate_all_processes(cls, processes):
        for p in processes:
            if p.state != 'Terminate':
                return False
        return True

    @classmethod
    def get_arrival_processes(cls, current_time, processes):
        p = []
        for process in processes:
            if process.arrival_time == current_time:
                p.append(process)
        return p


    def check_finish_process(self):
        if self.achieved_work == self.burst_time:
            return True
        return False

    def cal_turnaround_time(self):
        self.turnaround_time = self.end_time - self.start_time

    def cal_response_time(self):
        self.response_time = self.start_time - self.arrival_time


    def enter_ready_queue_first_time(self):
        self.state = "Ready"

    def enter_CPU_first_time(self, current_time):
        self.state = 'In_Progress'
        self.start_time = current_time
        self.cal_response_time()

    def enter_ready_queue(self, current_time):
        self.state = "Ready"
        self.save_waiting_time = current_time

    def enter_CPU(self, current_time):
        self.state = 'In_Progress'
        self.waiting_time += current_time - self.save_waiting_time
        self.save_waiting_time = 0

    def terminate(self, current_time):
        self.state = 'Terminate'
        self.end_time = current_time
        self.cal_turnaround_time()

    def to_string(self):
        return 'id: {}, burst_time: {}, arrival_time: {}, state: {}, achieved_work: {}, ' \
               'response_time: {}, waiting_time: {}, start_time: {}, end_time: {}, turnaround_time: {}, '.format(
            self.p_id,
            self.burst_time,
            self.arrival_time,
            self.state,
            self.achieved_work,
            self.response_time,
            self.waiting_time,
            self.start_time,
            self.end_time,
            self.turnaround_time
        )
