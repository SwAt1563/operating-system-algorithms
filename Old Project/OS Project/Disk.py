

class Disk:
    __DISK_SIZE = 0  # TAKEN FROM USER
    __MOVE_CYCLES_FROM_DISK_TO_MEMORY = 300  # TAKEN FROM PROJECT INFO

    def __init__(self):
        self.__data_list = [0] * self.__DISK_SIZE

    def clear_disk(self):
        for i in range(self.__DISK_SIZE):
            self.__data_list[i] = 0

    @classmethod
    def get_search_cycles(cls):
        return cls.__MOVE_CYCLES_FROM_DISK_TO_MEMORY

    @classmethod
    def set_disk_size(cls, size):
        from Memory import Memory
        if size > 0 and size >= 10 * Memory.get_sizes_info()[0]:
            cls.__DISK_SIZE = size
        else:
            cls.__DISK_SIZE = 10 * Memory.get_sizes_info()[0]
            print("At least the disk size should be 10 duplicate of the memory size")

    @classmethod
    def get_disk_size(cls):
        return cls.__DISK_SIZE

    def load_data_on_disk_initially(self, process_traces):
        from Trace import Trace
        from Memory import Memory
        num_of_traces = len(process_traces)
        count = 0
        for i in range(self.__DISK_SIZE):
            if count == num_of_traces:
                break
            if self.__data_list[i] == 0:
                address = Trace.get_page_number_from_trace(process_traces[count], Memory.get_page_size())
                if self.__data_list.count(address) == 0:
                    self.__data_list[i] = address
                count += 1

    # address = page number
    def insert_data_by_memory_management(self, address):
        for i in range(self.__DISK_SIZE):
            if self.__data_list[i] == 0:
                self.__data_list[i] = address

    # address = page number
    def get_data_by_memory_management(self, address):
        for i in range(self.__DISK_SIZE):
            if self.__data_list[i] == address:
                # self.__data_list[i] = 0  # when take data from disk we didn't delete it from the disk
                return self.__data_list[i]







