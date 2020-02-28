import tkinter as tk
import subprocess
import json
import os
import re


class PingAnalysis:
    def __init__(self):
        self.settings_file = open("settings.json", "r")
        self.settings_json = json.load(self.settings_file)
        self.settings_file.close()

        self.FONT = ("Times New Roman", "16", "bold")
        self.FONT_MEDIUM = ("Times New Roman", "20", "bold")
        self.FONT_LARGE = ("Times New Roman", "24", "bold")
        self.DEFAULT_BG = self.settings_json["DEFAULT_BG"]
        self.DEFAULT_FG = self.settings_json["DEFAULT_FG"]
        self.DEFAULT_DARK_BG = self.settings_json["DEFAULT_DARK_BG"]
        self.DEFAULT_DARK_FG = self.settings_json["DEFAULT_DARK_FG"]
        self.DIRECTORY = self.settings_json["DIRECTORY"]

        self.theme = self.settings_json["theme"]
        self.theme_toggle = False if self.theme == "light" else True
        self.tiny_ping = self.settings_json["tiny_ping"]
        self.small_ping = self.settings_json["small_ping"]
        self.medium_ping = self.settings_json["medium_ping"]
        self.large_ping = self.settings_json["large_ping"]
        self.extreme_ping = self.settings_json["extreme_ping"]
        self.version = self.settings_json["version"]
        self.selection_index = None
        self.selection = None

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

        self.root = tk.Tk()
        self.root.title(f"Ping Analysis {self.version}")
        self.root.geometry("750x575")
        self.root.iconbitmap("images/favicon/favicon.ico")
        self.root.bind("<Return>", self.user_keypress)

        self.frame_data = tk.Frame(self.root)
        self.frame_data.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(fill=tk.BOTH, expand=1)

        self.listbox_data = tk.Listbox(self.frame_data, height=25)
        self.listbox_data.pack(side=tk.TOP)

        self.label_header = tk.Label(self.frame_main, font=self.FONT_LARGE, text="Ping Analysis")
        self.label_header.pack(pady=(10, 25))

        self.label_file = tk.Label(self.frame_main, font=self.FONT_LARGE, anchor="w")
        self.label_file.pack(fill=tk.X, pady=(0, 25), padx=(10, 0))

        self.label_lag_analysis = tk.Label(self.frame_main, font=self.FONT_MEDIUM, anchor="w")
        self.label_lag_analysis.pack(fill=tk.X, padx=(10, 0))

        self.label_max_ping = tk.Label(self.frame_main, font=self.FONT_MEDIUM, anchor="w")
        self.label_max_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_min_ping = tk.Label(self.frame_main, font=self.FONT_MEDIUM, anchor="w")
        self.label_min_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_mean_ping = tk.Label(self.frame_main, font=self.FONT_MEDIUM, anchor="w")
        self.label_mean_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_lag_count = tk.Label(self.frame_main, font=self.FONT_MEDIUM, anchor="w")
        self.label_lag_count.pack(fill=tk.X, pady=(0, 25), padx=(10, 0))

        self.label_tiny_ping = tk.Label(self.frame_main, font=self.FONT, anchor="w")
        self.label_tiny_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_small_ping = tk.Label(self.frame_main, font=self.FONT, anchor="w")
        self.label_small_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_medium_ping = tk.Label(self.frame_main, font=self.FONT, anchor="w")
        self.label_medium_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_large_ping = tk.Label(self.frame_main, font=self.FONT, anchor="w")
        self.label_large_ping.pack(fill=tk.X, padx=(10, 0))

        self.label_extreme_ping = tk.Label(self.frame_main, font=self.FONT, anchor="w")
        self.label_extreme_ping.pack(fill=tk.X, padx=(10, 0))

        self.button_analyze = tk.Button(self.frame_data, text="Analyze")
        self.button_analyze.pack(fill=tk.BOTH, expand=1)

        self.button_refresh = tk.Button(self.frame_data, text="Refresh List")
        self.button_refresh.pack(fill=tk.BOTH, expand=1)

        self.button_open_cmd = tk.Button(self.frame_data, text="Open CMD")
        self.button_open_cmd.pack(fill=tk.BOTH, expand=1)

        self.button_open_folder = tk.Button(self.frame_data, text="Open Folder")
        self.button_open_folder.pack(fill=tk.BOTH, expand=1)

        self.button_toggle_theme = tk.Button(self.frame_data, text="Dark Theme")
        self.button_toggle_theme.pack(fill=tk.BOTH, expand=1)

    def start_mainloop(self):
        self.root.mainloop()

    def populate_listbox(self, files):
        self.clear_listbox()
        for file in files:
            self.listbox_data.insert("end", file)

    def clear_listbox(self):
        self.listbox_data.delete(0, tk.END)

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
            self.frame_data.configure(bg=self.DEFAULT_DARK_BG)
            self.frame_main.configure(bg=self.DEFAULT_DARK_BG)
            self.listbox_data.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_toggle_theme.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_analyze.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_open_cmd.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_open_folder.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.button_refresh.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
            self.label_header.configure(fg=self.DEFAULT_DARK_FG, bg=self.DEFAULT_DARK_BG)
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
            self.frame_data.configure(bg=self.DEFAULT_BG)
            self.frame_main.configure(bg=self.DEFAULT_BG)
            self.listbox_data.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_toggle_theme.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_analyze.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_open_cmd.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_open_folder.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.button_refresh.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
            self.label_header.configure(fg=self.DEFAULT_FG, bg=self.DEFAULT_BG)
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
        files = os.listdir(self.DIRECTORY)
        return files

    def get_selection(self):
        self.selection_index = self.listbox_data.curselection()

        if self.selection_index != ():
            self.selection = self.listbox_data.get(self.selection_index)
        else:
            self.selection = None
            self.clear_labels()
            self.label_header.configure(text="ERROR: No file selected")

    def open_folder(self):
        subprocess.run(f"explorer {self.DIRECTORY}")

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
                    self.label_header.configure(text="ERROR: One or more lines could not be read")

        raw_data_file.close()

    def user_keypress(self, event):
        self.analyze()

    def analyze(self):
        self.clear_variables()
        self.clear_labels()
        self.label_header.configure(text="Ping Analysis")

        self.get_selection()

        if self.selection is not None:
            self.generate_list()
        else:
            self.clear_labels()
            self.label_header.configure(text="ERROR: No file selected")
            return -1

        if len(self.ping_list) != 0:
            self.mean_ping = int((sum(self.ping_list) / len(self.ping_list)))
        else:
            self.clear_labels()
            self.label_header.configure(text="ERROR: No data or file is not UTF-8")
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
