import json
from pathlib import Path

import numpy as np
import cv2
import ray

from star_common import imsave, mkdir, star_source_img_ids
import star_common as sc

INPUT = 'x1'

IN_DIR = Path(sc.CACHE_DIR, INPUT)
MID_DIR = Path('o/star_060')
OUT_DIR = MID_DIR

# R = 90
# G = 110
# B = 100

def main():
    mkdir(MID_DIR)
    mkdir(OUT_DIR)

    ids = sc.star_source_img_ids()
    img = cv2.imread(str(IN_DIR / f"{ids[0]}.png"))
    height, width, c = img.shape
    base = np.empty(img.shape).astype(np.int32)
    mask = cv2.imread('o/017/0__bigmask.png')
    
    o = 0
    tx = 1.66774462e+01
    ty = 1.06190648e+01
    # K = 20 
    # DB = 100 + K
    # DG = 100 + K
    # DR = 100 + K
    K = 120
    DB = 10 + K
    DG = 10 + K
    DR = 10 + K
    for id in ids:
        img = cv2.imread(str(IN_DIR / f"{id}.png"))
        img = np.maximum(img, mask) - mask
        img[:,:,0] = np.maximum(img[:,:,0], DB) - DB
        img[:,:,1] = np.maximum(img[:,:,1], DG) - DG
        img[:,:,2] = np.maximum(img[:,:,2], DR) - DR
        if o != 0:
            m = np.array([[1, 0, - tx * o],[0, 1, - ty * o]])
            img = cv2.warpAffine(img, m, (width, height))
        base += img
        o += 1

    base = base / (len(ids) - 10)
    # base = np.maximum(base, 25) - 25
    base = np.minimum(base, 255)
    # base = cv2.GaussianBlur(base, (5, 5), 0)
    cv2.imwrite(str(OUT_DIR / "stack.png"), base.astype(np.uint8))
    clip = base[200:-200, 200:-200,:]
    cv2.imwrite(str(OUT_DIR / "stack_clip.png"), clip)
    clip2 = cv2.resize(clip,None, fx=2, fy=2)
    cv2.imwrite(str(OUT_DIR / "stack_clip_2.png"), clip2)


if __name__ == '__main__':
    main()
