from tkinter import *
from PIL import ImageTk, Image
import math

def vector_magnitute(vector):
    vector_sum = 0
    for value in vector:
        vector_sum += value ** 2
    return math.sqrt(vector_sum)

def normalise(vector):
    magnitude = vector_magnitute(vector)
    normalised = []
    for value in vector:
        normalised.append(value / magnitude)
    return normalised
    

class Player:
    """
    Archer
    """
    def __init__(self, location):
        self.arrow_delta = [0, 0]
        self.gravity = [0, 0.1]
        self.shooted = False
        self.player_x = location[0]
        self.player_y = location[1]
        self.size = 4
        self.arrow_canvas = {}
        self.load_sprites()

    def load_sprites(self):
        """
        Loads resources
        """
        bow_img = Image.open("resources/fiery_bow.png")
        bow_img = bow_img.resize((20, 30), Image.ANTIALIAS)
        self.bow = ImageTk.PhotoImage(bow_img)

        self.arrow_img = Image.open("resources/arrow.png")
        self.arrow_img = self.arrow_img.rotate(-90)
        self.arrow_img = self.arrow_img.resize((70, 70), Image.ANTIALIAS)
        self.arrow = ImageTk.PhotoImage(self.arrow_img)

    def draw(self, canvas):
        """
        Player draws itself
        """
        canvas.create_oval(self.player_x - self.size * 1.5, self.player_y - self.size * 1.5,
                           self.player_x + self.size * 1.5, self.player_y + self.size * 1.5, fill="black")
        #platform
        canvas.create_line(self.player_x-30, self.player_y+45, self.player_x+30, self.player_y+45, fill="black", width=self.size)
        #body
        canvas.create_line(self.player_x, self.player_y, self.player_x, self.player_y + 25, fill="black", width=self.size)
        #right arm
        canvas.create_line(self.player_x, self.player_y+10, self.player_x+18, self.player_y+10,
                           fill="black", width=self.size)
        #left arm
        canvas.create_line(self.player_x, self.player_y+8, self.player_x-10, self.player_y+25,
                           fill="black", width=self.size)
        #right leg
        canvas.create_line(self.player_x, self.player_y+25, self.player_x+10, self.player_y+45,
                           fill="black", width=self.size)
        #right leg
        canvas.create_line(self.player_x, self.player_y+25, self.player_x-10, self.player_y+45,
                           fill="black", width=self.size)
        canvas.create_image(self.player_x+15, self.player_y+8, image=self.bow)

        canvas.create_image(self.player_x+25, self.player_y+8, image=self.arrow)

    def shoot(self, canvas, towards, power):
        """
        Shoots arrow in direction of 'towards' (x, y) point with some power
        """
        if not self.shooted:
            direction = [towards[0] - self.player_x, towards[1] - self.player_y]
            normalised_direction = normalise(direction)
            self.arrow_delta[0] = normalised_direction[0] * power
            self.arrow_delta[1] = normalised_direction[1] * power
            self.shooted = True
        self.arrow_delta[0] += self.gravity[0]
        self.arrow_delta[1] += self.gravity[1]

        self.arrow_img = self.arrow_img.rotate(-math.atan2(self.arrow_delta[0], self.arrow_delta[1]))
        self.arrow = ImageTk.PhotoImage(self.arrow_img)
        canvas.create_image(self.player_x+25, self.player_y+8, image=self.arrow)
        
        #canvas.move(self.arrow_canvas, self.arrow_delta[0], self.arrow_delta[1])
        canvas.update()

class Game:
    """
    Game
    """
    def __init__(self):
        self.master = Tk()
        self.main_player = Player((100, 500))
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
        self.shoot()
        mainloop()

    def shoot(self):
        """
        Takes care of shooting animation
        """
        self.main_player.shoot(self.canvas, [500, 200], 7)
        self.master.after(16, self.shoot)


GAME = Game()
GAME.init_canvas()
GAME.start()
