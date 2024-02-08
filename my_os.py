from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import os
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks


def open_rtv(fname):
    file = open(fname, 'rb')
    n = 1024 * 1360
    file_array = np.fromfile(file, dtype='uint16', offset=0x2000, count=n * 4).reshape((4, 1024, 1360))
    ar_right = np.copy(file_array[1::2, :, :1360 // 2])
    ar_left = np.copy(file_array[1::2, :, 1360 // 2:])
    file_array[1::2, :, :1360 // 2] = ar_left
    file_array[1::2, :, 1360 // 2:] = ar_right

    image_array = np.copy(file_array)
    file.close()
    return image_array


def open_folder():
    open_flag = 1
    images_list = []
    file_name = filedialog.askopenfilename(initialdir='./Example')
    images_list.append(open_rtv(file_name))
    while open_flag:
        try:
            file_name = filedialog.askopenfilename()
            images_list.append(open_rtv(file_name))
        except Exception as ex:
            print(ex)
            open_flag = 0
    return images_list
