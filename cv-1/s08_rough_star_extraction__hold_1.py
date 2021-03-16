"""
s04_mask_0.py 得到比较好的star mask.
以此为基础，尝试用中值平均去除光污染
"""
import math
import time
from pathlib import Path

import cv2
import numpy as np
from star_common import imsave, mkdir

SRC_0 = 'star-cache/gray__x2/s_00.png'
SRC_1 = 'star-cache/x2/s_00.png'

OUT_DIR = Path("o/008")

def main():
    o = OUT_DIR
    mkdir(o)
    src = cv2.imread(SRC_0, cv2.IMREAD_GRAYSCALE)
    g0 = src
    ks = 5
    g1 = cv2.GaussianBlur(g0, (ks, ks), 0)
    imsave(o, "10_g1.png", g1)
    g2 = cv2.GaussianBlur(g1, (ks, ks), 0)
    imsave(o, "10_g2.png", g2)
    g3 = cv2.GaussianBlur(g2, (ks, ks), 0)
    imsave(o, "10_g3.png", g3)

    g2_1 = cv2.subtract(g1, g2)
    imsave(o, "20_g2_1.png", g2_1)
    g3_2 = cv2.subtract(g3, g1)
    imsave(o, "20_g3_2.png", g3_2)
    _, g3_2_b = cv2.threshold(g3_2, 3, 255, cv2.THRESH_BINARY)
    imsave(o, "20_g3_2_b.png", g3_2_b)


if __name__ == '__main__':
    main()