import numpy as np

# from my_math import *
from my_os import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
from scipy.fft import fft2, ifft2
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

class XRapid_viewer:
    def __init__(self, *args, **kwargs):
        self.data_dict = open_folder()
        self.sort_data_dict()
        self.show_original()






    def save_all_images(self, name):
        fig, ax = plt.subplots(2, 4)
        fig.set_size_inches(11.7, 8.3)
        for i in range(4):
            ax[0, i].imshow(self.before_array[i])
            ax[0, i].set_title(f'from {int(self.starts[i] * 1000)} ns to {int(self.stops[i] * 1000)} ns')
            ax[1, i].imshow(self.shot_array[i])
        plt.tight_layout()
        fig.savefig(name)
        plt.close()

    def save_all_images_specter(self, name):
        fig, ax = plt.subplots(2, 4)
        fig.set_size_inches(11.7, 8.3)
        for i in range(4):
            show_array = np.abs(self.before_array_specter[i]) + 1.0e-5
            show_array = np.where(show_array > 1.0e-3, np.log(show_array), 1.0e-3)
            ax[0, i].imshow(show_array)
            ax[0, i].set_title(f'from {int(self.starts[i] * 1000)} ns to {int(self.stops[i] * 1000)} ns')
            show_array = np.abs(self.shot_array_specter[i]) + 1.0e-5
            show_array = np.where(show_array > 1.0e-3, np.log(show_array), 1.0e-3)
            ax[1, i].imshow(show_array)
        plt.tight_layout()
        fig.savefig(name)
        plt.close()



    def contrast(self, image_array):
        ret_array = (image_array * 3) ** 2
        return ret_array

    def clean_picks(self, image_array):
        n_image, h_image, w_image = image_array.shape
        ret_array = image_array
        fft_array_abs = np.abs(image_array)
        for i in range(n_image):
            max_filter = maximum_filter(fft_array_abs[i], size=100)
            max_index = np.argwhere(fft_array_abs[i] == max_filter)
            w = 10
            for xy in max_index:
                if xy in np.array([[0, 0], [h_image - 1, 0], [0, w_image - 1], [h_image, w_image]]):
                    continue
                x0 = xy[1]
                y0 = xy[0]
                ret_array[i, y0, x0] = 0
                for r in np.arange(1, w):
                    for t in np.arange(0, 2.0 * np.pi, np.pi / int(2.0 * np.pi * r)):
                        x = int(x0 + r * np.cos(t))
                        y = int(y0 + r * np.sin(t))
                        if (x < 0): x = 0
                        if (y < 0): y = 0
                        if (y >= h_image): y = h_image - 1
                        if (x >= w_image): x = w_image - 1
                        ret_array[i, y, x] = 0
        return ret_array

    def show_arrays(self):
        fig, ax = plt.subplots(2, 4)
        for i in range(4):
            ax[0, i].imshow(self.before_array_up[i])
            ax[0, i].plot(self.before_array_up_profile[0][i], self.before_array_up_profile[1][i], 'or')
            ax[0, i].plot(self.before_array_up_approx[i][0], self.before_array_up_approx[i][1])
            ax[1, i].imshow(self.shot_array_up[i])
            ax[1, i].plot(self.shot_array_up_profile[0][i], self.shot_array_up_profile[1][i], 'or')
            ax[1, i].plot(self.shot_array_up_approx[i][0], self.shot_array_up_approx[i][1])
        plt.show()
        plt.clf()
        fig, ax = plt.subplots(2, 4)
        for i in range(4):
            ax[0, i].imshow(self.before_array_down[i])
            ax[0, i].plot(self.before_array_down_profile[0][i], self.before_array_down_profile[1][i], 'or')
            ax[0, i].plot(self.before_array_down_approx[i][0], self.before_array_down_approx[i][1])
            ax[1, i].imshow(self.shot_array_down[i])
            ax[1, i].plot(self.shot_array_down_profile[0][i], self.shot_array_down_profile[1][i], 'or')
            ax[1, i].plot(self.shot_array_down_approx[i][0], self.shot_array_down_approx[i][1])
        plt.show()

    def get_norm_array(self, image_array):
        ret = image_array.astype(float)
        for i in range(image_array.shape[0]):
            ret[i] -= ret[i].min()
            ret[i] /= ret[i].max()
        return ret

    def sort_data_dict(self):
        self.before_array = self.data_dict['before']
        self.shot_array = self.data_dict['shot']
    def show_original(self):
        plt.imshow(self.before_array[0])
        plt.show()
        plt.clf()
        fig, ax = plt.subplots(2, 4)
        for i in range(4):
            ax[0, i].imshow(self.before_array[i])
            #ax[0, i].set_title(f'from {int(self.starts[i] * 1000)} ns to {int(self.stops[i] * 1000)} ns')
            ax[1, i].imshow(self.shot_array[i])
        plt.show()
