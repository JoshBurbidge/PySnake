from tkinter import *
from tkinter import ttk
import game

def startGame():
    print("starting game...")
    game.main()

window = Tk()
window.title("snake game")

mainframe = ttk.Frame(window, padding="0.4i")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

start = Button(mainframe, text='Start New Game', command=startGame).grid()


mainloop()