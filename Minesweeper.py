from tkinter import *
from random import choice
import time
import tkinter.messagebox

frm = []
btn = []
xBtn = 5
yBtn = 5
playTime = None
mines = xBtn * yBtn // 6.4
imgMark = '★'
imgMine = '🚩'
playArea = []
nMoves = 0
mrk = 0
play_time = 0
timer_id = None

tk = Tk()
tk.title('САПЕР')
tk.geometry('800x700')

difficulty_times = {'easy': 180, 'medium': 300, 'hard': 420}

def play(n):
    global xBtn, yBtn, mines, nMoves, mrk, playTime

    if playTime is None:
        playTime = time.time()

    nMoves += 1

    if len(playArea) < xBtn * yBtn:
        return()

    if nMoves == 1:
        i = 0
        while i < mines:
            j = choice(range(0, xBtn * yBtn))
            if j != n and playArea[j] != -1:
                playArea[j] = -1
                i += 1

        for i in range(0, xBtn * yBtn):
            if playArea[i] != -1:
                k = 0
                if i not in range(0, xBtn * yBtn, xBtn):
                    if playArea[i - 1] == -1: k += 1
                    if i > xBtn - 1:
                        if playArea[i - xBtn - 1] == -1: k += 1
                    if i < xBtn * yBtn - xBtn:
                        if playArea[i + xBtn - 1] == -1: k += 1
                if i not in range(-1, xBtn * yBtn, xBtn):
                    if playArea[i + 1] == -1: k += 1
                    if i > xBtn - 1:
                        if playArea[i - xBtn + 1] == -1: k += 1
                    if i < xBtn * yBtn - xBtn:
                        if playArea[i + xBtn + 1] == -1: k += 1
                if i > xBtn - 1:
                    if playArea[i - xBtn] == -1: k += 1
                if i < xBtn * yBtn - xBtn:
                    if playArea[i + xBtn] == -1: k += 1
                playArea[i] = k
                update_time()

    if btn[n].cget('text') == imgMark:
        mrk -= 1
        tk.title('Кількість мін : ' + str(mines - mrk))
    btn[n].config(text=playArea[n], state=DISABLED, bg='white')

    if playArea[n] == 0:
        btn[n].config(text=' ', bg='#cdd')
    elif playArea[n] == -1:
        btn[n].config(text=imgMine)
        if nMoves <= (xBtn * yBtn - mines) or mines >= mrk:
            nMoves = 32000
            chainReaction(0)
            tk.title('Ви програли')
            tkinter.messagebox.showinfo("Ви програли", "Ви програли")

    if nMoves == (xBtn * yBtn - mines) and mines == mrk:
        elapsed_time = int(time.time() - playTime)
        tk.title('Перемога! Час: {} сек, Міни: {}'.format(elapsed_time, mines))
        tkinter.messagebox.showinfo("Вітаємо!", "Ви перемогли!")
        winner(0)

def chainReaction(j):
    if j <= len(playArea):
        for i in range(j, xBtn * yBtn):
            if playArea[i] == -1 and btn[i].cget('text') == ' ':
                btn[i].config(text=imgMine)
                btn[i].flash()
                tk.bell()
                tk.after(50, chainReaction, i + 1)
                break

def winner(j):
    if j == len(playArea):
        tkinter.messagebox.showinfo("Вітаємо!", "Ви перемогли!")

def marker(n):
    global mrk, mines, playTime

    if (btn[n].cget('state')) != 'disabled':
        if btn[n].cget('text') == imgMark:
            btn[n].config(text=' ')
            mrk -= 1
        else:
            btn[n].config(text=imgMark, fg='black')
            mrk += 1
            update_mines_label()
        tk.title('Кількість мін : ' + str(mines - mrk))
    if nMoves == (xBtn * yBtn - mines) and mines == mrk:
        tk.title('Перемога! ' + str(int(time.time() - playTime)) + ' сек')
        tkinter.messagebox.showinfo("Вітаємо!", "Ви перемогли!")
        winner(0)

