import os
import io
import shutil
import numpy as np
import matplotlib.pyplot as plt
from config import cfg
from PIL import Image

def plot_images(images, images_width, title, no_i_x, no_i_y=3):
    fig = plt.figure(figsize=(10, 15))
    fig.canvas.set_window_title(title)
    images_height = (int)(len(images[0][0]) / images_width)
    images = np.array(images).reshape(-1, images_height, images_width)
    for i in range(no_i_x):
        for j in range(no_i_y):
            ax = fig.add_subplot(no_i_x, no_i_y, no_i_x * j + (i + 1))
            ax.matshow(images[no_i_x * j + i], cmap="Oranges")
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))

            if j == 0 and i == 0:
                ax.set_title("Real")
            elif j == 0 and i == 1:
                ax.set_title("Distorted")
            elif j == 0 and i == 2:
                ax.set_title("Reconstructed")
    plt.show()

def save_as_image(picture_number, iteration, data):
    pixel_size = cfg.output_pixel_size
    if (pixel_size < 0):
        return
    path = './results/'+cfg.images_path[cfg.images_path.rfind('\\'):] + '/'
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.path.isdir(path+str(picture_number)):
        os.mkdir(path+str(picture_number))
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

def remove_results_folder():
    path = './results/'+cfg.images_path[cfg.images_path.rfind('\\'):] + '/'
    shutil.rmtree(path, ignore_errors=True)