import random
import tkinter as tk
from player import SmartPlayer, Target
from tester import TrialTester
import neural_networks as nn
from evolver import ga
import physics_consts
from PIL import ImageTk, Image

EPOCHS_BETWEEN_TESTS = 50

class Game:
    """
    Game controller
    """
    def __init__(self):
        self.master = tk.Tk()
        self.epochs = 1
        self.dimensions = [1100, 800]
        self.hits = []
        self.target_location = [900, 300]
        self.target_movement = 1
        self.players = [SmartPlayer((150, 80)),
                        SmartPlayer((20, 180)),
                        SmartPlayer((80, 280)),
                        SmartPlayer((5, 380)),
                        SmartPlayer((70, 480)),
                        SmartPlayer((190, 580)),
                        # SmartPlayer((100, 420)),
                        # SmartPlayer((30, 600)),
                        # SmartPlayer((220, 140)),
                        # SmartPlayer((450, 230)),
                        # SmartPlayer((110, 660)),
                        # SmartPlayer((90, 350))
                        ]
        self.target = Target(self.target_location)
        self.canvas = tk.Canvas(self.master, width=self.dimensions[0], height=self.dimensions[1])
        self.genetic_evolver = ga.GeneticAlgorithm(self.players)
        self.epochs_text = None
        self.tester = TrialTester((100, 400), self.target_location)
        self.conduct_tests = False
        self.wind = self.init_wind_notifier()
        self.rain = self.init_rain_notifier()

    def init_wind_notifier(self):
        wind_image = Image.open("resources/wind.png")
        wind_image = wind_image.resize((30, 30), Image.ANTIALIAS)
        return ImageTk.PhotoImage(wind_image)

    def init_rain_notifier(self):
        rain_image = Image.open("resources/rain.png")
        rain_image = rain_image.resize((30, 30), Image.ANTIALIAS)
        return ImageTk.PhotoImage(rain_image)

    def init_canvas(self):
        """
        Inits the canvas
        """
        self.canvas.pack()

    def start(self):
        """
        Starts animating
        """
        self.draw()
        self.evaluate_shot()
        self.loop()
        tk.mainloop()

    def evaluate_shot(self):
        """
        Gets the direction and power of the shot from the neural networks
        """
        results = self.genetic_evolver.get_results(self.target_location,
                                                   physics_consts.GRAVITY,
                                                   physics_consts.rain(),
                                                   physics_consts.wind())
        for i, plr in enumerate(self.players):
            plr.shoot([results[i][0], results[i][1]], results[i][2])

    def activate_tests(self):
        if self.epochs % EPOCHS_BETWEEN_TESTS == 0:
            self.players.sort(key=lambda x: x.hits, reverse=True)
            print([x.hits for x in self.players])
            self.tester.init_tests(self.players[0], physics_consts.GRAVITY)
            self.conduct_tests = True
            self.epochs += 1

    def stop_tests(self):
        if self.tester.tests_finished():
            print(self.tester.get_test_results())
            self.draw()
            self.tester.reset()
            self.conduct_tests = False

    def reset_trial(self):
        self.canvas.delete('all')
        self.move_target()
        self.target.draw(self.canvas)
        self.tester.test_best_archer(self.canvas)

    def loop(self):
        """
        Takes care of shooting animation
        """
        self.activate_tests()
        if self.conduct_tests:
            self.stop_tests()
            self.refresh_arrows([self.tester.test_archer])
            if self.tester.archer_tried():
                self.reset_trial()
        else:
            self.refresh_arrows(self.players)
            self.finish_epoch()
        self.master.after(1, self.loop)
    
    def refresh_arrows(self, archers):
        """
        Updates arrow locations and checks for collisions
        """
        for archer in archers:
            archer.update_arrow(self.canvas,
                                physics_consts.GRAVITY,
                                physics_consts.rain(),
                                physics_consts.wind())
            archer.check_distance(self.target_location)
        self.detect_hit(archers)

    def finish_epoch(self):
        """
        Finishes one generation
        """
        if not [plr for plr in self.players if not plr.waiting]:
            #if self.epochs % 50 == 0:
            self.move_target()
            self.next_generation()
            self.canvas.delete("all")
            for plr in self.players:
                plr.reset()
            self.update_epochs()
            self.evaluate_shot()
            self.draw()

    def draw(self):
        self.epochs_text = self.canvas.create_text(40, 10, text="epochs: " + str(self.epochs))
        for plr in self.players:
            plr.draw(self.canvas)
        self.target.draw(self.canvas)
        self.canvas.create_image(20, 40, image=self.wind)
        self.canvas.create_text(80, 40, text=': ' + str(physics_consts.wind()))
        self.canvas.create_image(20, 70, image=self.rain)
        self.canvas.create_text(60, 70, text=': ' + str(physics_consts.rain()))

    def update_epochs(self):
        self.canvas.delete(self.epochs_text)
        self.epochs += 1

    def move_target(self):   
        if self.target_location[1] > 700:
            self.target_movement = -1
        if self.target_location[1] < 100:
            self.target_movement = 1
        target_y = self.target_location[1] + 10 * (self.target_movement)
        self.target_location[1] = target_y
        self.target.player_y = target_y

    def next_generation(self):
        """
        Evolve the next generation
        """
        self.genetic_evolver.evolve(self.target_location)

    def detect_hit(self, archers):
        """
        Detects if any arrow has hit the target
        """
        for pl in archers:
            if not pl.waiting:
                arrow_coords = pl.get_arrow_coordinates()
                if self.is_out_of_field(arrow_coords):
                    pl.stop_arrow()
                if self.hit(arrow_coords):
                    self.hits.append(self.canvas.create_text(
                        self.target_location[0] + random.randint(-40, 40),
                        self.target_location[1] + random.randint(-60, -10),
                        text="HIT!"))
                    pl.hit()
                    pl.stop_arrow()
                if self.headshot(arrow_coords):
                    self.hits.append(self.canvas.create_text(
                        self.target_location[0] + random.randint(-40, 40),
                        self.target_location[1] + random.randint(-60, -10),
                        text="HEADSHOT!"))
                    pl.headshot()
                    pl.stop_arrow()

    def is_out_of_field(self, arrow_coords):
        """
        Boolean check if arrow is out of the field
        """
        return (arrow_coords[0] < 0
                or arrow_coords[0] > self.dimensions[0]
                or arrow_coords[1] > self.dimensions[1])

    def hit(self, arrow_coords):
        """
        Boolean check if arrow hits the target
        """
        return (arrow_coords[0] < self.target_location[0] + 40
                and arrow_coords[0] > self.target_location[0] - 8
                and arrow_coords[1] < self.target_location[1] + 50
                and arrow_coords[1] > self.target_location[1] + 10)

    def headshot(self, arrow_coords):
        """
        Boolean check if arrow headshots the target
        """
        return (arrow_coords[0] < self.target_location[0] + 40
                and arrow_coords[0] > self.target_location[0] - 6
                and arrow_coords[1] < self.target_location[1] + 10
                and arrow_coords[1] > self.target_location[1] - 2)
