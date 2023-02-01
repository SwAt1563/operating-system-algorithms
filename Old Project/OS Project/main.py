from CPU import CPU
from Process import Process
from Thread import Thread
from Simulation import Simulation
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from PageReplacement import PageReplacement

# THE TITLES FOR THE CREATED TABLE
titles = ("Process_id", "Arrival_time", "Duration_time", "Start_time", "End_time", "Turnaround_time",
          "Waiting_time", "Page_faults")


# FOR CREATE GUI TABLE
class Table:

    # frame: THE WINDOW WHICH WE WANT TO SHOW THE TABLE ON IT
    def __init__(self, frame):
        # FOR INSERT THE TITLES AS THE FIRST ROW IN THE TABLE
        # AND MAKE 7 COLUMNS
        for i in range(len(titles)):
            x = Label(frame, text=titles[i], borderwidth=1, relief="solid", width=20, fg='#ffffff', bg="#009879",
                      font=('tajawal', 10, 'bold'))
            x.grid(row=0, column=i)

        all_processes = Process.get_all_processes(processing_threads[0])
        table_rows = []
        for process in all_processes:
            table_rows.append(
                [process.get_id(), process.arrival_time, process.duration_time, process.start_time, process.end_time,
                 process.turnaround,
                 process.waiting_time, process.page_faults])
        # FOR INSERT THE PROCESSES INFORMATION AND THE Scheduling RESULTS AS ROWS IN THE TABLE
        for i in range(len(all_processes)):
            for j in range(len(titles)):
                if i % 2 == 0:
                    self.e = Label(frame, text=table_rows[i][j], borderwidth=1, relief="solid", width=20, fg='black',
                                   bg="#f3f3f3", font=('tajawal', 10, 'bold'))
                else:
                    self.e = Label(frame, text=table_rows[i][j], borderwidth=1, relief="solid", width=20, fg='black',
                                   bg="#dddddd", font=('tajawal', 10, 'bold'))

                self.e.grid(row=i + 1, column=j)


file_path = ""  # for save the path of the data file
dictionary_path = ""  # for save the dictionary which save all processes traces
quantum_value = 0  # for read the quantum from user
threads_number = 0  # for read the number of threads from user
page_replacement_algorithm = ""  # for choose the page replacement algorithm from user
correct_file = False  # if the user choose correct file


def browse_files():
    global file_path, correct_file, dictionary_path
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    try:
        path = str(filename)
        my_file = Path(path)
        if not my_file.is_file():
            raise FileNotFoundError
        file_path = path
        dictionary_path = "/".join(file_path.split("/")[:-1]) + "/"
        correct_file = True

    except FileNotFoundError:
        correct_file = False
        print("The File Not Exist")


# SUBMIT PARAMETERS BUTTON FUNCTION
def save_parameters():
    global quantum_value, threads_number, page_replacement_algorithm
    end = True
    try:
        quantum = int(dynamic_quantum.get())
        if quantum <= 1:
            raise Exception
        quantum_value = quantum
    except Exception:
        end = False
        dynamic_quantum.set("At least the minimum frames + 1")
    try:
        threads = int(dynamic_threads.get())
        if threads <= 2:
            raise Exception
        threads_number = threads
    except Exception:
        end = False
        dynamic_threads.set("At least 3 threads")
    try:
        algorithm = str(dynamic_algorithm.get())
        if algorithm != PageReplacement.FIFO and algorithm != PageReplacement.LRU:
            raise Exception
        page_replacement_algorithm = algorithm
    except Exception:
        end = False
        dynamic_algorithm.set("Wrong")

    if end and correct_file:
        parameters_window.destroy()


# PARAMETERS WINDOW
parameters_window = Tk()
parameters_window.configure(bg='#0B2F3A')
parameters_window.minsize(300, 300)
parameters_window.title("Define Parameters for The Virtual Memory Management Simulation")
parameters_window.resizable(width=0, height=0)

# DYNAMIC TEXT FIELD VALUES WITH DEFAULT VALUES
dynamic_quantum = IntVar(parameters_window, 3)
dynamic_threads = IntVar(parameters_window, 3)
dynamic_algorithm = StringVar(parameters_window)

# MAIN FRAME CONTAIN ALL THE LABELS AND BUTTON AND TEXT FIELDS
MainFrame = Frame(parameters_window, bd=100, width=1050, height=700, bg="#333333")
MainFrame.grid()

path_label = Label(MainFrame, width=20, height=2, text="Path", fg="gold", bg="#333333",
                   font=('tajawal', 20, 'bold')).grid(row=1, column=1)
button_explore = Button(MainFrame, width=10, font=('tajawal', 20, 'bold'),
                        text="Browse File", command=browse_files).grid(row=1, column=2)

quantum_label = Label(MainFrame, width=0, height=2, text="Quantum value", fg="gold", bg="#333333",
                      font=('tajawal', 20, 'bold')).grid(row=2, column=1)
quantum_text = Entry(MainFrame, width=21, textvariable=dynamic_quantum, font=('tajawal', 20, 'bold')).grid(row=2,
                                                                                                           column=2)

threads_label = Label(MainFrame, width=20, height=2, text="Threads number", fg="gold", bg="#333333",
                      font=('tajawal', 20, 'bold')).grid(row=3, column=1)
threads_text = Entry(MainFrame, width=21, textvariable=dynamic_threads, font=('tajawal', 20, 'bold')).grid(row=3,
                                                                                                           column=2)

algorithm_label = Label(MainFrame, width=20, height=2, text="Algorithm", fg="gold", bg="#333333",
                        font=('tajawal', 20, 'bold')).grid(row=4, column=1)

algorithm_box = ttk.Combobox(MainFrame, width=20, font=('tajawal', 20, 'bold'),
                             textvariable=dynamic_algorithm)

# Adding combobox drop down list
algorithm_box['values'] = ('LRU', 'FIFO')

algorithm_box.grid(row=4, column=2)

# Shows february as a default value
algorithm_box.current(1)

Label(MainFrame, height=2, bg="#333333").grid(row=5, column=1, columnspan=2)

button = Button(MainFrame, width=15, text="Submit", command=save_parameters, fg="black", bg="#DBA901",
                font=('tajawal', 20, 'bold')).grid(row=6, column=1, columnspan=2)

# CONTINUE THE LOOP OF PARAMETERS WINDOW UNTIL THE USER ENTER VALIDATED DATA
parameters_window.mainloop()

# for start the program
mm_thread, disk_thread = CPU.start_the_program(file_path, dictionary_path, threads_number, quantum_value)
processing_threads = []

# CPU.get_max_number_of_threads() - 2 ; dynamic threads number
for i in range(1):
    processing_threads.append(Thread.create_thread())
    processing_threads[i].set_thread_for_processes()

for thread in processing_threads:
    thread.processing(mm_thread, disk_thread, page_replacement_algorithm)
    # for print the simulation at console
    Simulation.simulation(thread)

# for create the Scheduling Table
table_window = Tk()
table_window.title("Scheduling Results")
table_window.minsize(1315, 300)
table_window.resizable(width=0, height=0)

# Create A Main Frame
main_frame = Frame(table_window)
main_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas)

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

# FOR CREATE TABLE DEPEND ON THE BEST RESULT OF THE ALGORITHMS
t = Table(second_frame)

# END THE PROGRAM WHEN CLOSE THE TABLE
table_window.mainloop()
