import numpy as np
import matplotlib.pyplot as plt

def plot_images(images, images_width):
    fig = plt.figure(figsize=(5, 5))
    images_height = (int)(len(images[0]) / images_width)
    images = np.array(images).reshape(-1, images_height, images_width)
    number_of_images = len(images)
    for i in range(number_of_images):
        ax = fig.add_subplot(number_of_images, 3, i + 1)
        ax.matshow(images[i], cmap="Oranges")
        plt.xticks(np.array([]))
        plt.yticks(np.array([]))
    plt.show()

def plot_images2(images, images_width, title, no_i_x, no_i_y=3):
    fig = plt.figure(figsize=(10, 15))
    fig.canvas.set_window_title(title)
    images_height = (int)(len(images[0][0]) / images_width)
    images = np.array(images).reshape(-1, images_height, images_width)
    number_of_images = len(images)
    for i in range(no_i_x):
        for j in range(no_i_y):
            ax = fig.add_subplot(no_i_x, no_i_y, no_i_x * j + (i + 1))
            ax.matshow(images[no_i_x * j + i], cmap="gray")
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))

            if j == 0 and i == 0:
                ax.set_title("Real")
            elif j == 0 and i == 1:
                ax.set_title("Distorted")
            elif j == 0 and i == 2:
                ax.set_title("Reconstructed")
    plt.show()