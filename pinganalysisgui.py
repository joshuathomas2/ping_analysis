from tkinter import *
import pinganalysis as pa


class PingAnalysisGui:
    def __init__(self):
        self.DIRECTORY = "raw_data"
        self.FONT = ("Times New Roman", "12")
        self.FONT_LARGE = ("Times New Roman", "24", "bold")
        self.FONT_MEDIUM = ("Times New Roman", "16", "bold")

        self.root = Tk()
        self.root.title("Ping Analysis")
        self.root.geometry("750x500")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(side=LEFT, fill=BOTH)

        self.data_frame = Frame(self.root)
        self.data_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.listbox_data = Listbox(self.main_frame, bg="gray", height=25)
        self.listbox_data.pack(side=TOP)

        self.label_title = Label(self.data_frame, height=3, text="Ping Analysis", font=self.FONT_LARGE)
        self.label_title.pack(fill=X)

        self.label_error = Label(self.data_frame, fg="red", font=self.FONT_LARGE)
        self.label_error.pack()

        self.label_file = Label(self.data_frame, height=2, font=self.FONT_MEDIUM)
        self.label_file.pack()

        self.label_tiny_ping = Label(self.data_frame)
        self.label_tiny_ping.pack()

        self.label_small_ping = Label(self.data_frame)
        self.label_small_ping.pack()

        self.label_medium_ping = Label(self.data_frame)
        self.label_medium_ping.pack()

        self.label_large_ping = Label(self.data_frame)
        self.label_large_ping.pack()

        self.label_extreme_ping = Label(self.data_frame)
        self.label_extreme_ping.pack()

        self.label_max_ping = Label(self.data_frame, font=self.FONT_MEDIUM)
        self.label_max_ping.pack()

        self.label_min_ping = Label(self.data_frame, font=self.FONT_MEDIUM)
        self.label_min_ping.pack()

        self.label_mean_ping = Label(self.data_frame, font=self.FONT_MEDIUM)
        self.label_mean_ping.pack()

        self.analyze_button = Button(self.main_frame, text="Analyze")
        self.analyze_button.pack(fill=BOTH, expand=1)

        self.refresh_button = Button(self.main_frame, text="Refresh List")
        self.refresh_button.pack(fill=BOTH, expand=1)

        self.selection_index = None
        self.selection = None

    def start_mainloop(self):
        self.root.mainloop()

    def populate_listbox(self, data):
        self.clear_listbox()
        for item in data:
            self.listbox_data.insert("end", item)

    def clear_listbox(self):
        self.listbox_data.delete(0, END)

    def get_selection(self):
        self.selection_index = self.listbox_data.curselection()

        try:
            self.selection = self.listbox_data.get(self.selection_index)
            print(self.selection)
        except TclError:
            print("Invalid selection")

    def configure_buttons(self):
        self.analyze_button.configure(command=self.analyze)
        self.refresh_button.configure(command=lambda: self.populate_listbox(pa.get_data(self.DIRECTORY)))

    def analyze(self):
        ping_list = []
        ping_count = 0
        lagspike_count = 0
        average_ping = 0
        tiny_ping_count = 0
        small_ping_count = 0
        medium_ping_count = 0
        large_ping_count = 0
        extreme_ping_count = 0
        error = False

        self.label_error.configure(text="")
        self.get_selection()

        if self.selection is None:
            self.label_error.configure(text="ERROR: No file selected")
            error = True
        else:
            raw_data_file = open(self.DIRECTORY + "/" + self.selection)

            for line in raw_data_file:
                if line[0:5] == "Reply":
                    ping_count += 1
                    ping_time = int(re.split(" ", line)[4][5:][:-2])
                    ping_list.append(ping_time)

            if len(ping_list) == 0:
                self.label_error.configure(text="ERROR: No data or file is not UTF-8")
                error = True
            else:
                average_ping = int((sum(ping_list) / len(ping_list)))

        if error:
            pass
        else:
            for ping in ping_list:
                if ping > 200:
                    extreme_ping_count += 1
                elif ping > 100:
                    large_ping_count += 1
                elif ping > 75:
                    medium_ping_count += 1
                elif ping > 25:
                    small_ping_count += 1
                elif ping > 1:
                    tiny_ping_count += 1

            lagspike_count = medium_ping_count + large_ping_count + extreme_ping_count

            self.label_file.configure(text="[" + self.selection + "] " + "Total ping count: " + str(ping_count))
            self.label_tiny_ping.configure(text="Tiny ping count: " + str(tiny_ping_count) + " (>1ms)")
            self.label_small_ping.configure(text="Small ping count: " + str(small_ping_count) + " (>25ms)")
            self.label_medium_ping.configure(text="Medium ping count: " + str(medium_ping_count) + " (>75ms)")
            self.label_large_ping.configure(text="Large ping count: " + str(large_ping_count) + " (>100ms)")
            self.label_extreme_ping.configure(text="Extreme ping count: " + str(extreme_ping_count) + " (>200ms)")
            self.label_max_ping.configure(text="MAXIMUM ping count: " + str(max(ping_list)))
            self.label_min_ping.configure(text="MINIMUM ping count: " + str(min(ping_list)))
            self.label_mean_ping.configure(text="MEAN ping count: " + str(average_ping))





