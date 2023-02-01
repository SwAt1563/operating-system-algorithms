
class Scheduling:
    times = []
    memory_traces = []
    p_ids = []

    @classmethod
    def scheduling(cls, time, p_id, memory):
        cls.times.append(time)
        cls.p_ids.append(p_id)
        ids = []
        for frame in memory:
            ids.append(frame[0])
        cls.memory_traces.append(ids)

    @classmethod
    def print_scheduling(cls):
        for i in range(len(cls.times)):
            print('At time: {}\nCurrent Page: {}\nMemory: {}\n'.
                  format(cls.times[i], cls.p_ids[i], cls.memory_traces[i]))
