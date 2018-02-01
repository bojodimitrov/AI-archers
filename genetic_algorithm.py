"""
Implements evolving algorithm for neural networks
"""
import math
import random
import neural_networks as nn
from player import Player

class GeneticAlgorithm:
    """
    Implements genetic evolving of neural networks
    """
    def __init__(self, population):
        self.population_count = len(population)
        self.neural_networks_pattern = [3, 5, 5, 3]
        self.free_spaces = []
        self.population = population
        self.offspring_termination_number = 0.4
        self.mutation_probability = 0.008
        for individual in self.population:
            individual.set_neural_network(nn.neural_network.NeuralNetwork(self.neural_networks_pattern))

    def get_results(self, target, gravity):
        """
        Makes test calculations of the population
        """
        results = []
        for individual in self.population:
            results.append(individual.get_neural_network().feed_forward(
                [target[0] - individual.player_x,
                 target[1] - individual.player_y,
                 gravity],
                nn.f.identity))
        return results

    def fitness_function(self, shot, target, frames, hit):
        """
        Calculates how good all shots are based on how far the
        arrow is from the target and how much time it took to reach it
        """
        fintess_values = []
        distance = math.sqrt((target[0] - shot[0]) ** 2 + (target[1] - shot[1]) ** 2)
        fintess_value = distance
        if hit == 1:
            fintess_value /= 2
        if hit == 2:
            fintess_value /= 8
        fintess_values.append(fintess_value)
        return fintess_values

    def selection(self, target):
        """
        Kills weakest archers
        """
        to_be_killed = math.floor(self.offspring_termination_number * self.population_count)
        self.population.sort(key=lambda x: self.fitness_function(x.get_arrow_coordinates(),
                                                                 target, x.get_frames(),
                                                                 x.hitted),
                             reverse=True)
        for _ in range(0, to_be_killed):
            self.free_spaces.append([self.population[0].player_x, self.population[0].player_y])
            del self.population[0]
            self.population_count -= 1

    def crossbreed(self, target):
        """
        Crossbreeds archers
        """
        self.population.sort(key=lambda x: x.hitted)

        sequence = [x for x in range(0, 8)]
        random.shuffle(sequence)
        for i in range(0, len(sequence), 2):
            pl = Player([self.free_spaces[0][0], self.free_spaces[0][1]])
            del self.free_spaces[0]
            rand_op = random.randint(0, 1)
            if rand_op == 0:
                new_nn = self.swap_layer(self.population[sequence[i]].get_neural_network(),
                                         self.population[sequence[i+1]].get_neural_network())
            if rand_op == 1:
                new_nn = self.swap_neuron(self.population[sequence[i]].get_neural_network(),
                                          self.population[sequence[i+1]].get_neural_network())
            pl.set_neural_network(new_nn)
            self.population.append(pl)
            self.population_count += 1

    def mutation(self):
        """
        Mutates some of the archers
        """
        for individual in self.population:
            if individual.hitted == 1:
                individual.get_neural_network().mutate(self.mutation_probability / 2,
                                                       [self.lesser_shift])

            if individual.hitted == 0:
                individual.get_neural_network().mutate(self.mutation_probability,
                                                       [self.shift])

    def swap_neuron(self, nn_a, nn_b):
        """
        Swaps random neuron in the two neural networks
        """
        new_neural_newtork = nn.neural_network.NeuralNetwork(self.neural_networks_pattern)
        new_neural_newtork.set_input_layer(nn_a.get_layer(0))
        for layer in range(1, len(self.neural_networks_pattern)):
            new_neural_newtork.set_layer(layer, nn_a.get_layer(layer))
        rand_layer = random.randint(1, len(self.neural_networks_pattern) - 1)
        rand_neuron = random.randint(0, self.neural_networks_pattern[rand_layer] - 1)

        b_neuron = nn_b.get_neuron(rand_layer, rand_neuron)
        new_neural_newtork.set_neuron(rand_layer, rand_neuron, b_neuron)
        return new_neural_newtork

    def swap_layer(self, nn_a, nn_b):
        """
        Swaps random neuron in the two neural networks
        """
        new_neural_newtork = nn.neural_network.NeuralNetwork(self.neural_networks_pattern)
        new_neural_newtork.set_input_layer(nn_a.get_layer(0))
        for layer in range(1, len(self.neural_networks_pattern)):
            new_neural_newtork.set_layer(layer, nn_a.get_layer(layer))
        rand_layer = random.randint(1, len(self.neural_networks_pattern) - 1)
        b_layer = nn_b.get_layer(rand_layer)
        new_neural_newtork.set_layer(rand_layer, b_layer)
        return new_neural_newtork

    def replace_weight(self, weight):
        """
        Replaces weight
        """
        return random.randint(-1, 1)

    def scale(self, weight):
        """
        Scales weight by some value
        """
        return weight * random.uniform(0.5, 1.5)

    def shift(self, weight):
        """
        Adds random number between -0.8, 0.8
        """
        return weight + random.uniform(-0.8, 0.8)

    def swap_sign(self, weight):
        """
        Swaps sign of weight
        """
        return weight * (-1)

    def lesser_shift(self, weight):
        """
        Narrows the shift
        """
        return self.shift(weight) * 0.07

    def lesser_scale(self, weight):
        """
        Narrows the scale
        """
        return self.scale(weight) * 0.3
        

    def evolve(self, target):
        """
        One evolutionary cycle
        """
        self.selection(target)
        self.crossbreed(target)
        self.mutation()
