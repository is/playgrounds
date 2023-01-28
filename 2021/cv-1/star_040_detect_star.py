import json
from pathlib import Path

import numpy as np
import cv2
import ray

from star_common import imsave, mkdir, star_source_img_ids
import star_common as sc

INPUT = 'x1'

IN_DIR = Path(sc.CACHE_DIR, INPUT)
MID_DIR = Path('o/star_040')
OUT_DIR = Path(sc.CACHE_DIR, 'contour')

MASK_THRESHOLD_0 = 190

def mid_save(id, name, img):
    imsave(MID_DIR, f"{id}_{name}.png", img)

@ray.remote
def process(id):
    img = cv2.imread(str(IN_DIR/f"{id}.png"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    mid_save(id, '01_blur', blur)

    _, mask = cv2.threshold(blur, MASK_THRESHOLD_0, 255, cv2.THRESH_BINARY)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=4)
    mid_save(id, '03_mask', mask)

    contours, _hierarchy = cv2.findContours(mask,
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"{id} has {len(contours)} contours")
    cnt_img = cv2.drawContours(gray, contours, -1, [0], 3)
    mid_save(id, '05_contour', gray)

    ds = []
    for contour in contours:
        ci = {}
        m = cv2.moments(contour)
        ci['M'] = m
        ci['area'] = cv2.contourArea(contour)
        ci['cx'] = m['m10'] / m['m00']
        ci['cy'] = m['m01'] / m['m00']
        ci['diameter'] = np.sqrt(4*ci['area']/np.pi)
        ci['shape'] = mask.shape[:2]
        ds.append(ci)
    return id, ds

def main():
    mkdir(MID_DIR)
    mkdir(OUT_DIR)
    ray.init()
    ids = sc.star_source_img_ids()
    futures = [process.remote(id) for id in ids]
    dss = ray.get(futures)
    dss.sort(key = lambda x: x[0])
    s = json.dumps(dss, indent=True)
    #print(s)
    with open('star-cache/040__contours.json', 'w') as fout:
        fout.write(s) 

if __name__ == '__main__':
    main()
