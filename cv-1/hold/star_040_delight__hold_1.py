from pathlib import Path
import numpy as np
import time

import cv2
import ray

import star_common as SC
from star_common import imsave, mkdir

IN = Path(SC.CACHE_DIR, "x2")
OUT = Path(SC.CACHE_DIR, "delight")
OUT_MASK = Path(SC.CACHE_DIR, "delight-mask")


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
            dst[row, col, :] = (x / np.sum(msub)).astype(np.int8)
    return dst


@ray.remote
def process(img_id):
    fn = f"{img_id}.png"
    SRC = str(IN / fn)
    src = cv2.imread(SRC, cv2.IMREAD_GRAYSCALE)
    gray = src
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)

    gray = gaussian
    mean = np.mean(gray)
    std = np.std(gray)
    ret0, mask0 = cv2.threshold(gray, mean + int(std * 2.15), 255, cv2.THRESH_BINARY)
    mask0_blur = cv2.GaussianBlur(mask0, (5, 5), 0)
    imsave(OUT_MASK, fn, mask0)
    raw = cv2.imread(SRC)

    mask = mask0_blur
    tic = time.perf_counter()
    bg = background(raw, mask)
    toc = time.perf_counter()
    print(f"use {toc - tic:.4f} seconds")
    star = np.abs(raw.astype(np.int32) - bg.astype(np.int32)).astype(np.uint8)
    imsave(OUT, fn, star)

def main():
    ray.init(address='auto')
    img_ids = SC.star_source_img_ids()
    mkdir(OUT)
    mkdir(OUT_MASK)
    future = [ process.remote(img_id) for img_id in img_ids ]
    ray.get(future)


if __name__ == '__main__':
    main()
