class Scheduling:
    times = 0
    operations = []



    @classmethod
    def scheduling(cls, time, p_id, resources_state, process_needs, available):
        cls.operations.append([time, p_id, resources_state, process_needs, available])


    @classmethod
    def print_scheduling(cls):
        time = 0
        print()
        for i in range(len(cls.operations)):
            if cls.operations[i][0] != time:
                time = cls.operations[i][0]
                print('At time: {}\n'.format(time))
            print('The Process ID: {}\nThe Resources available size: {}\nThe Process remaining requests: {'
                  '}\nAvailable: {}\n'.
                  format(cls.operations[i][1], cls.operations[i][2], cls.operations[i][3], cls.operations[i][4]))