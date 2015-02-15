from math import copysign, exp
from random import shuffle
import numpy as np
from neural.utils import *

U = 1.001
D = 0.999


class Perceptron:
    def __init__(self, w_len, learning_rate=10, func=SigmoidActivator(),
                 momentum=.1):
        self.learning_rate = np.ones(w_len + 1) * learning_rate
        self.weights = np.random.rand(w_len + 1) * 1000
        self.activator = func
        self.last_delta = np.zeros(w_len + 1)
        self.last_deriv = 0
        self.momentum = momentum

    def train(self, training_set, target_function, it_limit=10000000):
        training_set = list(training_set)

        for _ in range(it_limit):
            shuffle(training_set)

            for instance in training_set:
                dp = target_function(*instance)
                x = np.r_[instance, 1]
                yp = self.activator(np.dot(self.weights, x))
                if not near(dp, yp):
                    deriv = self.activator.deriv(yp)
                    delta_w = (dp - yp) * deriv
                    self.learning_rate *= (U if self.last_deriv * deriv >= 0
                                           else D)
                    delta_w *= self.learning_rate
                    delta_w += self.momentum * self.last_delta
                    self.weights += delta_w * x
                    self.last_delta = delta_w
                    self.last_deriv = deriv
                    #print(self.weights, self.last_delta)
                    break
            else:
                break
        else:
            return False
        return True

    def __call__(self, input_vec):
        input_vec = np.r_[input_vec, 1]
        return self.activator(np.dot(input_vec, self.weights))


