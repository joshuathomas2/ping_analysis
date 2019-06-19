from tkinter import *
import subprocess
import json
import os
import re


class PingAnalysis:
    def __init__(self):
        self.FONT = ("Times New Roman", "12")
        self.FONT_MEDIUM = ("Times New Roman", "16", "bold")
        self.FONT_LARGE = ("Times New Roman", "24", "bold")
        self.DEFAULT_BG = "SystemButtonFace"
        self.DEFAULT_FG = "black"
        self.DEFAULT_DARK_BG = "black"
        self.DEFAULT_DARK_FG = "white"
        self.DIRECTORY = "raw_data"

        self.settings_file = open("settings.json", "r")
        self.settings_json = json.load(self.settings_file)
        self.settings_file.close()

        self.theme = self.settings_json["theme"]
        self.tiny_ping = self.settings_json["tiny_ping"]
        self.small_ping = self.settings_json["small_ping"]
        self.medium_ping = self.settings_json["medium_ping"]
        self.large_ping = self.settings_json["large_ping"]
        self.extreme_ping = self.settings_json["extreme_ping"]
        self.version = self.settings_json["version"]

        self.ping_list = []
        self.ping_count = 0
        self.ping_time = 0
        self.lag_count = 0
        self.lag_percentage = 0.0
        self.mean_ping = 0
        self.tiny_ping_count = 0
        self.small_ping_count = 0
        self.medium_ping_count = 0
        self.large_ping_count = 0
        self.extreme_ping_count = 0
        self.theme_toggle = False if self.theme == "light" else True

        self.root = Tk()
        self.root.title(f"Ping Analysis {self.version}")
        self.root.geometry("750x575")
        self.root.iconbitmap("images/favicon/favicon.ico")

        self.frame_main = Frame(self.root)
        self.frame_main.pack(side=LEFT, fill=BOTH)

        self.frame_data = Frame(self.root)
        self.frame_data.pack(side=RIGHT, fill=BOTH, expand=1)

        self.listbox_data = Listbox(self.frame_main, height=25)
        self.listbox_data.pack(side=TOP)

        self.label_title = Label(self.frame_data, height=2, text="Ping Analysis", font=self.FONT_LARGE)
        self.label_title.pack(fill=X)

        self.label_error = Label(self.frame_data, fg="red", font=self.FONT_LARGE)
        self.label_error.pack()

        self.label_file = Label(self.frame_data, height=1, font=self.FONT_MEDIUM)
        self.label_file.pack()

        self.label_tiny_ping = Label(self.frame_data, font=self.FONT)
        self.label_tiny_ping.pack()

        self.label_small_ping = Label(self.frame_data, font=self.FONT)
        self.label_small_ping.pack()

        self.label_medium_ping = Label(self.frame_data, font=self.FONT)
        self.label_medium_ping.pack()

        self.label_large_ping = Label(self.frame_data, font=self.FONT)
        self.label_large_ping.pack()

        self.label_extreme_ping = Label(self.frame_data, font=self.FONT)
        self.label_extreme_ping.pack()

        self.label_max_ping = Label(self.frame_data, font=self.FONT_MEDIUM)
        self.label_max_ping.pack()

        self.label_min_ping = Label(self.frame_data, font=self.FONT_MEDIUM)
        self.label_min_ping.pack()

        self.label_mean_ping = Label(self.frame_data, font=self.FONT_MEDIUM)
        self.label_mean_ping.pack()

        self.label_lag_count = Label(self.frame_data, font=self.FONT_MEDIUM)
        self.label_lag_count.pack()

        self.label_lag_analysis = Label(self.frame_data, font=self.FONT_MEDIUM)
        self.label_lag_analysis.pack()

        '''
        self.checkbutton_auto_analyze_status = IntVar()
        self.checkbutton_auto_analyze = Checkbutton(self.frame_main,
                                                    text="Auto-Analyze", variable=self.checkbutton_auto_analyze_status)
        self.checkbutton_auto_analyze.pack(fill=BOTH, expand=1)
        '''

        self.button_analyze = Button(self.frame_main, text="Analyze")
        self.button_analyze.pack(fill=BOTH, expand=1)

        self.button_refresh = Button(self.frame_main, text="Refresh List")
        self.button_refresh.pack(fill=BOTH, expand=1)

        self.button_open_cmd = Button(self.frame_main, text="Open CMD")
        self.button_open_cmd.pack(fill=BOTH, expand=1)

        self.button_open_folder = Button(self.frame_main, text="Open Folder")
        self.button_open_folder.pack(fill=BOTH, expand=1)

        self.button_toggle_theme = Button(self.frame_main, text="Dark Theme")
        self.button_toggle_theme.pack(fill=BOTH, expand=1)

        self.folder = subprocess

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

    def clear_labels(self):
        self.label_tiny_ping.configure(text="")
        self.label_small_ping.configure(text="")
        self.label_medium_ping.configure(text="")
        self.label_large_ping.configure(text="")
        self.label_extreme_ping.configure(text="")
        self.label_max_ping.configure(text="")
        self.label_min_ping.configure(text="")
        self.label_mean_ping.configure(text="")
        self.label_file.configure(text="")
        self.label_lag_count.configure(text="")
        self.label_lag_analysis.configure(text="")

    def clear_variables(self):
        self.ping_list = []
        self.ping_count = 0
        self.ping_time = 0
        self.lag_count = 0
        self.lag_percentage = 0.0
        self.mean_ping = 0
        self.tiny_ping_count = 0
        self.small_ping_count = 0
        self.medium_ping_count = 0
        self.large_ping_count = 0
        self.extreme_ping_count = 0

    def set_theme(self):
        if self.theme_toggle:
            self.theme = "dark"
            self.theme_toggle = False
            self.button_toggle_theme.configure(text="Light Theme")
            self.frame_main.configure(bg=self.DEFAULT_DARK_BG)
            self.frame_data.configure(bg=self.DEFAULT_DARK_BG)
            self.listbox_data.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_toggle_theme.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_analyze.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_open_cmd.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_open_folder.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_refresh.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_title.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_error.configure(bg=self.DEFAULT_DARK_BG)
            self.label_tiny_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_small_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_medium_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_large_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_extreme_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_max_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_min_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_mean_ping.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_file.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_lag_count.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_lag_analysis.configure(bg=self.DEFAULT_DARK_BG)
        else:
            self.theme = "light"
            self.theme_toggle = True
            self.button_toggle_theme.configure(text="Dark Theme")
            self.frame_main.configure(bg=self.DEFAULT_BG)
            self.frame_data.configure(bg=self.DEFAULT_BG)
            self.listbox_data.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_toggle_theme.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_analyze.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_open_cmd.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_open_folder.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_refresh.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_title.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_error.configure(bg=self.DEFAULT_BG)
            self.label_tiny_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_small_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_medium_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_large_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_extreme_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_max_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_min_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_mean_ping.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_file.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_lag_count.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_lag_analysis.configure(bg=self.DEFAULT_BG)

    def get_data(self):
        data = os.listdir(self.DIRECTORY)
        return data

    def get_selection(self):

        self.selection_index = self.listbox_data.curselection()

        if self.selection_index != ():
            self.selection = self.listbox_data.get(self.selection_index)
        else:
            self.selection = None
            self.clear_labels()
            self.label_error.configure(text="ERROR: No file selected")

    def open_folder(self):
        self.folder.Popen(f"explorer {self.DIRECTORY}")

    def open_cmd(self):
        cwd = os.getcwd()

        if cwd[-8:] != self.DIRECTORY:
            os.chdir(self.DIRECTORY)
            os.system("start cmd")
        else:
            os.system("start cmd")
        os.chdir("..")

    def configure_commands(self):
        self.button_analyze.configure(command=self.analyze)
        self.button_refresh.configure(command=lambda: self.populate_listbox(self.get_data()))
        self.button_open_folder.configure(command=self.open_folder)
        self.button_toggle_theme.configure(command=self.set_theme)
        self.button_open_cmd.configure(command=self.open_cmd)
        self.root.protocol("WM_DELETE_WINDOW", self.close_and_save)

    def close_and_save(self):
        self.settings_file = open("settings.json", "w")
        self.settings_json["theme"] = self.theme
        json.dump(self.settings_json, self.settings_file, indent=4)
        self.settings_file.close()
        self.root.destroy()

    def generate_list(self):
        raw_data_file = open(self.DIRECTORY + "/" + self.selection)

        for line in raw_data_file:
            if line[0:5] == "Reply":
                try:
                    self.ping_time = int(re.split(" ", line)[4][5:][:-2])
                    self.ping_count += 1
                    self.ping_list.append(self.ping_time)
                except ValueError:
                    self.label_error.configure(text=f"ERROR: One or more lines could not be read")


        raw_data_file.close()

    def check_auto_analyze(self):
        if self.checkbutton_auto_analyze_status.get():
            self.checkbutton_auto_analyze.after(250, self.analyze())

    def analyze(self):
        self.clear_variables()
        self.clear_labels()
        self.label_error.configure(text="")

        self.get_selection()

        if self.selection is not None:
            self.generate_list()
        else:
            self.clear_labels()
            self.label_error.configure(text="ERROR: No file selected")
            return -1

        if len(self.ping_list) != 0:
            self.mean_ping = int((sum(self.ping_list) / len(self.ping_list)))
        else:
            self.clear_labels()
            self.label_error.configure(text="ERROR: No data or file is not UTF-8")
            return -1

        for ping in self.ping_list:
            if ping > self.extreme_ping:
                self.extreme_ping_count += 1
            elif ping > self.large_ping:
                self.large_ping_count += 1
            elif ping > self.medium_ping:
                self.medium_ping_count += 1
            elif ping > self.small_ping:
                self.small_ping_count += 1
            elif ping > self.tiny_ping:
                self.tiny_ping_count += 1

        self.lag_count = self.medium_ping_count + self.large_ping_count + self.extreme_ping_count
        self.lag_percentage = round(self.lag_count / self.ping_count * 100, 2)

        self.label_file.configure(text=f"[{self.selection}] Total ping count: {self.ping_count}")
        self.label_tiny_ping.configure(text=f"Tiny ping count: {self.tiny_ping_count} (>{self.tiny_ping}ms)")
        self.label_small_ping.configure(text=f"Small ping count: {self.small_ping_count} (>{self.small_ping}ms)")
        self.label_medium_ping.configure(text=f"Medium ping count: {self.medium_ping_count} (>{self.medium_ping}ms)")
        self.label_large_ping.configure(text=f"Large ping count: {self.large_ping_count} (>{self.large_ping}ms)")
        self.label_extreme_ping.configure(text=f"Extreme ping count: {self.extreme_ping_count} (>{self.extreme_ping}ms)")
        self.label_max_ping.configure(text=f"MAXIMUM ping: {max(self.ping_list)}")
        self.label_min_ping.configure(text=f"MINIMUM ping: {min(self.ping_list)}")
        self.label_mean_ping.configure(text=f"MEAN ping: {self.mean_ping}")
        self.label_lag_count.configure(text=f"Lagged {self.lag_count} {'time' if self.lag_count == 1 else 'times'} "
                                       f"out of {self.ping_count} ({self.lag_percentage}%)")

        if self.lag_percentage > 10.0:
            self.label_lag_analysis.configure(text="Extremely Severe Lag", fg="red")
        elif self.lag_percentage > 5.0:
            self.label_lag_analysis.configure(text="Severe Lag", fg="red")
        elif self.lag_percentage > 3.0:
            self.label_lag_analysis.configure(text="Moderate Lag", fg="yellow")
        elif self.lag_percentage > 1.0:
            self.label_lag_analysis.configure(text="Low Lag", fg="green")
        else:
            self.label_lag_analysis.configure(text="Extremely Low Lag", fg="cyan")

        return 0


def main():
    pa = PingAnalysis()
    pa.set_theme()
    pa.configure_commands()
    pa.populate_listbox(pa.get_data())
    pa.start_mainloop()


if __name__ == "__main__":
    main()
