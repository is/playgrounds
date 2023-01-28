from pathlib import Path

import numpy as np
import cv2

from star_common import imsave

S0 = 'star-cache/x1/s_00.png'
# S0 = 'blob_detection.jpeg'
OUT_DIR = Path('o/012')

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = cv2.imread(S0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    im_mask, cnts, hierarchy = cv2.findContours(gray,
        cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    mask2 = np.zero(img)
    cv2.drawContours(mask2, cnts, -1,(255,255,255),-1)
    imsave(OUT_DIR, "contours.png", mask2)

if __name__ == '__main__':
    main()