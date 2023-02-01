
class PageReplacement:
    FIFO = "FIFO"
    LRU = "LRU"

    @classmethod
    def FIFO_MIN(cls, page):
        return page[1]

    @classmethod
    def LRU_MIN(cls, page):
        return page[2]

    # page_table = hash_table
    @classmethod
    def method(cls, memory, page_table, address, new_page_entry, current_pages, disk, process, current_time,
               page_replacement_METHOD):
        from Memory import Memory

        if new_page_entry[0] != 0:  # the page already in the memory
            # for update the time for the page
            page_table.set_val(address, [new_page_entry[0], new_page_entry[1], current_time])

            return 0  # if the page already in the memory
        else:  # if the page in the disk not in the memory
            max_number_of_pages = Memory.get_min_frames_number()
            if len(current_pages) != max_number_of_pages:  # there is enough space for new page to put in the memory
                data_from_disk = disk.get_data_by_memory_management(address)
                frame_index = 0

                for i in range(Memory.get_sizes_info()[1], Memory.get_sizes_info()[0]):
                    if memory[i] == 0:
                        frame_index = i
                        break
                memory[frame_index] = data_from_disk
                page_table.set_val(address, [frame_index, current_time, current_time])
                process.save_pages.append(address)

            else:  # when the process has max_number_of_pages
                data_from_disk = disk.get_data_by_memory_management(address)
                pages_table_entries = []
                for adds in current_pages:
                    pages_table_entries.append(page_table.get_val(adds))

                victim_page_entry = 0
                if page_replacement_METHOD == PageReplacement.FIFO:
                    victim_page_entry = min(pages_table_entries, key=cls.FIFO_MIN)
                elif page_replacement_METHOD == PageReplacement.LRU:
                    victim_page_entry = min(pages_table_entries, key=cls.LRU_MIN)

                victim_page_address = 0
                for adds in current_pages:
                    if page_table.get_val(adds) == victim_page_entry:
                        victim_page_address = adds
                        break

                frame_index = victim_page_entry[0]  # for take the frame address from old page to the new page
                memory[frame_index] = data_from_disk  # for update to new data
                page_table.set_val(victim_page_address, [0, 0, 0])
                page_table.set_val(address, [frame_index, current_time, current_time])
                process.save_pages.remove(victim_page_address)
                process.save_pages.append(address)

        return 1  # cuz we should go to disk to get the data
