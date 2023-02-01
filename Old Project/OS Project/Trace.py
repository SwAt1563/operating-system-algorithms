import math
import random


class Trace:
    # the traces form in the files
    __ADDRESS_FORM = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']

    # for save the traces of the process in this object
    # address_length = page_number
    def __init__(self, process_id, process_size, page_size_by_bits):
        self.process_id = process_id
        self.memory_traces = []
        self.address_length, self.pages_number = self.get_length_of_address_and_pages_number(process_size,
                                                                                             page_size_by_bits)

    def set_random_memory_trace(self):
        self.memory_traces = self.create_random_memory_traces(self.address_length, self.pages_number)

    # page_size = 12 bits, given from project
    # for get the number of pages and the length of the traces
    @classmethod
    def get_length_of_address_and_pages_number(cls, process_size, page_size_by_bits):
        lower_digits = cls.__get_num_of_digits_by_hex_form(page_size_by_bits)
        pages_number = cls.get_pages_number(process_size, page_size_by_bits)
        number_of_pages_by_bits = cls.__get_number_of_bits_based_on_number_of_pages(pages_number)
        upper_digits = cls.__get_num_of_digits_by_hex_form(number_of_pages_by_bits)
        length_of_address = upper_digits + lower_digits
        return length_of_address, pages_number

    # 12 bits = 3 number of hex. digits
    # each 4 bits = 1 digit of hex.
    @classmethod
    def __get_num_of_digits_by_hex_form(cls, bits):
        return math.ceil(bits / 4)

    # process size = 10000byte
    # page_size_by_bits = 12
    # page_size = 2 ^ 12 = 4096 byte
    # pages_number = ceil(10000 / 4096) = 3
    @classmethod
    def get_pages_number(cls, process_size, page_size_by_bits):
        page_size = math.pow(2, page_size_by_bits)
        pages_number = math.ceil(process_size / page_size)
        return pages_number

    # 3 pages need 2 bits
    # 5 pages need 3 bits
    # 1 or 2 pages need 1 bit
    @classmethod
    def __get_number_of_bits_based_on_number_of_pages(cls, pages_number):
        if pages_number == 1:
            return 1
        return math.ceil(math.log(pages_number) / math.log(2))

    # for create random memory traces
    @classmethod
    def create_random_memory_traces(cls, address_length, pages_number):
        memory_traces = []
        for i in range(pages_number):
            address = []
            for j in range(address_length):
                address.append(random.choice(cls.__ADDRESS_FORM))
            address = list(map(str, address))
            address = "".join(address)
            memory_traces.append(address)
        return memory_traces

    # for change the trace to address
    @classmethod
    def get_page_number_from_trace(cls, trace, page_size_by_bits):
        lower_digits = cls.__get_num_of_digits_by_hex_form(page_size_by_bits)
        upper_digits = len(trace) - lower_digits
        page_number = trace[0: upper_digits]
        return page_number

    # for create file for process traces
    @classmethod
    def write_memory_traces_on_file(cls, process_id, memory_trace, dictionary_path):
        file = open("{0}P{1}".format(dictionary_path, process_id), "w")
        num_of_lines = len(memory_trace)

        for i in range(num_of_lines):
            file.write(memory_trace[i])
            file.write("\n")
        file.close()

    # for read the process traces file
    @classmethod
    def read_memory_traces_from_file(cls, process_id, dictionary_path):
        file = open("{0}P{1}".format(dictionary_path, process_id), "r")
        memory_traces = []
        for line in file.readlines():
            if line != "\n":
                memory_traces.append(line.replace("\n", ""))
        file.close()
        return memory_traces
