import numpy as np
import cv2
from PIL import Image

W = 21
M = 10
N = 30

MAP = """
##############################
#         #              #   #
# ####    ########       #   #
#    #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  #     #
#              #       #     #
##############################
"""

MAP = [list(x) for x in MAP.split("\n") if x]

def generate_map_image():
    mau_xanh = np.zeros((W, W, 3), np.uint8) + (255, 0, 0)
    mau_trang = np.zeros((W, W, 3), np.uint8) + (255, 255, 255)
    image = np.ones((M * W, N * W, 3), np.uint8) * 255

    for x in range(0, M):
        for y in range(0, N):
            if MAP[x][y] == '#':
                image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_xanh
            elif MAP[x][y] == ' ':
                image[x * W:(x + 1) * W, y * W:(y + 1) * W] = mau_trang

    color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_coverted)
    return pil_image
