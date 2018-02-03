"""
Implements evolving algorithm for neural networks
"""
import math
import random
import neural_networks as nn
import evolver.mutation_operations as mut_op
import evolver.crossbreed_oprations as crs_op
from player import SmartPlayer

class GeneticAlgorithm:
    """
    Implements genetic evolving of neural networks
    """
    def __init__(self, population):
        self.population_count = len(population)
        self.neural_networks_pattern = [6, 8, 8, 3]
        self.free_spaces = []
        self.population = population
        self.offspring_termination_number = 0.4
        self.mutation_probability = 0.008
        for individual in self.population:
            individual.set_neural_network(nn.neural_network.NeuralNetwork(self.neural_networks_pattern))

    def get_results(self, target, gravity, rain, wind):
        """
        Makes test calculations of the population
        """
        results = []
        for individual in self.population:
            results.append(individual.get_neural_network().feed_forward(
                [target[0] - individual.player_x,
                 target[1] - individual.player_y,
                 gravity, 
                 rain,
                 wind[0],
                 wind[1]],
                nn.f.identity))
        return results

    def fitness_function(self, closest_shot, frames, hit):
        """
        Calculates how good all shots are based on how far the
        arrow is from the target and how much time it took to reach it
        """
        fintess_values = []
        distance = closest_shot
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
        self.population.sort(key=lambda x: self.fitness_function(x.closest_to_target,
                                                                 x.get_frames(),
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

        sequence = [x for x in range(0, 4)]
        random.shuffle(sequence)
        for i in range(0, len(sequence), 2):
            pl = SmartPlayer([self.free_spaces[0][0], self.free_spaces[0][1]])
            del self.free_spaces[0]
            rand_op = random.randint(0, 1)
            if rand_op == 0:
                new_nn = crs_op.swap_layer(self.population[sequence[i]].get_neural_network(),
                                           self.population[sequence[i+1]].get_neural_network(),
                                           self.neural_networks_pattern)
            if rand_op == 1:
                new_nn = crs_op.swap_neuron(self.population[sequence[i]].get_neural_network(),
                                            self.population[sequence[i+1]].get_neural_network(),
                                            self.neural_networks_pattern)
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
                                                       [mut_op.lesser_shift])

            if individual.hitted == 0:
                individual.get_neural_network().mutate(self.mutation_probability,
                                                       [mut_op.shift])

    def evolve(self, target):
        """
        One evolutionary cycle
        """
        self.selection(target)
        self.crossbreed(target)
        self.mutation()
