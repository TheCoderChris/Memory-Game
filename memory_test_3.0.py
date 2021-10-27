from tkinter import *
import random


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Memory Game")
        self.config(bg="#1a1a1a")

        self.fr = Frame(self, bg="#1a1a1a")
        self.fr.pack()

        self.options = Frame(self, bg="#1a1a1a")
        self.back_label = Label(self.options, text="back", font=("Berlin Sans FB", 40, "underline"),
                                bg="#1a1a1a", fg="#9de0df")
        self.back_label.bind("<Button-1>", self.back)
        self.back_label.bind("<Enter>", self.on_enter_back)
        self.back_label.bind("<Leave>", self.on_leave_back)
        self.back_label.grid(row=2, column=0, columnspan=3, pady=30, padx=347)
        self.game_label = Label(self.options, text="MEMORY GAME", font=("Berlin Sans FB", 40),
                                bg="#1a1a1a", fg="#cf02a9")
        self.game_label.grid(row=0, column=0, columnspan=3, pady=50)
        self.htp_label = Label(self.options, text="How to play?", font=("Berlin Sans FB", 40, "underline"),
                               bg="#1a1a1a", fg="#9de0df")
        self.htp_label.bind("<Button-1>", self.htp)
        self.htp_label.bind("<Enter>", self.on_enter_htp)
        self.htp_label.bind("<Leave>", self.on_leave_htp)
        self.htp_label.grid(row=1, column=0, columnspan=3, pady=30)

        self.htpfr = Frame(self, bg="#1a1a1a")
        self.game_label = Label(self.htpfr, text="MEMORY GAME", font=("Berlin Sans FB", 40),
                                bg="#1a1a1a", fg="#cf02a9")
        self.game_label.grid(row=0, column=0, pady=50, padx=218)
        text = "On the beginning of each round\nyou will be shown a pattern,\nthat you have to repeat.\n" \
               "The amount of errors you are allowed\nto make are determined by\nthe button you clicked.\n" \
               "0 errors is the top left button\nand 8 is the bottom right one."
        self.htp_text = Label(self.htpfr, text=text, font=("Berlin Sans FB", 30), bg="#1a1a1a", fg="#9de0df")
        self.htp_text.grid(row=1, column=0)
        self.back_one_label = Label(self.htpfr, text="back", font=("Berlin Sans FB", 40, "underline"),
                                    bg="#1a1a1a", fg="#9de0df")
        self.back_one_label.bind("<Button-1>", self.back_one)
        self.back_one_label.bind("<Enter>", self.on_enter_back_one)
        self.back_one_label.bind("<Leave>", self.on_leave_back_one)
        self.back_one_label.grid(row=2, column=0, pady=30, padx=347)

        self.current = 0
        self.errors = 0
        self.level_errors = 0
        self.allowed = None
        self.started = False
        self.done = False

        self.buttons = list(range(9))
        for i, something in enumerate(self.buttons):
            self.buttons[i] = Button(self.fr, padx=50, pady=50, height=2, width=4,
                                     bg="#009467", activebackground="#005eff")
            self.buttons[i].bind("<Enter>", lambda event, ins=i: self.on_enter(ins))
            self.buttons[i].bind("<Leave>", lambda event, ins=i: self.on_leave(ins))
            row, column = int(i / 3) + 1, (i % 3)
            self.buttons[i].grid(row=row,
                                 column=column,
                                 padx=(200 if column == 0 else 0, 200 if column == 2 else 0),
                                 pady=0)
        self.buttons[0].configure(command=lambda: self.press(0))
        self.buttons[1].configure(command=lambda: self.press(1))
        self.buttons[2].configure(command=lambda: self.press(2))
        self.buttons[3].configure(command=lambda: self.press(3))
        self.buttons[4].configure(command=lambda: self.press(4))
        self.buttons[5].configure(command=lambda: self.press(5))
        self.buttons[6].configure(command=lambda: self.press(6))
        self.buttons[7].configure(command=lambda: self.press(7))
        self.buttons[8].configure(command=lambda: self.press(8))

        self.info = Label(self.fr, text="Click any button to start.", font=("Berlin Sans FB", 40),
                          bg="#1a1a1a", fg="#9de0df")
        self.info.grid(row=4, column=0, columnspan=3, pady=50)

        self.menubutton = Label(self.fr, text="Options", font=("Berlin Sans FB", 40, "underline"),
                                bg="#1a1a1a", fg="#9de0df")
        self.menubutton.bind("<Button-1>", self.menu)
        self.menubutton.bind("<Enter>", self.on_enter_menu)
        self.menubutton.bind("<Leave>", self.on_leave_menu)
        self.menubutton.grid(row=0, column=0, columnspan=3, pady=50)

        self.remember = list(range(1))
        for i, j in enumerate(self.remember):
            self.remember[i] = random.randint(0, 8)

    def menu(self, event):
        self.fr.pack_forget()
        self.options.pack()

    def back(self, event):
        self.options.pack_forget()
        self.fr.pack()

    def htp(self, event):
        self.options.pack_forget()
        self.htpfr.pack()

    def back_one(self, event):
        self.htpfr.pack_forget()
        self.options.pack()

    def log(self):
        self.info["text"] = "{}/{}".format(self.current, len(self.remember))
        self.info.update()

    def press(self, i):
        if not self.started:
            self.info["text"] = "How many Errors are allowed? (0-8)"
            self.info.update()
            self.started = True
        elif self.allowed is None:
            self.allowed = i
            self.info["text"] = "Click to start remembering."
            self.info.update()
        elif not self.done:
            for a in range(len(self.remember)):
                self.buttons[self.remember[a]]['background'] = '#ae00ff'
                self.buttons[self.remember[a]].update()
                self.after(500)
                self.buttons[self.remember[a]]['background'] = "#009467"
                self.buttons[self.remember[a]].update()
                self.after(50)
            self.info["text"] = "0/{}".format(len(self.remember))
            self.info.update()
            self.done = True
        else:
            try:
                if i == self.remember[self.current]:
                    self.right()
                else:
                    self.wrong()
            except IndexError:
                self.current = 0

    def right(self):
        self.current += 1
        self.log()
        if self.current >= len(self.remember):
            for f in range(9):
                self.buttons[f]['background'] = '#6fde00'
                self.buttons[f].update()
            self.after(100)
            for L in range(9):
                self.buttons[L]['background'] = '#009467'
                self.buttons[L].update()
            self.remember.append(random.randint(0, 8))
            self.done = False
            self.current = 0
            self.level_errors = 0
            self.info["text"] = "Click any button to continue with {}".format(len(self.remember))
            self.info.update()

    def wrong(self):
        self.errors += 1
        self.level_errors += 1
        if self.errors > self.allowed:
            self.failed()
        else:
            for f in range(self.errors):
                self.buttons[f]['background'] = '#fc03b6'
                self.buttons[f].update()
            self.after(100)
            for L in range(self.errors):
                self.buttons[L]['background'] = '#009467'
                self.buttons[L].update()
            self.current = 0
            self.log()

    def failed(self):
        for f in range(9):
            self.buttons[f]['background'] = '#db003e'
            self.buttons[f].update()
        self.after(500)
        for L in range(9):
            self.buttons[L]['background'] = '#009467'
            self.buttons[L].update()
        self.info["text"] = "You lose! {} correct.\nClick to play again!".format(len(self.remember) - 1)
        self.info.update()
        self.current = 0
        self.errors = 0
        self.level_errors = 0
        self.allowed = None
        self.started = False
        self.done = False
        self.remember = list(range(1))
        for i, j in enumerate(self.remember):
            self.remember[i] = random.randint(0, 8)

    def on_enter(self, i):
        self.buttons[i]['background'] = '#00944c'

    def on_leave(self, i):
        self.buttons[i]['background'] = "#009467"

    def on_enter_menu(self, event):
        self.menubutton['foreground'] = '#3c75d6'

    def on_leave_menu(self, event):
        self.menubutton['foreground'] = "#9de0df"

    def on_enter_back(self, event):
        self.back_label['foreground'] = '#3c75d6'

    def on_leave_back(self, event):
        self.back_label['foreground'] = "#9de0df"

    def on_enter_htp(self, event):
        self.htp_label['foreground'] = '#3c75d6'

    def on_leave_htp(self, event):
        self.htp_label['foreground'] = "#9de0df"

    def on_enter_back_one(self, event):
        self.back_one_label['foreground'] = '#3c75d6'

    def on_leave_back_one(self, event):
        self.back_one_label['foreground'] = "#9de0df"


if __name__ == "__main__":
    root = App()
    root.mainloop()
