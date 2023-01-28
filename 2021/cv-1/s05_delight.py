"""
s04_mask_0.py 得到比较好的star mask.
以此为基础，尝试用中值平均去除光污染
"""
import math
import time
from pathlib import Path

import cv2
import numpy as np
import numba

from star_common import imsave

SRC_0 = 'star-cache/gray__x2/s_00.png'
SRC_1 = 'star-cache/x2/s_00.png'

OUT_DIR = Path("o/005")

#@numba.jit(nopython=False)
def background(src, mask, ksize=10):
    ret, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    if len(src.shape) == 2:
        src = np.expand_dims(src, -1)

    dst = src.copy()
    height = mask.shape[0]
    width = mask.shape[1]
    for row in range(ksize, height - ksize):
        for col in  range(ksize, width - ksize):
            if mask[row, col] == 0:
                continue
            ssub = src[row - ksize:row + 1 + ksize, col - ksize:col + 1 + ksize, :].astype(np.int32)
            msub = mask[row - ksize:row + 1 + ksize, col - ksize:col + 1 + ksize].astype(np.int32)
            msub = 255 - msub
            msum = np.sum(msub)
            if msum == 0:
                print("dead zone %d,%d" % (row, col))
                continue
            x = np.tensordot(ssub, msub, axes=([0,1], [0, 1]))
            #dst[row, col, :] = (np.tensordot(ssub, msub, axes=([0,0], [1,1])) / np.sum(msub)).astype(np.int8)
            #print(ssub.shape)
            #print(msub.shape)
            dst[row, col, :] = (x / np.sum(msub)).astype(np.int8)
            # print(msub)
            # print(x)
            # print(dst[row, col,:])
            #print(dst[row, col, :])
    return dst

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
    #raw = cv2.GaussianBlur(raw, (5, 5), 0)
    mask = mask0_blur
    tic = time.perf_counter()
    bg = background(raw, mask)
    toc = time.perf_counter()
    print(f"use {toc - tic:.4f} seconds")
    imsave(o, "30_background.png", bg)

    star = np.abs(raw.astype(np.int32) - bg.astype(np.int32)).astype(np.int8)
    imsave(o, "99_star.png", star)
    # 彩色照片
    #src2 = cv2.imread(SRC_1)
    #background = mask_bg(src2, mask0_blur)
    

if __name__ == '__main__':
    main()