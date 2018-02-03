import random
import neural_networks as nn

def swap_neuron(nn_a, nn_b, pattern):
    """
    Swaps random neuron in the two neural networks
    """
    new_neural_newtork = nn.neural_network.NeuralNetwork(pattern)
    new_neural_newtork.set_input_layer(nn_a.get_layer(0))
    for layer in range(1, len(pattern)):
        new_neural_newtork.set_layer(layer, nn_a.get_layer(layer))
    rand_layer = random.randint(1, len(pattern) - 1)
    rand_neuron = random.randint(0, pattern[rand_layer] - 1)

    b_neuron = nn_b.get_neuron(rand_layer, rand_neuron)
    new_neural_newtork.set_neuron(rand_layer, rand_neuron, b_neuron)
    return new_neural_newtork

def swap_layer(nn_a, nn_b, pattern):
    """
    Swaps random neuron in the two neural networks
    """
    new_neural_newtork = nn.neural_network.NeuralNetwork(pattern)
    new_neural_newtork.set_input_layer(nn_a.get_layer(0))
    for layer in range(1, len(pattern)):
        new_neural_newtork.set_layer(layer, nn_a.get_layer(layer))
    rand_layer = random.randint(1, len(pattern) - 1)
    b_layer = nn_b.get_layer(rand_layer)
    new_neural_newtork.set_layer(rand_layer, b_layer)
    return new_neural_newtork