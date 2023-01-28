"""
06,最简单的堆叠
"""
from pathlib import Path

import cv2
import numpy as np

from star_common import imsave
import star_common as sc

OUT_DIR = Path("o/006")
#IN_DIR = Path("star-cache/x4")
IN_DIR = Path(sc.CACHE_DIR, "delight")

def main():
    o = OUT_DIR
    o.mkdir(parents=True, exist_ok=True)

    img_ids = sc.star_source_img_ids()
    img_ids = img_ids[:]
    src_0 = cv2.imread(str(IN_DIR / f"{img_ids[0]}.png"))
    mgr = np.empty(src_0.shape).astype(np.int32)
    for id in img_ids:
        print(id)
        img = cv2.imread(str(IN_DIR / f"{id}.png"))
        mgr += img
    #mgr = mgr / len(img_ids)
    mgr = np.clip(mgr, 0, 255)
    mgr = mgr.astype(np.uint8)
    imsave(OUT_DIR, "00_stack.png", mgr)

if __name__ == '__main__':
    main()