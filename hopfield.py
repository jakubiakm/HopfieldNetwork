import numpy as np
import matplotlib.pyplot as plt
import random
import os
import io
from PIL import Image
from array import array
from config import cfg

def train(neu, training_data):
    w = np.zeros([neu, neu])
    for data in training_data:
        w += np.outer(data, data)
    for i in range(neu):
        w[i][i] = 0
    return w

def test(weights, testing_data, update_type, steps, patterns):
    success = 0.0
    iteration = 0
    output_data = []

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

    for _ in range(steps):
        saveAsImage(iteration, _, res)
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
        stopValue = stopCriterium(prev2, prev, res, patterns)
        if stopValue > 0:
            if stopValue == 1:
                print('repeated pattern', _+1)
            elif stopValue == 2:
                print('cyclic pattern', _+1)
            else:
                print('same as training pattern', _+1)
            saveAsImage(iteration, _+1, res)
            return res
    print('returning because of iterations limit',_+1)
    saveAsImage(iteration, _+1, res)
    return res

def stopCriterium(prev2_data, prev_data, data, patterns):
    if(cfg.update_type == 'synchronous'):
        if np.array_equal(data, prev_data):
            return 1
        if np.array_equal(data, prev2_data):
            return 2
    for pattern in patterns:
        if np.array_equal(data, pattern):
            return 3
    return -1

def saveAsImage(picture_number, iteration, data):
    pixel_size = cfg.output_pixel_size
    if (pixel_size < 0):
        return
    path = './results/'+cfg.images_path[cfg.images_path.rfind('\\'):] + '/'
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.path.isdir(path+str(picture_number)):
        os.mkdir(path+str(picture_number));
    width = cfg.image_width
    height = int(cfg.number_of_neurons / cfg.image_width)
    
    img = Image.new( '1', (width * pixel_size, height * pixel_size), "black") # Create a new black image
    pixels = img.load() # Create the pixel map
    for i in range(width):    # For every pixel:
        for j in range(height):
            if data[i+cfg.image_width*j] == 1:
                for x in range(pixel_size):
                    for y in range(pixel_size):
                        pixels[i*pixel_size+x,j*pixel_size+y] = (1) # Set the colour accordingly
    img.save(path+str(picture_number)+'/'+str(iteration) + '.bmp')
    

