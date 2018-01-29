"""
Implements evolving algorithm for neural networks
"""
import neural_networks as nn


class GeneticAlgorithm:
    """
    Implements genetic evolving of neural networks
    """
    def __init__(self, population):
        self.population_count = len(population)
        self.population = list(population)
        self.neural_networks = []
        for _ in range(0, self.population_count):
            self.neural_networks.append(nn.neural_network.NeuralNetwork([2, 3, 3]))

    def get_results(self, target):
        """
        Makes test calculations of the population
        """
        results = []
        for i in range(0, self.population_count):
            results.append(self.neural_networks[i].feed_forward(
                [target[0]-self.population[i].player_x,
                 target[1]-self.population[i].player_y],
                nn.f.ReLU))
