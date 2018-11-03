import numpy as np
import matplotlib.pyplot as plt
import random
import images as images
from config import cfg

def train(neu, training_data):
    w = np.zeros([neu, neu])
    for data in training_data:
        w += np.outer(data, data)
    for i in range(neu):
        w[i][i] = 0
    if cfg.serialize_matrix:
        with open("./results/matrix.txt", 'w') as f:
            for arr in w:
                for item in arr:
                    f.write("%s" % NPositionNumber(item))
                f.write("\n")
    return w

def NPositionNumber(number, positions=10):
    result = str(number);
    while len(result) < positions:
        result = " " + result
    return result



def test(weights, testing_data, update_type, steps, patterns):
    success = 0.0
    iteration = 0
    output_data = []

    images.remove_results_folder()

    for data in testing_data:
        true_data = data[0]
        noisy_data = data[1]
        predicted_data = retrieve_pattern(weights, noisy_data, update_type, steps, patterns, iteration)
        if np.array_equal(true_data, predicted_data):
            success += 1.0
        output_data.append([true_data, noisy_data, predicted_data])
        iteration += 1

    return (100 * success / len(testing_data)), output_data

def retrieve_pattern(weights, data, update_type, steps=200, patterns = None, iteration = 0):
    res = np.array(data)
    prev = None
    prev2 = None
    last_saved = None

    for step in range(steps):
        if(update_type == 'synchronous' or (np.array_equal(last_saved, res) == False)):
            images.save_as_image(iteration, step, res)
            last_saved = np.copy(res)
        prev2 = prev
        prev = np.copy(res)
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
        stopValue = stop_criterium(update_type, prev2, prev, res, patterns)
        if stopValue > 0:
            if stopValue == 1:
                print('repeated pattern', step + 1)
            elif stopValue == 2:
                print('cyclic pattern', step + 1)
            else:
                print('same as training pattern', step + 1)
            images.save_as_image(iteration, step + 1, res)
            return res
    print('returning because of iterations limit', step + 1)
    images.save_as_image(iteration, step + 1, res)
    return res

def stop_criterium(update_type, prev2_data, prev_data, data, patterns):
    if(update_type == 'synchronous'):
        if np.array_equal(data, prev_data):
            return 1
        if np.array_equal(data, prev2_data):
            return 2
    for pattern in patterns:
        if np.array_equal(data, pattern):
            return 3
    return -1