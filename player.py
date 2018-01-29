"""
Contains player class
"""
import math
import utils
from PIL import ImageTk, Image


class Player:
    """
    Archer
    """
    def __init__(self, location):
        self.arrow_delta = [0, 0]
        self.gravity = [0, 0.2]
        self.shooted = False
        self.player_x = location[0]
        self.player_y = location[1]
        self.arrow_x = self.player_x+25
        self.arrow_y = self.player_y+8
        self.size = 4
        self.arrow_canvas = {}
        self.arrow = {}
        self.arrow_stopped = False
        self.load_sprites()

    def load_sprites(self):
        """
        Loads resources
        """
        bow_img = Image.open("resources/fiery_bow.png")
        bow_img = bow_img.resize((20, 30), Image.ANTIALIAS)
        self.bow = ImageTk.PhotoImage(bow_img)

        arrow_img = Image.open("resources/arrow.png")
        arrow_img = arrow_img.rotate(-90)
        self.arrow_img = arrow_img.resize((70, 70), Image.ANTIALIAS)

    def stop_arrow(self):
        """
        Stops arrow
        """
        self.arrow_stopped = True

    def get_arrow_coordinates(self):
        """
        Returns [x, y] coordinates of shooted arrow
        """
        return [self.arrow_x, self.arrow_y]

    def draw(self, canvas):
        """
        Player draws itself
        """
        canvas.create_oval(self.player_x - self.size * 1.5, self.player_y - self.size * 1.5,
                           self.player_x + self.size * 1.5, self.player_y + self.size * 1.5,
                           fill="black")
        #platform
        canvas.create_line(self.player_x-30, self.player_y+45,
                           self.player_x+30, self.player_y+45, fill="black", width=self.size)
        #body
        canvas.create_line(self.player_x, self.player_y,
                           self.player_x, self.player_y + 25, fill="black", width=self.size)
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

        self.arrow = ImageTk.PhotoImage(self.arrow_img)
        self.arrow_canvas = canvas.create_image(self.arrow_x, self.arrow_y, image=self.arrow)

    def shoot(self, canvas, direction, power):
        """
        Shoots arrow in direction of 'towards' (x, y) point with some power
        """
        if not self.shooted:
            normalised_direction = utils.normalise(direction)
            self.arrow_delta[0] = normalised_direction[0] * power
            self.arrow_delta[1] = normalised_direction[1] * power
            self.shooted = True

        self.arrow = ImageTk.PhotoImage(self.arrow_img.rotate(
            math.degrees(math.atan2(self.arrow_delta[0], self.arrow_delta[1])) - 90))
        self.arrow_canvas = canvas.create_image(self.arrow_x, self.arrow_y, image=self.arrow)

        self.arrow_delta[0] += self.gravity[0]
        self.arrow_delta[1] += self.gravity[1]

        self.arrow_x += self.arrow_delta[0]
        self.arrow_y += self.arrow_delta[1]

class Target(Player):
    """
    Represents shooting target
    """
    def __init__(self, location):
        Player.__init__(self, location)

    def draw(self, canvas):
        """
        Player draws itself
        """
        canvas.create_oval(self.player_x - self.size * 1.5, self.player_y - self.size * 1.5,
                           self.player_x + self.size * 1.5, self.player_y + self.size * 1.5,
                           fill="black")
        #platform
        canvas.create_line(self.player_x-30, self.player_y+45,
                           self.player_x+30, self.player_y+45, fill="black", width=self.size)
        #body
        canvas.create_line(self.player_x, self.player_y,
                           self.player_x, self.player_y + 25, fill="black", width=self.size)
        #right arm
        canvas.create_line(self.player_x, self.player_y+8, self.player_x+10, self.player_y+25,
                           fill="black", width=self.size)
        #left arm
        canvas.create_line(self.player_x, self.player_y+8, self.player_x-10, self.player_y+25,
                           fill="black", width=self.size)
        #right leg
        canvas.create_line(self.player_x, self.player_y+25, self.player_x+10, self.player_y+45,
                           fill="black", width=self.size)
        #left leg
        canvas.create_line(self.player_x, self.player_y+25, self.player_x-10, self.player_y+45,
                           fill="black", width=self.size)
