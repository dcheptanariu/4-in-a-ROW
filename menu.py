import game
import tkinter as tk
from tkinter import ttk

# Creating tkinter window

print(int('4'))
root = tk.Tk()
root.title('4 in a ROW')
root.geometry('800x600')
root['bg'] = '#00ccff'
title_label = ttk.Label(root, text="4 in a ROW", foreground="white", background='#00ccff', font=("Comic Sans MS", 30))
title_label.place(x=300, y=0)

difficulty_label = ttk.Label(root, text="Dificulty:", foreground="white", background='#00ccff',
                             font=("Comic Sans MS", 15))
difficulty_label.place(x=300, y=240)
nr_row_label = ttk.Label(root, text="Number rows:", foreground="white", background="#00ccff",
                         font=("Comic Sans MS", 15))
nr_row_label.place(x=300, y=150)

nr_col_label = ttk.Label(root, text="Number columns:", foreground="white", background='#00ccff',
                         font=("Comic Sans MS", 15))
nr_col_label.place(x=300, y=180)
opponent_label = ttk.Label(root, text="Opponent:", foreground="white", background='#00ccff', font=("Comic Sans MS", 15))
opponent_label.place(x=300, y=210)
start_label = ttk.Label(root, text="Who start:", foreground="white", background='#00ccff', font=("Comic Sans MS", 15))
start_label.place(x=300, y=270)

difficulty_combo = ttk.Combobox(root, width=10, font=("Comic Sans MS", 10))

difficulty_combo['values'] = ('Easy', 'Medium', 'Hard')
difficulty_combo.set('Easy')
difficulty_combo.place(x=460, y=248)
difficulty_combo.state(['readonly'])

opp_combo = ttk.Combobox(root, width=10, font=("Comic Sans MS", 10))

opp_combo['values'] = ('AI', 'Human')
opp_combo.set('AI')
opp_combo.place(x=460, y=218)
opp_combo.state(['readonly'])
start_combo = ttk.Combobox(root, width=10, font=("Comic Sans MS", 10))
start_combo['values'] = ('AI', 'Human')
start_combo.set('AI')
start_combo.place(x=460, y=278)
start_combo.state(['readonly'])

nr_rows_spinbox = tk.Spinbox(root, from_=4, to=10, width=5, font=("Comic Sans MS", 10), highlightbackground="white")
nr_rows_spinbox.place(x=460, y=158)
nr_cols_spinbox = tk.Spinbox(root, from_=4, to=10, width=5, font=("Comic Sans MS", 10), highlightbackground="white")
nr_cols_spinbox.place(x=460, y=188)


def start_pressed():
    rows = nr_rows_spinbox.get()
    cols = nr_cols_spinbox.get()
    opp = opp_combo.get()
    game.game_initialize(rows=rows, columns=cols, opponent_type=opp, dificulty=None, start=None)


def selected_opp(event):
    if opp_combo.get() == 'Human':
        difficulty_combo.place_forget()
        start_combo.place_forget()
        start_label.place_forget()
        difficulty_label.place_forget()
    else:
        difficulty_combo.place(x=460, y=248)
        start_combo.place(x=460, y=278)
        start_label.place(x=300, y=270)
        difficulty_label.place(x=300, y=240)


start_button = tk.Button(root, text="Start", font=("Comic Sans MS", 20), command=start_pressed)
start_button.place(x=390, y=320)

opp_combo.bind('<<ComboboxSelected>>', selected_opp)

root.mainloop()
