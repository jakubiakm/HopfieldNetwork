import tensorflow as tf
import data as data
import images as images

from config import cfg

def validate_arguments():
    if((cfg.update_type == 'asynchronous' or cfg.update_type == 'synchronous') == False):
        raise ValueError('Wrong update_type value. Possible values are: [''asynchronous'', ''synchronous'']')

def print_arguments():
    print(f'Number of neurons = {cfg.number_of_neurons}')
    print(f'Image path = {cfg.images_path}')
    print(f'Image width = {cfg.image_width}')
    print(f'Network update type = {cfg.update_type}')  

def main(_):
    validate_arguments()
    print_arguments()
    patterns = data.get_data(cfg.images_path)
    images.plot_images(patterns, cfg.image_width)
    
if __name__ == "__main__":
    tf.app.run()