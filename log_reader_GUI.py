from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import os

class Log_reader(Tk):

    levels = ["DEBUG", "INFO", "WARN", "ERROR"]

    def __init__(self):
        super().__init__()
        self.geometry("800x750")
        self.title("Log reader")

        self.fr_control = Frame(self)

        self.log_path = ""
        self.btn_get_log_path = Button(self.fr_control, text="Выбрать лог-файл", command=self.__get_log_path)
        self.btn_get_log_path.pack(padx=(5, 80), pady=(5, 0), anchor=NW)

        self.lbl_log_path = Label(self.fr_control, text="Лог-файл: ")
        self.lbl_log_path.pack(padx=(5, 0), pady=(5, 0), anchor=NW)
        
        Label(self.fr_control, text="Поиск строки в файле:").pack(padx=(5, 0), pady=(5, 0), anchor=NW)
        self.entry_key_word = Entry(self.fr_control)
        self.entry_key_word.pack(padx=5, pady=(5, 0), anchor=NW, fill=X)
        self.check_register = IntVar()
        self.check_regular = IntVar()
        Checkbutton(self.fr_control, text="Учитывать регистр", variable=self.check_register).pack(padx=(5, 0), pady=(5, 0), anchor=NW)
        Checkbutton(self.fr_control, text="Регулярное выражение", variable=self.check_regular).pack(padx=(5, 0), pady=(5, 0), anchor=NW)

        Label(self.fr_control, text="Искать уровни логирования:").pack(padx=(5, 0), pady=(5, 0), anchor=NW)
        self.__included_levels = []
        self.check_DEBUG = IntVar()
        self.check_INFO = IntVar()
        self.check_WARN = IntVar()
        self.check_ERROR = IntVar()
        Checkbutton(self.fr_control, text="DEBUG", variable=self.check_DEBUG, command=self.__add_DEBUG).pack(padx=(5, 0), pady=(2, 0), anchor=NW)
        Checkbutton(self.fr_control, text="INFO", variable=self.check_INFO, command=self.__add_INFO).pack(padx=(5, 0), pady=(2, 0), anchor=NW)
        Checkbutton(self.fr_control, text="WARNING", variable=self.check_WARN, command=self.__add_WARN).pack(padx=(5, 0), pady=(2, 0), anchor=NW)
        Checkbutton(self.fr_control, text="ERROR", variable=self.check_ERROR, command=self.__add_ERROR).pack(padx=(5, 0), pady=(2, 0), anchor=NW)

        self.fr_control.pack(anchor=W, side=LEFT, fill=Y)

        self.textw = ScrolledText()
        self.textw.pack(anchor=W, side=LEFT, fill=BOTH, expand=True)
    
    def __get_log_path(self):
        self.log_path = filedialog.askopenfilename(initialdir="/", filetypes=(("", "*.log"), ))
        self.lbl_log_path.config(text=f"Лог-файл: {os.path.basename(self.log_path)}")
        with open(self.log_path, "r+b") as log_f:
            self.log = log_f.read()
        self.textw.insert('1.0', self.log)
    
    def __add_DEBUG(self):
        if self.check_DEBUG.get():
            self.__included_levels.append(b"DEBUG")
        else:
            self.__included_levels.remove(b"DEBUG")
    
    def __add_INFO(self):
        if self.check_INFO.get():
            self.__included_levels.append(b"INFO")
        else:
            self.__included_levels.remove(b"INFO")
    
    def __add_WARN(self):
        if self.check_WARN.get():
            self.__included_levels.append(b"WARN")
        else:
            self.__included_levels.remove(b"WARN")
    
    def __add_ERROR(self):
        if self.check_ERROR.get():
            self.__included_levels.append(b"ERROR")
        else:
            self.__included_levels.remove(b"ERROR")
        


if __name__ == "__main__":
    window = Log_reader()
    window.mainloop()