__author__ = 'davide'

from neural.perceptron import Perceptron
from utils import *
import matplotlib.pyplot as plt
import itertools as it
import numpy as np

if __name__ == "__main__":
    target_function = lambda a, b: float(a + b > 3)
    training_set = list(it.product(range(5), repeat=2))
    perceptron = Perceptron(2, learning_rate=1,
                            momentum=.5, func=StepActivator())
    if not perceptron.train(training_set, target_function):
        exit("NO")

    correct = np.array(list(it.starmap(target_function, training_set)))
    neural = np.array(list(map(perceptron, training_set)))

    print(neural)
    print(correct)

    print(perceptron.weights)