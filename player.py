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
        self.hits = 0
        self.arrow_delta = [0, 0]
        self.closest_to_target = 10000
        self.frames = 0
        self.shooted = False
        self.player_x = location[0]
        self.player_y = location[1]
        self.arrow_x = self.player_x+25
        self.arrow_y = self.player_y+8
        self.size = 3
        self.arrow_canvas = None
        self.arrow = None
        self.waiting = False
        self.load_sprites()
        self.hitted = 0

    def load_sprites(self):
        """
        Loads resources
        """
        bow_img = Image.open("resources/fiery_bow.png")
        bow_img = bow_img.resize((18, 27), Image.ANTIALIAS)
        self.bow = ImageTk.PhotoImage(bow_img)

        arrow_img = Image.open("resources/arrow.png")
        arrow_img = arrow_img.rotate(-90)
        self.arrow_img = arrow_img.resize((70, 70), Image.ANTIALIAS)

    def hit(self):
        """
        Direct hit
        """
        self.hits += 1
        self.hitted = 1

    def headshot(self):
        """
        Direct headshot
        """
        self.hits += 1
        self.hitted = 2

    def reset(self):
        """
        Resets arrow
        """
        self.frames = 0
        self.hitted = 0
        self.arrow_x = self.player_x+25
        self.arrow_y = self.player_y+8
        self.waiting = False
        self.shooted = False
        self.closest_to_target = 10000

    def get_frames(self):
        """
        Returns how much 'time' it took the arrow to reach destination
        """
        return self.frames

    def stop_arrow(self):
        """
        Stops arrow
        """
        self.waiting = True

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
        canvas.create_line(self.player_x-30, self.player_y+35,
                           self.player_x+30, self.player_y+35, fill="black", width=self.size)
        #body
        canvas.create_line(self.player_x, self.player_y,
                           self.player_x, self.player_y + 20, fill="black", width=self.size)
        #right arm
        canvas.create_line(self.player_x, self.player_y+8, self.player_x+14, self.player_y+8,
                           fill="black", width=self.size)
        #left arm
        canvas.create_line(self.player_x, self.player_y+8, self.player_x-10, self.player_y+25,
                           fill="black", width=self.size)
        #right leg
        canvas.create_line(self.player_x, self.player_y+20, self.player_x+8, self.player_y+35,
                           fill="black", width=self.size)
        #right leg
        canvas.create_line(self.player_x, self.player_y+20, self.player_x-8, self.player_y+35,
                           fill="black", width=self.size)
        canvas.create_image(self.player_x+12, self.player_y+8, image=self.bow)

        self.arrow = ImageTk.PhotoImage(self.arrow_img)
        self.arrow_canvas = canvas.create_image(self.arrow_x, self.arrow_y, image=self.arrow)

    def check_distance(self, target):
        dist = math.sqrt((target[0] - self.arrow_x) ** 2 + (target[1] - self.arrow_y) ** 2)
        if dist < self.closest_to_target:
            self.closest_to_target = dist

    def shoot(self, direction, power):
        normalised_direction = utils.normalise(direction)
        self.arrow_delta[0] = normalised_direction[0] * power
        self.arrow_delta[1] = normalised_direction[1] * power
        self.shooted = True

    def update_arrow(self, canvas, gravity, rain, wind):
        """
        Shoots arrow in direction of 'towards' (x, y) point with some power
        """
        if self.waiting:
            return

        self.arrow = ImageTk.PhotoImage(self.arrow_img.rotate(
            math.degrees(math.atan2(self.arrow_delta[0], self.arrow_delta[1])) - 90))
        self.arrow_canvas = canvas.create_image(self.arrow_x, self.arrow_y, image=self.arrow)
        # canvas.create_oval(self.arrow_x,  self.arrow_y,
        #                   self.arrow_x + 3,  self.arrow_y + 3,
        #                   fill="black")
        self.frames += 1
        self.arrow_delta[1] += gravity
        self.arrow_delta[1] += rain
        self.arrow_delta[0] += wind[0]
        self.arrow_delta[1] += wind[1]

        self.arrow_x += self.arrow_delta[0] 
        self.arrow_y += self.arrow_delta[1] 


class SmartPlayer(Player):
    def __init__(self, location):
        Player.__init__(self, location)
        self.neural_network = None
    
    def set_neural_network(self, neural_network):
        """
        Assigns neural network to player
        """
        self.neural_network = neural_network

    def get_neural_network(self):
        """
        Returns neural network of player
        """
        return self.neural_network

    def delete_neural_network(self):
        """
        Deletes neural network
        """
        self.neural_network = None

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
