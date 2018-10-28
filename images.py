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