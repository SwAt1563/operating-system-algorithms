from HashTable import HashTable


class PageTable:

    def __init__(self, process_id, pages_number, process_traces):
        self.process_id = process_id  # for save this page table for which process
        self.pages_number = pages_number  # for save the number of pages of the process
        self.memory_addresses = self.get_reference_strings(process_traces)  # for save the list of the address
        self.table = HashTable(pages_number)  # for make hash table
        self.set_invalid_initially()  # for set the current pages initially invalid cuz it in the disk

    # for change the list of traces to list of addresses
    @classmethod
    def get_reference_strings(cls, process_traces):
        from Trace import Trace
        from Memory import Memory
        memory_traces = []
        size = len(process_traces)
        for i in range(size):
            reference_string = Trace.get_page_number_from_trace(process_traces[i], Memory.get_page_size())
            if memory_traces.count(reference_string) == 0:
                memory_traces.append(reference_string)
        return memory_traces

    # page table entry = invalid/frame_address(valid), time_when_put_in_memory, time_update_in_memory
    def set_invalid_initially(self):
        for address in self.memory_addresses:
            self.table.set_val(address, [0, 0, 0])

    # when send data from memory to disk
    def set_invalid(self, address):
        self.table.set_val(address, [0, 0, 0])

    # when get data from disk to memory
    def set_valid(self, address, frame_index, time1, time2):
        self.table.set_val(address, [frame_index, time1, time2])

    # update the page table
    def update_page_table(self, old_address, new_address, frame_index, time1, time2):
        self.set_invalid(old_address)
        self.set_valid(new_address, frame_index, time1, time2)


