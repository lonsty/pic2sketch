# @Author: allen
# @Date: May 26 14:37 2020
from typing import Iterable
import os
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from fnmatch import fnmatch


import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage

warnings.filterwarnings('ignore')  # Disable numpy warnings


def mkdirs_if_not_exist(dir):
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
        except FileExistsError:
            pass


def list_files(dir_name: str, include: Iterable = None, exclude: Iterable = None) -> list:
    """
    Get all files in a directory excluding ignored files.
    :param dir_name: str, the root directory.
    :param include: Iterable, the patterns to include.
    :param exclude: Iterable, the patterns to exclude.
    :return: list, the files with full path.
    """
    if not exclude:
        exclude = []
    if not include:
        include = []

    list_of_file = os.listdir(dir_name)
    all_files = []

    for entry in list_of_file:
        full_path = os.path.abspath(os.path.join(dir_name, entry))
        for pattern in exclude:
            if fnmatch(os.path.split(full_path)[-1], pattern):
                break
        else:
            if os.path.isdir(full_path):
                all_files = all_files + list_files(full_path, include, exclude)
            else:
                if not include:
                    all_files.append(full_path)
                else:
                    for pattern in include:
                        if fnmatch(os.path.split(full_path)[-1], pattern):
                            all_files.append(full_path)
                            continue

    return all_files


def _dodge(front, back):
    result = front * 255 / (255 - back)
    result[result > 255] = 255
    result[back == 255] = 255
    return result.astype('uint8')


def _grayscale(rgb, formula=None):
    if not formula:
        formula = [0.299, 0.587, 0.114]
    return np.dot(rgb[..., :3], formula)


def p2sk(img, destination: str, sigma: int=30):

    if not destination:
        destination = os.path.dirname(os.path.abspath(img))

    formula = [0.299, 0.587, 0.114]

    start_img = imageio.imread(img)

    if start_img.shape[2] == 3:
        formula = [0.299, 0.587, 0.114]
    elif start_img.shape[2] == 4:
        formula = [0.299, 0.587, 0.114, -0.35]

    gray_img = _grayscale(start_img, formula)
    inverted_img = 255 - gray_img

    blur_img = scipy.ndimage.filters.gaussian_filter(inverted_img, sigma=sigma)
    final_img = _dodge(blur_img, gray_img)

    name, ext = os.path.splitext(os.path.basename(img))
    filename = os.path.join(destination, f'{name}_sketch{ext}')

    plt.imsave(filename, final_img, cmap='gray', vmin=0, vmax=255)
    return filename


def multi_processes_tasks(images: list, dest: str, sigma: int):
    with ProcessPoolExecutor() as pool:
        futures = [pool.submit(p2sk, img, dest, sigma) for img in images]

    for future in as_completed(futures):
        try:
            result = future.result()
        except Exception as e:
            print(e)
        else:
            print(result)