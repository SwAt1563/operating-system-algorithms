
class Memory:
    __MEMORY_SIZE = 0  # TAKEN FROM USER
    # the pages tables for the processes will set in the os memory size
    # each pages table for process will take just one frame
    __OPERATING_SYSTEM_SIZE = 0  # TAKEN FROM USER
    __MINIMUM_FRAMES_PER_PROCESS = 0  # TAKEN FROM USER
    __PAGE_SIZE_OF_BITS = 12  # TAKEN FROM PROJECT INFO

    def __init__(self):
        self.memory = [0] * self.__MEMORY_SIZE

    def get_page_table_of_process(self, process_id):
        from PageTable import PageTable
        for i in range(0, self.__OPERATING_SYSTEM_SIZE):
            if isinstance(self.memory[i], PageTable):
                if self.memory[i].process_id == process_id:
                    return self.memory[i]
        return None  # when the pages_table not exist

    def get_first_free_index(self):
        for i in range(self.__OPERATING_SYSTEM_SIZE, self.__MEMORY_SIZE):
            if self.memory[i] == 0:
                return i
        return -1  # when there no free space

    # page_table is isinstance of PageTable
    def set_data_from_disk_to_memory(self, page_table, address, disk, time):
        free_frame_index = self.get_first_free_index()
        self.memory[free_frame_index] = disk.get_data_by_memory_management(address)
        page_table.set_valid(address, free_frame_index, time, time)

    # page_table is isinstance of PageTable
    def free_data_from_memory_to_disk(self, page_table, address):
        frame_index = page_table.table.get_val(address)[0]
        self.memory[frame_index] = 0
        page_table.set_invalid(address)

    def free_frames_of_the_process(self, process):
        frames_addresses = process.save_pages
        page_table = self.get_page_table_of_process(process.get_id())
        for f in frames_addresses:
            self.free_data_from_memory_to_disk(page_table, f)

    # for check if we can insert new process in the memory or not
    # this function used when we have many thread work as parallel
    def check_minimum_frame_for_new_process(self):
        if self.memory[self.__OPERATING_SYSTEM_SIZE:].count(0) >= self.__MINIMUM_FRAMES_PER_PROCESS:
            return True
        return False

    def get_frame_address_from_pages_table_by_mm(self, process_id, trace):
        from PageTable import PageTable
        from Trace import Trace
        for i in range(0, self.__OPERATING_SYSTEM_SIZE):
            if isinstance(self.memory[i], PageTable):
                if self.memory[i].process_id == process_id:
                    address = Trace.get_page_number_from_trace(trace, self.__PAGE_SIZE_OF_BITS)
                    return self.memory[i].table.get_val(address)[0]
        return -1  # when the address not exist at the page table

    def create_pages_table_by_mm(self, process_id, pages_number, process_traces):
        from PageTable import PageTable
        pages_table = PageTable(process_id, pages_number, process_traces)
        no_space = True

        for i in range(0, self.__OPERATING_SYSTEM_SIZE):
            if self.memory[i] == 0:
                self.memory[i] = pages_table
                no_space = False
                break

        if no_space:
            print("The memory doesn't hsa enough space for the pages table")

    def delete_pages_table_by_mm(self, process_id):
        from PageTable import PageTable
        for i in range(0, self.__OPERATING_SYSTEM_SIZE):
            if isinstance(self.memory[i], PageTable):
                if self.memory[i].process_id == process_id:
                    self.memory[i] = 0

    # for check if the needed page for the process is in the memory or not
    # if it in the memory then nothing to do
    # but if it not in the memory the page replacement should work
    def insert_new_page_to_process_frames_by_mm(self, process, disk, time, page_replacement):
        from PageReplacement import PageReplacement
        from Trace import Trace
        address = Trace.get_page_number_from_trace(process.traces[process.save_index], self.__PAGE_SIZE_OF_BITS)
        page_table = self.get_page_table_of_process(process.get_id())

        page_entry = page_table.table.get_val(address)
        pages_faults = PageReplacement.method(self.memory, page_table.table, address, page_entry, process.save_pages,
                                              disk, process, time, page_replacement)

        process.page_faults += pages_faults
        process.save_index += 1
        return pages_faults

    # for insert the oldest pages of the process in the memory before insert the new one
    def insert_old_pages_to_process_frames_by_mm(self, process, old_address, disk, time):
        page_table = self.get_page_table_of_process(process.get_id())
        frame_index = self.get_first_free_index()
        page_table.set_valid(old_address, frame_index, time, time)
        data = disk.get_data_by_memory_management(old_address)
        self.memory[frame_index] = data

        process.page_faults += 1  # get data from disk
        return 1  # return page_fault


    @classmethod
    def get_page_size(cls):
        return cls.__PAGE_SIZE_OF_BITS

    @classmethod
    def get_min_frames_number(cls):
        return cls.__MINIMUM_FRAMES_PER_PROCESS

    @classmethod
    def get_sizes_info(cls):
        memory_size = cls.__MEMORY_SIZE
        os_size = cls.__OPERATING_SYSTEM_SIZE
        frames_size = memory_size - os_size
        return memory_size, os_size, frames_size

    @classmethod
    def set_memory_size(cls, size):
        if size >= cls.__MINIMUM_FRAMES_PER_PROCESS + cls.mm_size_condition():
            cls.__MEMORY_SIZE = size
        else:
            cls.__MEMORY_SIZE = cls.__MINIMUM_FRAMES_PER_PROCESS + cls.mm_size_condition()
            print("The size of the memory should be larger than minimum frames")

    @classmethod
    def mm_size_condition(cls):
        from Process import Process
        return Process.number_of_processes()

    @classmethod
    def set_os_size(cls, size):
        if cls.__MEMORY_SIZE > size >= cls.mm_size_condition() and cls.__MEMORY_SIZE - size >= cls.__MINIMUM_FRAMES_PER_PROCESS:
            cls.__OPERATING_SYSTEM_SIZE = size
        else:
            cls.__OPERATING_SYSTEM_SIZE = cls.mm_size_condition()
            print("The OS SYSTEM size should be less than Memory size and larger or equal to the number of processes")

    @classmethod
    def set_min_framers_per_process(cls, num):
        if num >= 1:
            cls.__MINIMUM_FRAMES_PER_PROCESS = num
        else:
            cls.__MINIMUM_FRAMES_PER_PROCESS = 1
            print("The minimum frames should be larger than zero")
