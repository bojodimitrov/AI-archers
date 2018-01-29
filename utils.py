"""
Utility functions
"""
import math

def vector_magnitute(vector):
    """
    Calculates vector magnitude
    """
    vector_sum = 0
    for value in vector:
        vector_sum += value ** 2
    return math.sqrt(vector_sum)

def normalise(vector):
    """
    Normalises vector
    """
    magnitude = vector_magnitute(vector)
    normalised = []
    for value in vector:
        normalised.append(value / magnitude)
    return normalised
