"""
Implements evolving algorithm for neural networks
"""
import math
import random
import neural_networks as nn


class GeneticAlgorithm:
    """
    Implements genetic evolving of neural networks
    """
    def __init__(self, population):
        self.population_count = len(population)
        self.neural_networks_pattern = [2, 4, 3]
        self.population = population
        self.offspring_termination_number = 0.5
        self.reproduction_number = 0.4
        for individual in self.population:
            individual.set_neural_network(nn.neural_network.NeuralNetwork(self.neural_networks_pattern))

    def get_results(self, target):
        """
        Makes test calculations of the population
        """
        results = []
        for individual in self.population:
            results.append(individual.get_neural_network().feed_forward(
                [target[0] - individual.player_x,
                 target[1] - individual.player_y],
                nn.f.PReLU))
        return results

    def fitness_function(self, shot, target, frames):
        """
        Calculates how good all shots are based on how far the
        arrow is from the target and how much time it took to reach it
        """
        fintess_values = []
        distance = math.sqrt((target[0] - shot[0]) ** 2 + (target[1] - shot[1]) ** 2)
        fintess_values.append(distance + frames)
        return fintess_values

    def kill_offspring(self, target):
        """
        Kills weakest archers
        """
        to_be_killed = math.floor(self.offspring_termination_number * self.population_count)
        self.population.sort(key=lambda x: self.fitness_function(x.get_arrow_coordinates(),
                                                                 target, x.get_frames()),
                             reverse=True)
        print(to_be_killed)
        for _ in range(0, to_be_killed):
            del self.population[0]
            self.population_count -= 1

    def crossbreed(self):
        """
        Crossbreeds archers
        """
        sequence = [x for x in range(0, self.population_count-1)]
        random.shuffle(sequence)
        for i in range(len(sequence), 2):
            rand_op = random.randint(0, 1)
            if rand_op == 0:
                self.swap_layer(self.population[sequence[i]].get_neural_network(),
                                self.population[sequence[i+1]].get_neural_network())
            if rand_op == 1:
                self.swap_neuron(self.population[sequence[i]].get_neural_network(),
                                 self.population[sequence[i+1]].get_neural_network())

    def swap_neuron(self, nn_a, nn_b):
        """
        Swaps random neuron in the two neural networks
        """
        new_neural_newtork = nn.neural_network.NeuralNetwork(self.neural_networks_pattern)
        for layer in range(len(self.neural_networks_pattern)):
            new_neural_newtork.set_layer(nn_a.get_layer(layer))
        rand_layer = random.randint(1, len(self.neural_networks_pattern)-1)
        rand_neuron = random.randint(0, len(self.neural_networks_pattern[rand_layer])-1)

        b_neuron = nn_b.get_neuron(rand_layer, rand_neuron)
        new_neural_newtork.set_neuron(rand_layer, rand_neuron, b_neuron)
        return new_neural_newtork

    def swap_layer(self, nn_a, nn_b):
        """
        Swaps random neuron in the two neural networks
        """
        new_neural_newtork = nn.neural_network.NeuralNetwork(self.neural_networks_pattern)
        for layer in range(len(self.neural_networks_pattern)):
            new_neural_newtork.set_layer(nn_a.get_layer(layer))
        rand_layer = random.randint(1, len(self.neural_networks_pattern)-1)

        a_layer = nn_a.get_layer(rand_layer)
        new_neural_newtork.set_layer(a_layer)
        return new_neural_newtork

    def evolve(self, target):
        """
        One evolutionary cycle
        """
        self.kill_offspring(target)
        self.crossbreed()