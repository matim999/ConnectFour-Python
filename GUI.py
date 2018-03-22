#! /usr/bin/env python3

from tkinter import *
from ConnectFour import ConnectFour


class FullColumnException(Exception):
    pass

class Rules:
    def __init__(self, master):
        self.master = master
        master.title('Rules')
        label1 = Label(master, text='Liczba kolumn:')
        label1.grid(row=0)
        s1 = Scale(master, from_=4, to=20, orient=HORIZONTAL)
        s1.grid(row=1)
        label2 = Label(master, text='Liczba wierszy:')
        label2.grid(row=2)
        s2 = Scale(master, from_=4, to=20, orient=HORIZONTAL)
        s2.grid(row=3)
        button = Button(master, text="Ok", command=lambda x=17: self.newGUI(int(s1.get()), int(s2.get())))
        button.grid(row=4)

    def newGUI(self, col, row):
        global root, app
        app.destory1()
        root = Tk()
        app = GUI(root, columns=col, rows=row)
        root.mainloop()
        self.master.destroy()

class GUI:
    elementSize = 52
    gridBorder = 3
    gridColor = "#AAA"
    p1Color = "#4096EE"
    p2Color = "#FF1A00"
    backgroundColor = "#FFFFFF"
    gameOn = False
    
    def __init__(self, master, columns=7, rows=12):
        self.master = master
        self.buttons = [Button(master, text="k"+str(i), command= lambda i=i: self.dropButtonClick(i)) for i in range(columns)]
        self.columns = columns
        self.rows = rows

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        x = 12
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Change rules", command= lambda x=x: self.openChildWindow())
        menubar.add_cascade(label="File", menu=fileMenu)

        master.title('Connect Four')

        label = Label(master)
        label.grid(row=0)

        for i in range(columns):
            self.buttons[i].config(height=3, width=6)
            self.buttons[i].grid(row=1, column=i)

        button = Button(master, text="New Game!", command=self._newGameButton)
        button.grid(row=3, columnspan = columns)
        
        self.canvas = Canvas(master, width=200, height=50, background=self.backgroundColor, highlightthickness=0)
        self.canvas.grid(row=2, columnspan = columns)

        self.currentPlayerVar = StringVar(self.master, value="")
        self.currentPlayerLabel = Label(self.master, textvariable=self.currentPlayerVar, anchor=W)
        self.currentPlayerLabel.grid(row=4, columnspan = columns)

        self.newGame()

    def draw(self):       
        for c in range(self.game.size['c']):
            for r in range(self.game.size['r']):
                if r >= len(self.game.grid[c]): continue
                
                x0 = c*self.elementSize
                y0 = r*self.elementSize
                x1 = (c+1)*self.elementSize
                y1 = (r+1)*self.elementSize
                fill = self.p1Color if self.game.grid[c][r] == self.game.players[True] else self.p2Color
                self.canvas.create_oval(x0 + 2,
                                        self.canvas.winfo_height() - (y0 + 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 - 2),
                                        fill = fill, outline=self.gridColor)

    def drawGrid(self):
        x0, x1 = 0, self.canvas.winfo_width()
        for r in range(1, self.game.size['r']):
            y = r*self.elementSize
            self.canvas.create_line(x0, y, x1, y, fill=self.gridColor)

        y0, y1 = 0, self.canvas.winfo_height()
        for c in range(1, self.game.size['c']):
            x = c*self.elementSize
            self.canvas.create_line(x, y0, x, y1, fill=self.gridColor)

    def drop(self, column):
        try:
            return self.game.drop(column)
        except ValueError:
            return False

    def newGame(self):
        # Ask for players' names
        self.p1 = 'Blue'
        self.p2 = 'Red'

        # Ask for grid size
        
        self.game = ConnectFour(columns=self.columns, rows=self.rows)

        self.canvas.delete(ALL)
        self.canvas.config(width=(self.elementSize)*self.game.size['c'],
                           height=(self.elementSize)*self.game.size['r'])
        self.master.update() # Rerender window
        self.drawGrid()
        self.draw()

        self._updateCurrentPlayer()

        self.gameOn = True

    def _updateCurrentPlayer(self):
        p = self.p1 if self.game.first_player else self.p2
        self.currentPlayerVar.set('Current player: ' + p)

    def dropButtonClick(self, c):
        if not self.gameOn: return
        if self.game.game_over: return

        self.drop(c)
        self.draw()
        self._updateCurrentPlayer()

        if self.game.game_over:
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            if self.game.game_over == 'draw':
                t = 'DRAW!'
            else:
                winner = self.p1 if self.game.first_player else self.p2
                t = winner + ' won!'
            self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")

    def _newGameButton(self):
        self.newGame()

    def openChildWindow(self):
        root2 = Toplevel(self.master)
        Rules(root2)

    def destory1(self):
        self.master.destroy()

root = Tk()
app = GUI(root)

root.mainloop()
