"""
Activation function
"""
import math

def step_function(value):
    """
    Step function
    """
    if value >= 1:
        return 1
    return 0

def sigmoid(value):
    """
    Implementation of sigmoid function
    """
    return 1 / (1 + math.exp(-value))

def sigmoid_derivative(value):
    """
    Returns value of the derivative of the sigmoid function
    """
    return value * (1 - value)

def hyperbolic_tangent(value):
    """
    Return the hyperbolic tangent of x
    """
    return math.tanh(value)

def hyperbolic_tangent_derivative(value):
    """
    Returns derivative value of the hyberbolic tangent
    """
    return 1.0 - math.tanh(value) ** 2

def ReLU(x):
    """
    Rectifier
    """
    return 0.1 * x * (x > 0)
