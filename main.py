"""
Main
"""
import random
import tkinter as tk
import player
import neural_networks as nn

class Game:
    """
    Game
    """
    def __init__(self):
        self.master = tk.Tk()
        self.hits = []
        self.target_location = [700, 300]
        self.players = [player.Player((100, 500)),
                        player.Player((100, 200)),
                        player.Player((100, 400))]
        self.target = player.Target(self.target_location)
        self.canvas = tk.Canvas(self.master, width=800, height=600)

    def init_canvas(self):
        """
        Inits the canvas
        """
        self.canvas.pack()

    def start(self):
        """
        Starts animating
        """
        for pl in self.players:
            pl.draw(self.canvas)
        self.target.draw(self.canvas)
        self.shoot()
        tk.mainloop()

    def shoot(self):
        """
        Takes care of shooting animation
        """
        for pl in self.players:
            if not pl.arrow_stopped:
                pl.shoot(self.canvas, [700 - pl.player_x, 140-pl.player_y], 15)
        self.detect_hit()
        self.master.after(4, self.shoot)

    def detect_hit(self):
        """
        Detects if any arrow has hit the target
        """
        for pl in self.players:
            if not pl.arrow_stopped:
                arrow_coords = pl.get_arrow_coordinates()
                if self.hit(arrow_coords):
                    self.hits.append(self.canvas.create_text(
                        self.target_location[0] + random.randint(-40, 40),
                        self.target_location[1] + random.randint(-60, -10),
                        text="HIT!"))
                    self.master.after(2000, self.remove_hit_announce)
                    pl.stop_arrow()
                if self.headshot(arrow_coords):
                    self.hits.append(self.canvas.create_text(
                        self.target_location[0] + random.randint(-40, 40),
                        self.target_location[1] + random.randint(-60, -10),
                        text="HEADSHOT!"))
                    pl.stop_arrow()


    def hit(self, arrow_coords):
        """
        Boolean check if arrow hits the target
        """
        return (arrow_coords[0] < self.target_location[0] + 20
                and arrow_coords[0] > self.target_location[0] - 8
                and arrow_coords[1] < self.target_location[1] + 50
                and arrow_coords[1] > self.target_location[1] + 10)

    def headshot(self, arrow_coords):
        """
        Boolean check if arrow headshots the target
        """
        return (arrow_coords[0] < self.target_location[0] + 20
                and arrow_coords[0] > self.target_location[0] - 6
                and arrow_coords[1] < self.target_location[1] + 10
                and arrow_coords[1] > self.target_location[1] - 2)

    def remove_hit_announce(self):
        """
        Removes Hit! text
        """
        for text_id in self.hits:
            self.canvas.delete(text_id)

#GAME = Game()
#GAME.init_canvas()
#GAME.start()
NN = nn.neural_net.NeuralNetwork([2, 3, 3], 1)
result = NN.feed_forward([500, 200], nn.f.ReLU)
print(result)