def newGame(difficulty='easy'):
    global xBtn, yBtn, mines, nMoves, mrk, playTime, play_time, timer_id

    if timer_id:
        tk.after_cancel(timer_id)

    if difficulty == 'easy':
        xBtn = 5
        yBtn = 5
    elif difficulty == 'medium':
        xBtn = 8
        yBtn = 8
    elif difficulty == 'hard':
        xBtn = 14
        yBtn = 10

    mines = xBtn * yBtn * 10 // 64
    nMoves = 0
    mrk = 0
    playTime = time.time()
    playArea.clear()
    if len(btn) != 0:
        for i in range(0, len(btn)):
            btn[i].destroy()
        btn.clear()
        for i in range(0, len(frm)):
            frm[i].destroy()
        frm.clear()

    playground()
    update_mines_label()

    if difficulty in difficulty_times:
        play_time = difficulty_times[difficulty]
        time_label.config(text='Час: {} сек'.format(play_time))
    else:
        time_label.config(text='Час: 0 сек')

    tk.title('Кількість мін : ' + str(mines))
    update_time()

def set5x5():
    newGame('easy')

def set8x8():
    newGame('medium')

def set10x14():
    newGame('hard')

def rules():
    rules_text = 'Ваше завдання – відкрити всі осередки, крім тих, де знаходяться міни. Ви можете відкрити комірку, клацнувши по ній лівою кнопкою миші. Якщо в комірці немає міни, то відкриється число, яке показує, скільки мін знаходиться поряд із цією коміркою. Якщо ви вважаєте, що у певному осередку знаходиться міна, ви можете позначити її прапорцем, натиснувши правою кнопкою миші. Якщо ви відкриєте комірку з міною, гра завершиться, і ви програєте. Якщо ви відкриєте всі комірки без мін та помітите всі міни, гра завершиться, і ви переможете.'
    tkinter.messagebox.showinfo("Правила гри", rules_text)

def playground():
    global xBtn, yBtn

    for i in range(0, yBtn):
        frm.append(Frame())
        frm[i].pack(expand=YES, fill=BOTH)

        for j in range(0, xBtn):
            btn.append(Button(frm[i], text=' ', font=('mono', 20, 'bold'),
                              width=1, height=1, padx=0, pady=0, bg='green'))

    for i in range(0, xBtn * yBtn):
        if xBtn * yBtn > 256:
            btn[i].config(font=('mono', 8, 'normal'))
        btn[i].config(command=lambda n=i: play(n))
        btn[i].bind('<Button-3>', lambda event, n=i: marker(n))
        btn[i].pack(side=LEFT, expand=YES, fill=BOTH, padx=0, pady=0)
        btn[i].update()
        playArea.append(0)

info_frame = Frame(tk)
info_frame.pack(fill=X)

def update_time():
    global playTime, play_time, xBtn, yBtn, timer_id

    if playTime is not None and nMoves < (xBtn * yBtn - mines):
        elapsed_time = int(time.time() - playTime)
        remaining_time = play_time - elapsed_time

        if remaining_time <= 0:
            remaining_time = 0
            tkinter.messagebox.showinfo("Час вийшов!", "Ви програли")
            mainloop()

        time_label.config(text='Час: {} сек'.format(remaining_time))

        if remaining_time > 0:
            timer_id = time_label.after(1000, update_time)
        else:
            time_label.config(text='Час: 0 сек')

def update_mines_label():
    remaining_mines = mines - mrk
    mines_label.config(text=f'Кількість мін : {remaining_mines}')

frmTop = Frame()
frmTop.pack(expand=YES, fill=BOTH)

mines_label = Label(info_frame, text='Кількість мін : ', font=('mono', 16))
mines_label.pack(side=LEFT, expand=NO, fill=X, anchor=N)

time_label = Label(info_frame, text='Час: 0 сек', font=('mono', 16))
time_label.pack(side=RIGHT, expand=NO, fill=X, anchor=N)

Button(frmTop, text='Правила', font=(16), command=rules).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='Легка', font=(16), command=set5x5).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='Середня', font=(16), command=set8x8).pack(side=LEFT, expand=YES, fill=X, anchor=N)
Button(frmTop, text='Складна', font=(16), command=set10x14).pack(side=LEFT, expand=YES, fill=X, anchor=N)

update_time()
mainloop()