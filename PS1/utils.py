# !/usr/bin/python

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def normalize_image(img: np.ndarray, threshold: float = 0.1):
    """
    normalize the image to be between 0 and 1
    0 if pixel value < threshold else 1
    """
    dims = img.shape
    env = np.ones(dims)
    z = np.where(img < threshold)
    env[z] = 0.0
    return env


def plot_enviroment(img: np.ndarray, obj: np.ndarray, state: tuple, cut: bool = False):
    """
    @param img: original image in 2d
    @param obj: is the 3d array of different configurations
    @param state: is the curent pose (x, y, orientation) of the object

    @return: the merged image
    """
    dims = obj.shape
    dim_x = int((dims[0] - 1) / 2)
    dim_y = int((dims[1] - 1) / 2)
    obj_pixels = np.dstack(np.nonzero(obj[:,:,state[-1]])).squeeze()
    # from icecream import ic
    # ic(dims, dim_x, dim_y, state)
    # ic(state[0] - dim_x, state[0] + dim_x + 1)
    # ic(state[1] - dim_y, state[1] + dim_y + 1)
    
    merged_img = np.copy(img)
    for obj_pixel in obj_pixels:
        merged_img[state[0] - dim_x+obj_pixel[0],
                   state[1] - dim_y+obj_pixel[1]] += 0.5    
    # merged_img[state[0] - dim_x:state[0] + dim_x + 1, 
    #            state[1] - dim_y:state[1] + dim_y + 1] += \
    #                obj[:, :, state[2]] * 0.5
    if cut:
        return merged_img[state[0] - dim_x:state[0] + dim_x + 1,
                          state[1] - dim_y:state[1] + dim_y + 1]
    return merged_img


def plotting_results(environment: np.ndarray, rod: np.ndarray, 
                     plan: list, save_path: str = 'rod_solve.mp4'):
    """
    create an animation of the plan and save it to a file

    @param environment: the environment image in 2d
    @param rod: is the 3d array of different configurations
    @param plan: list of poses
    @param save_path: path to save the animation
    """

    fig = plt.figure()
    imgs = []

    for state in plan:
        im = plot_enviroment(environment, rod, state)
        plot = plt.imshow(im)
        imgs.append([plot])

    ani = animation.ArtistAnimation(fig, imgs, interval=50, blit=True)

    ani.save(save_path)

    plt.show()
