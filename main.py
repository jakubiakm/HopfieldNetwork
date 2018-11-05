import numpy as np
import tensorflow as tf
import data as data
import images as images
import hopfield as hopfield

from config import cfg

def validate_arguments():
    if((cfg.update_type == 'asynchronous' or cfg.update_type == 'synchronous') == False):
        raise ValueError('Wrong update_type value. Possible values are: [''asynchronous'', ''synchronous'']')

def print_arguments():
    print(f'Number of neurons = {cfg.number_of_neurons}')
    print(f'Image path = {cfg.images_path}')
    print(f'Image width = {cfg.image_width}')
    print(f'Network update type = {cfg.update_type}')  
    print(f'Step count in update = {cfg.steps}')  
    print(f'Test data distortion = {cfg.distortion}')
    print(f'Number of tests = {cfg.number_of_tests}')
    
def main(_):
    validate_arguments()
    print_arguments()
    patterns = data.get_data(cfg.images_path)
    training_data = [np.array(d) for d in patterns]
    test_data = data.get_test_data(training_data, cfg.number_of_tests, cfg.distortion)

    W = hopfield.train(cfg.number_of_neurons, patterns)
    accuracy, op_imgs = hopfield.test(W, test_data, cfg.update_type, cfg.steps, patterns)
    print("Accuracy of the network is %f" % (accuracy))
   
if __name__ == "__main__":
    tf.app.run()