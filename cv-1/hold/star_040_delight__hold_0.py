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
    
    raw = cv2.imread(SRC)
    mask = mask0_blur
    star = np.empty(raw.shape, np.int32)
    for i in range(3):
        star[:,:,i] = (raw[:,:,i].astype(np.int32) * mask / 255)
    star = star.astype(np.uint8)
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
