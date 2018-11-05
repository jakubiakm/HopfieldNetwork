import numpy as np
import matplotlib.pyplot as plt
import random
import images as images
import os
import datetime
from config import cfg

def train(neurons, training_data):
    w = np.zeros([neurons, neurons], dtype='b')
    ind = 0
    for data in training_data:
        w += np.outer(data, data)
        print(f'training iteration: {ind} time: {datetime.datetime.now()}')
        ind += 1
    for i in range(neurons):
        w[i][i] = 0
    return w

def serialize_matrix(matrix):
     if cfg.serialize_matrix:
        directory = './results/'+cfg.images_path[cfg.images_path.rfind('\\'):] + '/'
        if not os.path.isdir(directory):
            os.mkdir(directory)
        with open(directory + "_matrix.txt", 'w') as f:
            for arr in matrix:
                for item in arr:
                    f.write("%s" % n_position_number(item))
                f.write("\n")

def n_position_number(number, positions=10):
    result = str(number)
    while len(result) < positions:
        result = " " + result
    return result

def test(weights, testing_data, update_type, steps, patterns):
    success = 0.0
    iteration = 0
    output_data = []

    images.remove_results_folder()
    serialize_matrix(weights)

    for data in testing_data:
        true_data = data[0]
        noisy_data = data[1]
        images.save_as_image(iteration, 0, true_data)
        predicted_data = retrieve_pattern(weights, noisy_data, update_type, steps, patterns, iteration)
        if np.array_equal(true_data, predicted_data):
            success += 1.0
        output_data.append([true_data, noisy_data, predicted_data])
        iteration += 1

    return (100 * success / len(testing_data)), output_data

def retrieve_pattern(weights, data, update_type, steps=20000, patterns = None, iteration = 0):
    res = np.array(data)
    prev = None
    prev2 = None
    last_saved = None
    last_saved_permutation = np.copy(res)
    permutation_array = np.arange(len(res))
    np.random.shuffle(permutation_array)
    index = 0
    for step in range(steps):
        if(update_type == 'synchronous' or (np.array_equal(last_saved, res) == False)):
            images.save_as_image(iteration, step + 1, res)
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
            raw_v = np.dot(weights[permutation_array[index]], res)
            if raw_v > 0:
                res[permutation_array[index]] = 1
            else:
                res[permutation_array[index]] = -1
            index += 1
            
        stopValue = stop_criterium(update_type, prev2, prev, res, last_saved_permutation, index, patterns)
        if index == len(res):
            np.random.shuffle(permutation_array)
            last_saved_permutation = np.copy(res)
            index = 0

        if stopValue > 0:
            if stopValue == 1:
                print('repeated pattern', step + 1)
            elif stopValue == 2:
                print('cyclic pattern', step + 1)
            elif stopValue == 3:
                print('asynchronous cyclic pattern', step + 1)
            else:
                print('same as training pattern', step + 1)
            images.save_as_image(iteration, step + 2, res)
            return res
    print('returning because of iterations limit', step + 1)
    images.save_as_image(iteration, step+2, res)
    return res

def stop_criterium(update_type, prev2_data, prev_data, data, last_saved_permutation, index, patterns):
    if(update_type == 'synchronous'):
        if np.array_equal(data, prev_data):
            return 1
        if np.array_equal(data, prev2_data):
            return 2
    if(update_type == 'asynchronous'):
        if index == len(data):
            if np.array_equal(data, last_saved_permutation):
                return 3
    for pattern in patterns:
        if np.array_equal(data, pattern):
            return 4
    return -1
    