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
        self.shot_array = np.array(open_folder())
        self.show_original()

    def show_original(self):
        fig, ax = plt.subplots(self.shot_array.shape[0], self.shot_array.shape[1])
        fig.set_layout_engine(layout='tight')
        try:
            for i in range(self.shot_array.shape[1]):
                ax[i].imshow(self.shot_array[0, i], cmap='gray_r')
        except:
            for i in range(self.shot_array.shape[0]):
                for j in range(self.shot_array.shape[1]):
                    ax[i, j].imshow(self.shot_array[i, j], cmap='gray_r')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()
