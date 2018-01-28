from tkinter import *

class Player:
    """
    Archer
    """
    def __init__(self, location):
        self.x = location[0]
        self.y = location[1]
        self.size = 4

    def draw(self, canvas):
        """
        Player draws itself
        """
        canvas.create_oval(self.x - self.size * 1.5, self.y - self.size * 1.5,
                           self.x + self.size * 1.5, self.y + self.size * 1.5, fill="black")
        canvas.create_line(self.x, self.y, self.x, self.y + 25, fill="black", width=self.size)
        canvas.create_line(self.x, self.y+8, self.x+10, self.y+25,
                           fill="black", width=self.size)
        canvas.create_line(self.x, self.y+8, self.x-10, self.y+25,
                           fill="black", width=self.size)
        canvas.create_line(self.x, self.y+25, self.x-10, self.y+45,
                           fill="black", width=self.size)
        canvas.create_line(self.x, self.y+25, self.x+10, self.y+45,
                           fill="black", width=self.size)

class Game:
    """
    Game
    """
    def __init__(self):
        self.master = Tk()
        self.main_player = Player((100, 100))
        self.canvas = Canvas(self.master, width=800, height=600)


    def init_canvas(self):
        """
        Inits the canvas
        """
        self.canvas.pack()

    def start(self):
        """
        Starts animating
        """
        self.main_player.draw(self.canvas)
        mainloop()

GAME = Game()
GAME.init_canvas()
GAME.start()
