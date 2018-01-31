"""
Main
"""
import random
import tkinter as tk
import player
import neural_networks as nn
import genetic_algorithm as ga

class Game:
    """
    Game
    """
    def __init__(self):
        self.master = tk.Tk()
        self.epochs = 0
        self.dimensions = [800, 600]
        self.hits = []
        self.target_location = [700, 300]
        self.players = [player.Player((100, 200)),
                        player.Player((100, 220)),
                        player.Player((100, 240)),
                        player.Player((100, 260)),
                        player.Player((100, 280)),
                        player.Player((100, 300))
                        #player.Player((100, 420)),
                        #player.Player((100, 480)),
                        #player.Player((100, 540))
                        ]
        self.target = player.Target(self.target_location)
        self.canvas = tk.Canvas(self.master, width=self.dimensions[0], height=self.dimensions[1])
        self.genetic_evolver = ga.GeneticAlgorithm(self.players)
        self.epochs_text = None

    def init_canvas(self):
        """
        Inits the canvas
        """
        self.canvas.pack()

    def start(self):
        """
        Starts animating
        """
        self.epochs_text = self.canvas.create_text(30, 30, text="epochs: " + str(self.epochs))
        for plr in self.players:
            plr.draw(self.canvas)
        self.target.draw(self.canvas)
        self.shoot()
        tk.mainloop()

    def shoot(self):
        """
        Takes care of shooting animation
        """
        results = self.genetic_evolver.get_results(self.target_location)
        for i, plr in enumerate(self.players):
            if not plr.arrow_stopped:
                plr.shoot(self.canvas, [results[i][0], results[i][1]], results[i][2])
        self.detect_hit()
        self.finish_epoch()
        self.master.after(2, self.shoot)

    def finish_epoch(self):
        """
        Resets all player's arrows
        """
        if not [plr for plr in self.players if not plr.arrow_stopped]:
            self.next_generation()
            self.canvas.delete("all")
            for plr in self.players:
                plr.reset()
                plr.draw(self.canvas)
            self.target.draw(self.canvas)
            self.canvas.delete(self.epochs_text)
            self.epochs += 1
            self.epochs_text = self.canvas.create_text(30, 30, text="epochs: " + str(self.epochs))
            if self.epochs % 100 == 0:
                target_y = random.randint(100, 500)
                self.target_location[1] = target_y
                self.target.player_y = target_y

    def next_generation(self):
        """
        Evolve the next generation
        """
        self.genetic_evolver.evolve(self.target_location)

    def detect_hit(self):
        """
        Detects if any arrow has hit the target
        """
        for pl in self.players:
            if not pl.arrow_stopped:
                arrow_coords = pl.get_arrow_coordinates()
                if self.is_out_of_field(arrow_coords):
                    pl.stop_arrow()
                if self.hit(arrow_coords):
                    self.hits.append(self.canvas.create_text(
                        self.target_location[0] + random.randint(-40, 40),
                        self.target_location[1] + random.randint(-60, -10),
                        text="HIT!"))
                    self.master.after(2000, self.remove_hit_announce)
                    pl.hit()
                    pl.stop_arrow()
                if self.headshot(arrow_coords):
                    self.hits.append(self.canvas.create_text(
                        self.target_location[0] + random.randint(-40, 40),
                        self.target_location[1] + random.randint(-60, -10),
                        text="HEADSHOT!"))
                    self.master.after(2000, self.remove_hit_announce)
                    pl.headshot()
                    pl.stop_arrow()

    def is_out_of_field(self, arrow_coords):
        """
        Boolean check if arrow is out of the field
        """
        return (arrow_coords[0] < 0
                or arrow_coords[0] > self.dimensions[0]
                or arrow_coords[1] < 0
                or arrow_coords[1] > self.dimensions[1])

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

GAME = Game()
GAME.init_canvas()
GAME.start()
