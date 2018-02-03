import random
import math

GRAVITY = 0.2

def rain():
        return round(random.uniform(0, 0.1), 3)

def wind():
        return [round(random.uniform(-0.05, 0.05), 3),
                round(random.uniform(-0.05, 0.05), 3)]
