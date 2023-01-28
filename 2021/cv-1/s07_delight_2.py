"""
s04_mask_0.py 得到比较好的star mask.
以此为基础，尝试用中值平均去除光污染
"""
import math
import time
from pathlib import Path

import cv2
import numpy as np
from star_common import imsave

SRC_0 = 'star-cache/gray__x2/s_00.png'
SRC_1 = 'star-cache/x2/s_00.png'

OUT_DIR = Path("o/007")

def main():
    o = OUT_DIR
    o.mkdir(parents=True, exist_ok=True)

    src = cv2.imread(SRC_0, cv2.IMREAD_GRAYSCALE)
    gray = src
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
    imsave(o, "10_gaussian.png", gaussian)
    print(f"gaussian mean:{np.mean(gaussian)}, std:{np.std(gaussian)}")

    gray = gaussian
    mean = np.mean(gray)
    std = np.std(gray)
    ret0, mask0 = cv2.threshold(gray, mean + int(std * 2.15), 255, cv2.THRESH_BINARY)
    imsave(o, "20_mask_0.png", mask0)

    mask0_blur = cv2.GaussianBlur(mask0, (7, 7), 0)
    imsave(o, "22_mask_0_blur.png", mask0_blur)

    raw = cv2.imread(SRC_1)
    imsave(o, "00_src.png", raw)

    star = np.empty(raw.shape, np.int32)
    for i in range(3):
        star[:,:,i] = (raw[:,:,i].astype(np.int32) * mask0_blur / 255)

    star = star.astype(np.uint8)
    imsave(o, "99_star.png", star)

    #raw = cv2.GaussianBlur(raw, (5, 5), 0)
    #mask = mask0_blur
    # bg = background(raw, mask)
    # toc = time.perf_counter()
    # print(f"use {toc - tic:.4f} seconds")
    # imsave(o, "30_background.png", bg)

    # star = np.abs(raw.astype(np.int32) - bg.astype(np.int32)).astype(np.int8)
    
    # 彩色照片
    #src2 = cv2.imread(SRC_1)
    #background = mask_bg(src2, mask0_blur)
    

if __name__ == '__main__':
    main()