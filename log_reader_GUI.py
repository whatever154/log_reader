from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import os
import re

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

        self.fr_search_bar = Frame(self.fr_control)
        self.entry_key_word = Entry(self.fr_search_bar,  width=30)
        self.entry_key_word.grid(row=0, column=0, sticky=EW, padx=(0, 2))
        self.btn_search = Button(self.fr_search_bar, text=">", height=1, command=self.__search)
        self.btn_search.grid(row=0, column=1)
        self.fr_search_bar.pack(padx=5, pady=(5, 0), anchor=NW, fill=X)


        self.check_register = IntVar()
        self.check_regular = IntVar()
        Checkbutton(self.fr_control, text="Не учитывать регистр", variable=self.check_register).pack(padx=(5, 0), pady=(5, 0), anchor=NW)
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

        self.notebook = ttk.Notebook(self, width=300)
        self.notebook.pack(anchor=W, side=LEFT, fill=BOTH, expand=True)
        self.fr_text = Frame()

        self.textw = ScrolledText(self.fr_text)
        self.textw.pack(anchor=W, side=LEFT, fill=BOTH, expand=True)
        self.textw.tag_configure("highlight", background="yellow")
        self.textw.tag_configure("curhighlight",  background="orange")
        self.textw.bind("<ButtonRelease-1>", self.__get_position)
        self.notebook.add(self.fr_text, text="Просмотр файла", sticky=NSEW)

        self.fr_findings = Frame()

        self.text_findings = ScrolledText(self.fr_findings, state="disabled")
        self.text_findings.pack(anchor=W, side=LEFT, fill=BOTH, expand=True)
        self.text_findings.tag_configure("highlight", background="yellow")
        self.text_findings.tag_configure("curhighlight",  background="orange")

        self.notebook.add(self.fr_findings, text="Результаты поиска", sticky=NSEW)
    
    def __get_log_path(self):
        self.log_path = filedialog.askopenfilename(initialdir="/", filetypes=(("", "*.log"), ))
        self.lbl_log_path.config(text=f"Лог-файл: {os.path.basename(self.log_path)}")
        with open(self.log_path, "r+b") as log_f:
            self.log = log_f.read()
        self.textw.delete('1.0', END)
        self.textw.insert('1.0', self.log)
    
    def __add_DEBUG(self):
        if self.check_DEBUG.get():
            self.__included_levels.append("DEBUG")
        else:
            self.__included_levels.remove("DEBUG")
    
    def __add_INFO(self):
        if self.check_INFO.get():
            self.__included_levels.append("INFO")
        else:
            self.__included_levels.remove("INFO")
    
    def __add_WARN(self):
        if self.check_WARN.get():
            self.__included_levels.append("WARN")
        else:
            self.__included_levels.remove("WARN")
    
    def __add_ERROR(self):
        if self.check_ERROR.get():
            self.__included_levels.append("ERROR")
        else:
            self.__included_levels.remove("ERROR")
    
    def __get_position(self, event):
        print(self.textw.index("insert"))
    
    def __find_logs(self, log, levels=["DEBUG", "INFO", "WARN", "ERROR"]):
        new_log = []
        for i in log:
            j = 0
            while j < len(levels):
                if levels[j] in i[1]:
                    new_log.append(i)
                    j = len(levels)
                j += 1
        return new_log
    
    def __search(self):
        self.text_findings.config(state="normal")
        self.text_findings.delete("1.0", END)
        self.text_findings.config(state="disabled")
        text = [x + "\n" for x in self.textw.get("1.0", END).split("\n")]
        log = [[1, text[0]]]
        self.positions = []
        i = 1
        while i < len(text):
            if text[i].startswith('~['):
                log.append([i + 1, text[i]])
            else:
                log[-1][1] += text[i]
            i += 1
        if self.__included_levels:
            log = self.__find_logs(log, self.__included_levels)
        else:
            log = self.__find_logs(log)
        current_pos = 0
        k = 1
        if self.check_regular.get():
            self.key_words = self.entry_key_word.get()
        else:
            self.key_words = self.entry_key_word.get().split()
        if self.check_regular.get():
            for i in log:
                if self.check_register.get():
                    match = re.search(self.key_words.lower(), i[1].lower())
                else:
                    match = re.search(self.key_words, i[1])
                if match:
                    self.positions.append((i[0], k))
                    self.text_findings.config(state="normal")
                    self.text_findings.insert(END, i[1])
                    self.text_findings.config(state="disabled")
                    k += 1
        else:
            if self.check_register.get():
                for i in log:
                    j = 0
                    while j < len(self.key_words):
                        if self.key_words[j].lower() in i[1].lower():
                            self.positions.append((i[0], k))
                            self.text_findings.config(state="normal")
                            self.text_findings.insert(END, i[1])
                            self.text_findings.config(state="disabled")
                            k += 1
                            j = len(self.key_words)
                        j += 1
            else:
                for i in log:
                    j = 0
                    while j < len(self.key_words):
                        if self.key_words[j] in i[1]:
                            self.positions.append((i[0], k))
                            self.text_findings.config(state="normal")
                            self.text_findings.insert(END, i[1])
                            self.text_findings.config(state="disabled")
                            k += 1
                            j = len(self.key_words)
                        j += 1
                    

        


if __name__ == "__main__":
    window = Log_reader()
    window.mainloop()
