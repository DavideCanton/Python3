__author__ = 'davide'

import numpy as np
import itertools as it
from random import shuffle
from utils import *


class MultiLayerNetwork:
    def __init__(self, layers, learning_rate=10, momentum=.5,
                 activator=StepActivator()):
        self.matrixes = [np.zeros((level, w + 1))
                         for level, w in zip(layers[1:], layers)]
        self.old = [np.zeros_like(m) for m in self.matrixes]
        self.rate = learning_rate
        self.momentum = momentum
        self.activator = activator

    def __call__(self, x):
        seq = []
        for matrix_layer in self.matrixes:
            x = np.r_[x, 1]
            seq.append(x)
            output = np.dot(matrix_layer, x)
            x = self.activator(output)
        seq.append(np.r_[x, 1])
        return x, seq

    def train(self, training_set, target_function, it_limit=100000):
        training_set = list(training_set)
        for _ in range(it_limit):
            shuffle(training_set)
            for instance in training_set:
                correct_value = target_function(*instance)
                net_value, seq = self(instance)
                if not np.allclose(correct_value, net_value):
                    correct_vec = np.r_[correct_value, 1]
                    self._adjust_weights(correct_vec, seq)
                    break
            else:
                # nessun break, tutti corretti
                break
        else:
            return False
        return True

    def _adjust_weights(self, y, seq):
        error = None
        for level in range(1, len(self.matrixes) + 1):
            out_level = seq[-level]
            pred_level = seq[-level - 1]
            if level == 1:
                error = self._get_out_error(y, out_level)
            else:
                error = self._get_hidden_error(out_level, error, level)
            error = error[:-1]
            delta = (self.rate *
                     error.reshape((-1, 1)) *
                     pred_level.reshape((1, -1)))
            self.matrixes[-level] += delta
            self.matrixes[-level] += self.momentum * self.old[-level]
            self.old[-level] = delta

    def _get_out_error(self, y, yp):
        return (y - yp) * self.activator.deriv(yp)

    def _get_hidden_error(self, yp, error, level):
        error = error.reshape((1, -1))
        res = np.dot(error, self.matrixes[-level + 1]).reshape((1, -1)).flatten()
        return self.activator.deriv(yp) * res

    def __str__(self):
        return "\t".join("Level {}: {}".format(i + 1, l)
                         for i, l in enumerate(self.matrixes))


if __name__ == "__main__":
    def compute_error(correct_value, net_value):
        if near(correct_value, 0):
            return abs(net_value)
        else:
            return abs(net_value - correct_value) / abs(correct_value)

    network = MultiLayerNetwork([1, 1, 1])

    ts = [[i] for i in range(3)]
    correct_function = lambda x: np.array([x > 1], dtype=np.int)
    esito = network.train(ts, correct_function)
    print(network)

    print("Esito training:", esito)
    print("Input", "Rete", "Corretto", "Errore", sep="\t\t")
    for input_value in ts:
        input_value = input_value[0]
        net_value = network([input_value])[0]
        correct_value = correct_function(input_value)
        err = compute_error(correct_value, net_value)
        print([input_value], net_value, correct_value, err, sep="\t\t\t")