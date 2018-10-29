import numpy as np
import matplotlib.pyplot as plt
import random

def train(neu, training_data):
    w = np.zeros([neu, neu])
    for data in training_data:
        w += np.outer(data, data)
    return w

def test(weights, testing_data, update_type):
    success = 0.0

    output_data = []

    for data in testing_data:
        true_data = data[0]
        noisy_data = data[1]
        predicted_data = retrieve_pattern(weights, noisy_data, update_type)
        if np.array_equal(true_data, predicted_data):
            success += 1.0
        output_data.append([true_data, noisy_data, predicted_data])

    return (success / len(testing_data)), output_data

def retrieve_pattern(weights, data, update_type, steps=200):
    res = np.array(data)

    for _ in range(steps):
        if(update_type == 'synchronous'):
            for i in range(len(res)):
                raw_v = np.dot(weights[i], res)
                if raw_v > 0:
                    res[i] = 1
                else:
                    res[i] = -1
        if(update_type == 'asynchronous'):
            index = random.randrange(len(res))
            raw_v = np.dot(weights[index], res)
            if raw_v > 0:
                res[index] = 1
            else:
                res[index] = -1

    return res


