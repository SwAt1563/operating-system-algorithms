class Scheduling:
    time = []
    process_in_CPU = []
    processes_in_ready_queue = []


    @classmethod
    def scheduling(cls, current_time, p_id_progress, p_ids_ready):
        cls.time.append(current_time)
        if p_id_progress is None:
            cls.process_in_CPU.append('None')
        else:
            cls.process_in_CPU.append(p_id_progress.p_id)
        if len(p_ids_ready) == 0:
            cls.processes_in_ready_queue.append([])
        else:
            l = []
            for p in p_ids_ready:
                l.append(p.p_id)
            cls.processes_in_ready_queue.append(l)

    @classmethod
    def print_scheduling(cls):
        for i in range(len(cls.time)):
            print('At time: {}\nThe Process ID in the CPU: {}\nThe Processes IDs in the ready queue: {}'.
                  format(cls.time[i], cls.process_in_CPU[i], cls.processes_in_ready_queue[i]))