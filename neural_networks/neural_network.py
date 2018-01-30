"""
Implementation of neural network with one hidden layer
"""
import random
import neural_networks.units as units

class NeuralNetwork:
    """
    Represents neural network with just one hidden layer
    """
    def __init__(self, layer_pattern):
        self.layers = []
        self.depth = len(layer_pattern)

        self.layers.append({'bias': [], 'neurons': []})
        for _ in range(layer_pattern[0]):
            self.layers[0]['neurons'].append(units.InputNeuron(0))

        for i in range(1, self.depth-1):
            self.layers.append({'bias': [], 'neurons': []})
            for _ in range(layer_pattern[i]):
                rand_weights = []
                for _ in range(layer_pattern[i-1]):
                    rand_weights.append(random.uniform(-1, 1))
                self.layers[-1]['neurons'].append(units.Neuron(rand_weights))
                self.layers[-2]['bias'].append(random.uniform(-1, 1))

        self.layers.append({'neurons': []})
        for i in range(layer_pattern[-1]):
            rand_weights = []
            for _ in range(layer_pattern[-2]):
                rand_weights.append(random.uniform(-1, 1))
            self.layers[-1]['neurons'].append(units.Neuron(rand_weights))
            self.layers[-2]['bias'].append(random.uniform(-1, 1))

    def feed_forward(self, inputs, activation):
        """
        Feeds forward the input values
        """
        for i, value in enumerate(inputs):
            self.layers[0]['neurons'][i].set_value(value)


        for i in range(1, self.depth):
            for j, neuron in enumerate(self.layers[i]['neurons']):
                neuron.calculate(
                    [neuron.get_value() for neuron in self.layers[i-1]['neurons']],
                    activation, self.layers[i-1]['bias'][j])

        return [neuron.get_value() for neuron in self.layers[-1]['neurons']]

    def get_neuron(self, layer, index):
        """
        Returns [layer, index] neuron
        """
        return self.layers[layer]['neurons'][index]

    def get_layer(self, layer):
        """
        Returns layer
        """
        return self.layers[layer]['neurons']

    def set_neuron(self, layer, index, neuron):
        """
        Returns [layer, index] neuron
        """
        self.layers[layer]['neurons'][index] = neuron

    def set_layer(self, layer):
        """
        Returns layer
        """
        self.layers[layer]['neurons'] = layer

