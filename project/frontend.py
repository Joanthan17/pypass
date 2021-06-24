import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from ttkthemes import ThemedTk


# from car import car

class ScaleLabelCombo(ttk.Frame):
    def __init__(self, parent, scale_from=1, scale_to=200, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack_propagate(False)

        self.scale_len = scale_to - scale_from
        self.scale_from = scale_from

        # create label widget
        self.label = tk.Label(self, text=str(scale_from))
        self.label.place(anchor=tk.NW, y=5)

        # create a scale widget
        self.scale_var = tk.IntVar()
        self.scale = ttk.Scale(self, from_=scale_from, to=scale_to, orient=tk.HORIZONTAL,
                               variable=self.scale_var, length=100, command=self.labelupdate)
        self.scale.place(anchor=tk.NW, y=25)

    def labelupdate(self, ok=None):
        # move the label proportionally to the scale var position
        pos_atm = self.scale_var.get()
        self.label.config(text=pos_atm)
        self.label.place(anchor=tk.NW, y=5, x=((pos_atm - self.scale_from) / self.scale_len) * 90)


class TextScrollCombo(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set


class MainApplication(ThemedTk):
    def __init__(self):
        super().__init__()  # init for tk.TK
        self.title("Passpy - dictionary passwords generator")
        self.geometry("500x300")

        # ensure a consistent GUI size
        self.pack_propagate(False)

        """  -------------------------------- tabs init --------------------------------  """
        self.notebook = ttk.Notebook(self, takefocus=False)  # stores the tabs
        self.fields_frame = ttk.Frame(self.notebook, takefocus=False)
        self.loader_frame = ttk.Frame(self.notebook, takefocus=False)
        help_frame = ttk.Frame(self.notebook, takefocus=False)
        self.notebook.add(self.fields_frame, text="fields")
        self.notebook.add(self.loader_frame, text="loader")
        self.notebook.add(help_frame, text="Help")
        self.notebook.pack(fill=tk.BOTH)
        """  ----------------------------------------------------------------------------  """

        """_________________________________________ fields tab init ______________________________________"""

        """  ------------------------------- Entries init -------------------------------  """
        self.entries = []
        fields = "1st word", "2nd word", "3rd word", "4th word", "min password length", "max password length"

        for field in fields:
            row = ttk.Frame(self.fields_frame)
            lab_place_saver = tk.Label(row, width=3, anchor='w')
            lab_place_saver.pack(side=tk.LEFT)
            if (field == fields[4]) or (field == fields[5]):
                lab = tk.Label(row, width=len(max(fields[4:6])) - 1, text=field, anchor='w')
                ent = tk.Entry(row, width=5)
            else:
                lab = tk.Label(row, width=len(max(fields[0:4])), text=field, anchor='w')
                ent = tk.Entry(row, width=15)
            row.pack(fill=tk.X)
            lab.pack(side=tk.LEFT)  # maybe all need to be self.
            ent.pack(side=tk.LEFT, padx=3, pady=2, fill=tk.X)
            self.entries.append((field, ent))
        self.entries[3][1].config(state='disable')
        self.entries[2][1].config(state='disable')
        """  ----------------------------------------------------------------------------  """

        """  --------------------------------- Scale init -------------------------------  """
        self.scalecombo = ScaleLabelCombo(self.fields_frame, 1, 15)
        # self.scalecombo.pack(pady=5)
        self.scalecombo.place(anchor=tk.NW, y=165, x=190)
        self.scalecombo.config(width=120, height=40)
        """  ----------------------------------------------------------------------------  """

        """  ------------------------------- buttons init -------------------------------  """
        self.start_button = tk.Button(self.fields_frame, text="Generate!", command=self.getuserinput)
        self.quit_button = tk.Button(self.fields_frame, text="Quit", command=self.goodbye)

        self.start_button.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.quit_button.place(rely=0.0, relx=1.0, x=0, y=0, anchor=tk.NE)
        """  ----------------------------------------------------------------------------  """

        """  ------------------------------- Combobox init ------------------------------  """
        self.filesize_combo = ttk.Combobox(self.fields_frame,
                                           values=[
                                               "Minimalistic",
                                               "Small",
                                               "Big",
                                               "Huge"], font=("Times Roman", 10))
        self.filesize_combo.place(anchor=tk.NW, y=37, x=380, width=110)
        self.filesize_combo.set("Small")
        """  ----------------------------------------------------------------------------  """

        """  ---------------------------- CheckButtons init ----------------------------  """
        self.checkboxes_widgets = {}
        checkboxes_strings = "4th word", "Base64 Encoded", "Go Faster", "3rd word", "MD5", "SHA-1", "SHA-256"
        self.initflag = 0
        self.initflag4scale = 0

        for box_name in checkboxes_strings:
            if box_name == "3rd word":
                self.checkboxes_widgets[box_name] = ttk.Checkbutton(self.fields_frame, text=box_name,
                                                                    command=self.turnonfour, takefocus=False)
            elif box_name == "Go Faster":
                self.checkboxes_widgets[box_name] = ttk.Checkbutton(self.fields_frame, text=box_name, command=self.movescale,
                                                                    takefocus=False)
            else:
                self.checkboxes_widgets[box_name] = ttk.Checkbutton(self.fields_frame, text=box_name, takefocus=False)
            self.checkboxes_widgets[box_name].invoke()
            self.checkboxes_widgets[box_name].invoke()

        self.checkboxes_widgets["3rd word"].place(anchor=tk.NW, y=57, x=12)
        self.checkboxes_widgets["4th word"].place(anchor=tk.NW, y=81, x=12)
        self.checkboxes_widgets["4th word"].state(['disabled', ''])
        self.checkboxes_widgets["Base64 Encoded"].place(anchor=tk.NW, y=139, x=240)
        self.checkboxes_widgets["Go Faster"].place(anchor=tk.NW, y=190, x=313)
        self.checkboxes_widgets["MD5"].place(anchor=tk.NW, y=75, x=300)
        self.checkboxes_widgets["SHA-1"].place(anchor=tk.NW, y=95, x=300)
        self.checkboxes_widgets["SHA-256"].place(anchor=tk.NW, y=115, x=300)
        """  ----------------------------------------------------------------------------  """

        """  ------------------------------- Labels init --------------------------------  """
        self.filesize_label = tk.Label(self.fields_frame, text="Passwords File Size:")
        self.hashes_label = tk.Label(self.fields_frame, text="Hashes:")
        self.tnum_label = tk.Label(self.fields_frame, text="Number of Threads")
        self.passnum_label = tk.Label(self.fields_frame, text="Estimated passwords to generate:")
        self.passnum_label.config(font=("Times Roman", 9))
        self.filesize_label.place(anchor=tk.NW, y=37, x=240)
        self.hashes_label.place(anchor=tk.NW, y=62, x=240)
        self.tnum_label.place(anchor=tk.NW, y=190, x=50)
        self.passnum_label.place(anchor=tk.NW, y=210, x=80)
        """  ----------------------------------------------------------------------------  """

        """______________________________________________________________________________________________"""

        """  ------------------------------- loader init --------------------------------  """
        self.loader_label = tk.Label(self.loader_frame, fg="black", text="Loading...")
        self.loader_label.pack(side=tk.TOP, fill="x")
        self.progress_bar = ttk.Progressbar(self.loader_frame, orient=tk.HORIZONTAL, length=450, mode="determinate")
        self.progress_bar.pack(side=tk.TOP, fill="x")

        self.loader_pass_generated_label = tk.Label(self.loader_frame, fg="black", text="Loading...")
        self.loader_pass_generated_label.pack(fill="x", pady=5)
        self.loader_update_pass_label(10, 100)

        self.loader_stop_button = tk.Button(self.loader_frame, text="Stop", command=self.loader_barflow)
        self.loader_stop_button.place(anchor=tk.N, x=40, y=45)

        self.txtnscroll = TextScrollCombo(self.loader_frame)
        self.txtnscroll.pack(fill="both", pady=10, expand=True)
        self.txtnscroll.config(width=460, height=1000)
        self.txtnscroll.txt.config(font=("consolas", 9), undo=True, wrap='word')
        self.txtnscroll.txt.config(borderwidth=3, relief="sunken")
        quote = """HAMLET: To be, or not to be--that is the question:
        Whether 'tis nobler in the mind to suffer
        The slings and arrows of outrageous fortune
        Or to take arms against a sea of troubles
        And by opposing end them. To die, to sleep--
        No more--and by a sleep to say we end
        The heartache, and the thousand natural shocks
        That flesh is heir to. 'Tis a consummation
        Devoutly to be wished."""
        self.txtnscroll.txt.insert(tk.END, quote)
        self.txtnscroll.txt.config(state='disabled')
        """  ----------------------------------------------------------------------------  """

        """  -------------------------------- help init ---------------------------------  """
        self.help_label = tk.Label(help_frame, fg="black",
                                   text="This is the help menu:\n"
                                        "here you will be able to find explanation for everything.")
        self.help_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        """  ----------------------------------------------------------------------------  """

    def loader_stop(self):
        # stops everything
        pass

    def loader_barflow(self, value=20):
        self.progress_bar['value'] += value

    def loader_update_pass_label(self, pass_generated, pass_total):
        self.loader_pass_generated_label.config(
            text="Generated " + str(pass_generated) + " /" + str(pass_total) + " potential passwords")

    def loader_textbox(self, text):
        self.txtnscroll.txt.config(state='normal')
        self.txtnscroll.txt.insert(tk.END, text + "\n")
        self.txtnscroll.txt.config(state='disabled')

    def goodbye(self):
        if msg.askokcancel("Goodbye?", "Are you sure you want to close Passpy?"):
            self.notebook.quit()

    def help(self):
        print(self.winfo_width())

    def movescale(self):
        if self.initflag >= 2:
            if self.initflag4scale % 2 == 0:
                self.scalecombo.scale_var.set(10)
                self.scalecombo.labelupdate()
        self.initflag4scale += 1
        # pass

    # def labelupdate(self, ok=None):
    #    pos_atm = self.scale_var.get()
    #    #print (type(pos_atm))
    #    self.scale_lable.config(text=pos_atm)
    #    self.scale_lable.place(anchor=tk.NW, y=170, x=198+pos_atm/3)

    def turnonfour(self):
        if self.initflag >= 2:
            if self.initflag % 2 == 0:
                self.entries[3][1].config(state='normal')
                self.entries[2][1].config(state='normal')
                self.checkboxes_widgets["4th word"].state(['!disabled', ''])
            else:
                self.entries[3][1].config(state='disabled')
                self.entries[2][1].config(state='disable')
                self.checkboxes_widgets["4th word"].state(['disabled', ''])
        self.initflag += 1

    def disablechildren(self, parent):
        """ disables every child of a given parent (recursively)"""
        for child in parent.winfo_children():
            wtype = child.winfo_class()
            #print (wtype)
            if wtype not in ('TFrame','Frame', 'Labelframe', 'TScale'):
                child.configure(state='disable')
            else:
                self.disablechildren(child)

    def getuserinput(self, text=None):
        """ saves all user data for backend and disabling the first tab"""
        selected_checkboxes = []
        selected_words = []
        if not text:
            for entry in self.entries:
                field = entry[0]
                text = entry[1].get()
                if text not in selected_words:
                    selected_words.append(text) # remove repeated words
                print('%s: "%s"' % (field, text))
            for box in self.checkboxes_widgets:
                if "selected" in self.checkboxes_widgets[box].state():
                    selected_checkboxes.append(box)
            print(selected_checkboxes)
            print(self.filesize_combo.current())
            print(self.scalecombo.scale_var.get())

            # disable everything in the first tab (fields frame) and move to the second tab
            self.disablechildren(self.fields_frame)
            self.notebook.select(self.loader_frame)
            #start_all(selected_words, selected_checkboxes, self.filesize_combo.current(), self.scalecombo.scale_var.get())


if __name__ == "__main__":
    # execute only if run as a script
    window = MainApplication()
    window.set_theme("elegance")
    # window.minsize(width=40, height=50)
    # window.maxsize(width=500, height=300)

    window.mainloop()
